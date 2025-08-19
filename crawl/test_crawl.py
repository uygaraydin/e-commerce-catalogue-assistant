import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from bs4 import BeautifulSoup
import time
from crawl.utils.extract_data import extract_product_info

async def scrape_all_ikea_pages():
    """Scraping IKEA Pages"""
    
    base_url = "https://www.ikea.com.tr/kampanya/internete-ozel-indirim"
    all_products = [] # TÜM sayfalardaki ürünleri burada toplayacağız
    page = 1
    max_pages = 20  # Güvenlik limiti (sonsuz döngü önleme)
    
    config = CrawlerRunConfig(
        # Ürün container'larını hedefle
        # Sadece .product-item elementlerini hedefle
        # Bu sayede crawl4ai otomatik olarak:
        # 1. Tüm sayfayı indirir (1.164.690 karakter - nav, footer, js, css dahil)
        # 2. Sadece .product-item div'lerini filtreler  
        # 3. Geri kalanını (nav, footer, scripts, css, tracking kodları) çöpe atar
        # 4. Sonuç: 462.212 karakter temiz HTML (%60 azalma)
        target_elements=[
            ".product-item",
        ],
        #DELAY_BEFORE_RETURN_HTML: Ekstra güvenlik beklemesi  
        # wait_for ile element göründü ama henüz tam yüklenmemiş olabilir
        # - CSS animasyonları devam edebilir
        # - Lazy loading henüz tamamlanmamış olabilir  
        # - AJAX istekleri devam ediyor olabilir
        # 3 saniye ekstra bekleyerek "kesin bitti" diyoruz
        wait_for=".product-item",
        delay_before_return_html=3,
        # SCROLL_DELAY: Lazy loading için scroll simülasyonu
        # Çoğu e-ticaret sitesi performans için "lazy loading" kullanır
        # İlk 10-15 ürünü yükler, kullanıcı scroll yaptıkça diğerlerini getirir
        # scroll_delay=1 demek:
        # "Sayfayı yavaş yavaş aşağı kaydır, her kaydırmada 1 saniye bekle"
        # Bu sayede tüm ürünler yüklenir (20-30-40... hepsi)
        scroll_delay=1
    )
    
    # Headers'ı crawler'da tanımla
    # Siteler bot'ları engeller, bu header ile insan gibi görünürüz
    # Default "crawl4ai" header yerine "Chrome browser" header kullan
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    async with AsyncWebCrawler(headless=True, headers=headers) as crawler:
        while page <= max_pages:
            # URL OLUŞTURMA - Hangi sayfaya gidileceğini belirle
            if page == 1: # İlk sayfa: temiz URL (SEO için)
                url = base_url
            else:
                url = f"{base_url}?page={page}"
            
            print(f"\nSayfa {page} scraping: {url}")
            print("-" * 60)
            
            try:
                # crawl4ai sayfayı indirir, JS çalıştırır, scroll yapar, filtreler
                result = await crawler.arun(url=url, config=config)
                
                # HTML string'ini Python objesine çevir (manipüle edilebilir hale getir)
                soup = BeautifulSoup(result.html, 'html.parser')
                
                print(f"HTML uzunluğu: {len(result.html)}")
                print(f"Cleaned HTML uzunluğu: {len(result.cleaned_html)}")
                
                # Ürün kartlarını bul
                product_cards = soup.find_all('div', class_='product-item')
                print(f"Bulunan ürün kartları: {len(product_cards)}")
                
                # Ürün yoksa dur (son sayfa)
                if len(product_cards) == 0:
                    print(f"Sayfa {page}'de ürün bulunamadı. Scraping tamamlandı.")
                    break
                
                # Ürünleri extract et
                page_products = []
                for i, product in enumerate(product_cards, 1): # Her ürün kartını tek tek işle (enumerate = sıra numarası ile)
                    try:
                        product_data = extract_product_info(product)
                        if product_data and product_data.get('title'):  # Sadece title'ı olan ürünleri al
                            # Metadata ekle (hangi sayfa, hangi sırada bulundu)
                            product_data['page'] = page
                            product_data['position_on_page'] = i
                            # Bu sayfanın listesine ekle
                            page_products.append(product_data)
                            print(f"{i:2d}. {product_data['title'][:30]:<30} - {product_data.get('price', 'N/A')} TL")
                        else:
                            print(f"{i:2d}. Ürün verisi eksik")
                    except Exception as e:
                        print(f"{i:2d}. Ürün işlenirken hata: {e}")
                        continue
                
                # Bu sayfanın ürünlerini tüm ürünler listesine ekle
                all_products.extend(page_products)
                print(f"Bu sayfa: {len(page_products)} ürün eklendi")
                print(f"Toplam: {len(all_products)} ürün")
                
                # Aynı ürünler tekrar ediyorsa dur (döngüsel sayfa)
                # İlk sayfada duplikasyon olamaz, boş sayfada kontrol gereksiz
                if page > 1:
                    # Son sayfadaki ilk ürünün URL'si önceki sayfalarda var mı?
                    # Bu sayfadaki ürün linklerini topla
                    current_urls = {p['url'] for p in page_products if p.get('url')}
                    # Önceki sayfalardaki ürün linklerini topla
                    # (Son eklediğimiz sayfayı çıkararak, sadece gerçek eskiler)
                    previous_urls = {p['url'] for p in all_products[:-len(page_products)] if p.get('url')}
                    # Aynı link var mı kontrol et (aynı ürün = aynı link)
                    if current_urls.intersection(previous_urls):
                        print(f"Sayfa {page}'de tekrar eden ürünler bulundu. Scraping tamamlandı.")
                        # Duplikat ürünleri temizle (son eklediğimiz sayfayı çıkar)
                        all_products = all_products[:-len(page_products)]

                        break
                    else:
                        print(f"Sayfa {page}'de tekrar eden ürünler bulunmadı. Scraping devam ediyor.")
                        
                      
                
                # Sayfalar arası nezaket beklemesi (rate limiting)
                if page < max_pages:
                    print(f"2 saniye bekleniyor...")
                    await asyncio.sleep(2)
                
                page += 1
                
            except Exception as e:
                print(f"Sayfa {page} hatası: {e}")
                break
    
    return all_products

async def main():
    print("IKEA Tüm Sayfalar Scraper (Geliştirilmiş)")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        all_products = await scrape_all_ikea_pages()
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\nScraping Tamamlandı!")
        print(f"Toplam {len(all_products)} ürün bulundu")
        print(f"Süre: {duration:.1f} saniye")
        print("=" * 60)
        
        if all_products:
            # Sayfa istatistikleri
            pages = set(p['page'] for p in all_products if 'page' in p)
            print(f"Scrape edilen sayfalar: {sorted(pages)}")
            
            for page in sorted(pages):
                page_count = len([p for p in all_products if p.get('page') == page])
                print(f"Sayfa {page}: {page_count} ürün")
            
            # JSON dosyasına kaydet - timestamp ile
            timestamp = int(time.time())
            filename = f'ikea_all_products_{timestamp}.json'
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(all_products, f, ensure_ascii=False, indent=2)
            
            print(f"\nTüm veriler '{filename}' dosyasına kaydedildi.")
            

            
        else:
            print("Hiç ürün bulunamadı. Sayfa yapısı değişmiş olabilir.")
            
    except Exception as e:
        print(f"Ana hata: {e}")
        import traceback
        traceback.print_exc()



if __name__ == "__main__":
    asyncio.run(main())