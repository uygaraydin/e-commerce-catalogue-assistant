# 🛋️ E-Commerce Catalogue Assistant

An AI-powered RAG (Retrieval-Augmented Generation) application that helps customers find discounted IKEA furniture and home products using web scraping, vector search, and LangChain agents with Streamlit interface.

## Features

- Web scraping of IKEA discount products with crawl4ai and BeautifulSoup
- Vector search using Pinecone and OpenAI embeddings for RAG implementation
- Smart product recommendations using LangChain ReAct agents
- Fallback web search with Tavily when products not found in database
- Turkish language support
- Real-time chat interface with Streamlit
- Persistent chat history

## 🎬 Demo

![Demo Video](./demo.gif)

*Interactive IKEA product search assistant that helps customers find furniture and home decoration items with prices, specifications, and direct product links*

## Installation

1. **Clone and install dependencies:**
   ```bash
   git clone https://github.com/uygaraydin/e-commerce-catalogue-assistant.git
   cd e-commerce-catalogue-assistant
   pip install pipenv
   pipenv install
   pipenv shell
   ```

2. **Set up environment variables:**
   Create a `.env` file:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   TAVILY_API_KEY=your_tavily_api_key
   LANGCHAIN_API_KEY=your_langchain_api_key
   ```

3. **Get your API keys:**
   - **OpenAI API**: https://platform.openai.com/
   - **Pinecone**: https://www.pinecone.io/ (vector database)
   - **Tavily**: https://tavily.com/ (web search API)
   - **LangChain API**: https://smith.langchain.com/ (optional, for tracing)

## Usage

1. **First, scrape IKEA products:**
   ```bash
   python crawl/test_crawl.py
   ```

2. **Ingest scraped data into vector database:**
   ```bash
   python ingestion/ingestion.py
   ```

3. **Start the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and go to `http://localhost:8501`

5. **Search for products** by typing in Turkish or English

## How It Works

The system uses a multi-step approach:
1. **Web Scraping**: crawl4ai and BeautifulSoup scrape IKEA discount pages with lazy loading and pagination handling
2. **Data Processing**: Product information is extracted and cleaned using BeautifulSoup and regex patterns
3. **Data Ingestion**: Processed products are converted to JSON and loaded using LangChain JSONLoader
4. **Vector Storage**: Products are embedded using OpenAI embeddings and stored in Pinecone vector database for RAG retrieval
5. **Smart Search**: LangChain ReAct agent first searches internal Pinecone database, then falls back to Tavily web search directed to IKEA site
6. **Response Generation**: ChatOpenAI (GPT-4) provides helpful product recommendations in Turkish

## Project Structure

```
├── agent/
│   ├── __init__.py
│   └── ikea_agent.py           # LangChain ReAct agent with tools
├── crawl/
│   ├── utils/
│   │   └── extract_data.py     # Product data extraction utilities
│   ├── ikea_all_products_*.json # Scraped product data (generated)
│   └── test_crawl.py           # Main scraping script with crawl4ai
├── func/
│   ├── __init__.py
│   ├── retrieval_func.py       # Vector search functions
│   └── tavily_func.py          # Web search functions
├── ingestion/
│   └── ingestion.py            # Vector database ingestion script
├── tools/
│   ├── __init__.py
│   └── tools.py                # LangChain tools configuration
├── app.py                      # Streamlit web interface
├── .env                        # Environment variables (you create this)
├── Pipfile                     # Pipenv dependencies
├── Pipfile.lock               # Locked dependencies
└── README.md                   # This file
```

## Dependencies

```
streamlit
python-dotenv
crawl4ai
beautifulsoup4
langchain-community
langchain-openai
langchain-pinecone
langchain-tavily
pinecone-client
```

## Development

- **Automated Scheduled Updates**: Set up cron jobs or task schedulers for automatic daily/weekly crawling without manual intervention
- **Real-time Price Validation**: Implement live price checking during user queries to ensure accuracy
- **Background Data Sync**: Continuous monitoring and updating of product database in the background
- **Notification System**: Alert system for when products go out of stock or prices change significantly

## Troubleshooting

- **Scraping Issues**: Check if IKEA website structure changed or discount campaign ended
- **Broken URLs**: Product URLs may change or become inactive over time
- **HTML Structure Changes**: IKEA may update their website structure, requiring scraper updates

## Contributing

Feel free to submit issues and pull requests to improve the application!
