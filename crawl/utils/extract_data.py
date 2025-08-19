import re

def extract_product_info(product_element):
    """Bir ürün elementinden tüm bilgileri çıkarır"""
    product_data = {}
    
    try:
        #title
        title_elem = product_element.select_one('.title')
        title = title_elem.get_text(strip=True) if title_elem else None
        product_data['title'] = title
        
        # Description
        desc_elem = product_element.select_one('.desc')
        desc = desc_elem.get_text(strip=True) if desc_elem else None
        product_data['description'] = desc

        # Unit Color
        color_elem = product_element.select_one('.unit-color')
        color = color_elem.get_text(strip=True) if color_elem else None
        product_data['color'] = color

        # Cross Price (Eski fiyat)
        cross_elem = product_element.select_one('.cross-price')
        cross_price = clean_price(cross_elem.get_text(strip=True)) if cross_elem else None
        product_data['cross_price'] = cross_price

        # Discounted (current) price - Güncel fiyat
        price_elem = product_element.select_one('.price span')
        price = clean_price(price_elem.get_text(strip=True)) if price_elem else None
        product_data['price'] = price
      
        #Discount rate-İndirim oranı
        discount_rate_elem = product_element.select_one('.pc-discount-rate')
        discount_rate = clean_discount_rate(discount_rate_elem.get_text(strip=True)) if discount_rate_elem else None
        product_data['pc_discount_rate'] = discount_rate

        #Discount amount-İndirim Miktarı
        discount_amount_elem = product_element.select_one('.pc-discount-amount')
        discount_amount = clean_discount_amount(discount_amount_elem.get_text(strip=True)) if discount_amount_elem else None
        product_data['pc_discount_amount'] = discount_amount

        #Url
        link_elem = product_element.select_one('a.product-link')
        if link_elem and link_elem.get('href'):
            url = link_elem['href']
            # Relative URL'i absolute'a çevir: /urun/... -> https://www.ikea.com.tr/urun/...
            if not url.startswith('http'):
                url = 'https://www.ikea.com.tr' + url
            product_data['url'] = url
        else:
             product_data['url'] = None
        
        return product_data
        
    except Exception as e:
        print(f"Ürün bilgisi çıkarılırken hata: {e}")
        return None

def clean_price(price_text):
    """Fiyat metnini temizler"""
    if not price_text:
        return None
    
    # Sadece ilk rakam grubunu al
    price_match = re.search(r'(\d[\d.,]*)', price_text)
    if not price_match:
        return None
    
    cleaned = price_match.group(1)
    
    # Türk Lirası formatı: 14.999 (nokta binler ayracı)
    if '.' in cleaned and ',' not in cleaned:
        # Sadece nokta var - binler ayracı olabilir
        parts = cleaned.split('.')
        if len(parts[-1]) == 3:  # Son kısım 3 haneli ise binler ayracı
            cleaned = cleaned.replace('.', '')
        # Aksi halde ondalık ayracı olarak bırak
    elif ',' in cleaned:
        # Virgül varsa ondalık ayracı
        cleaned = cleaned.replace('.', '').replace(',', '.')
    
    return cleaned if cleaned.isdigit() or ('.' in cleaned and cleaned.replace('.', '').isdigit()) else None

def clean_discount_rate(rate_text):
    """İndirim oranını temizler: '%12indirim' → '%12'"""
    if not rate_text:
        return None
    
    # %12 kısmını al
    rate_match = re.search(r'(%\d+)', rate_text)
    return rate_match.group(1) if rate_match else rate_text

def clean_discount_amount(amount_text):
    """İndirim miktarını temizler: '2000₺ tasarruf' → '2000'"""
    if not amount_text:
        return None
    
    # İlk rakam grubunu al
    amount_match = re.search(r'(\d+)', amount_text)
    return amount_match.group(1) if amount_match else None
