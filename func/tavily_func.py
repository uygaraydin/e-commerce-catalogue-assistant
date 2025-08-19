from langchain_community.tools.tavily_search import TavilySearchResults

def search_external_products(query: str) -> str:
   """Search for furniture and home products on the web when not found in IKEA database"""
   # Initialize Tavily search tool with maximum 2 results
   search = TavilySearchResults(max_results=2)
   
   # Search specifically on IKEA Turkey website for the product
   result = search.run(f"{query} site: ikea.com.tr/")
   return result
