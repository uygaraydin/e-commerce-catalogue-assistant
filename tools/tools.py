from langchain.agents import Tool
from func.retrieval_func import search_ikea_products
from func.tavily_func import search_external_products

# IKEA Database Search Tool
ikea_tool = Tool(
  name="search_ikea_products",
  func=search_ikea_products,
  description="Search for IKEA furniture and home products in our database. Use this tool first when users ask about any furniture, home decor, or IKEA products. Returns detailed product information including prices, descriptions, and availability."
)

# External Web Search Tool
tavily_tool = Tool(
   name="search_external_products",
   func=search_external_products,
   description="Search the web for furniture and home products when the item is not found in IKEA database. Use this as a fallback when IKEA search returns no results."
)

# Combine all available tools into a list
tools = [ikea_tool, tavily_tool]