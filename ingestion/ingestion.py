from dotenv import load_dotenv
from langchain_community.document_loaders import JSONLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import json

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI embeddings
embeddings=OpenAIEmbeddings()

def ingest_doc():
   # Load JSON data from file - each product becomes a separate document
   loader=JSONLoader("/Users/uygaraydin/Desktop/rag/crawl/ikea_all_products_1754953227.json",
                   jq_schema=".[]",   # Extract each element from JSON array as separate document
                   text_content=False )# Keep JSON structure, convert to string for page_content

   # Load all documents from the JSON file
   docs=loader.load()

   # Process each document to add metadata and clean content
   for doc in docs:
    # Convert JSON string back to dictionary
    product_data = json.loads(doc.page_content)
   
    # Extract URL and add it to metadata as source
    product_url = product_data.get("url", "")
    doc.metadata["source"] = product_url
   
   
    # Convert cleaned JSON back to string format
    doc.page_content = json.dumps(product_data, ensure_ascii=False)

   # Create embedding model for vectorization
   embedding=OpenAIEmbeddings()

   # Create vector store and upload documents to Pinecone index
   vectorstore = PineconeVectorStore.from_documents(
   docs, embedding, index_name="ikea-product-index"
   )

# Run the main function when script is executed directly
if __name__=="__main__":
   # Execute the document ingestion process
   ingest_doc()