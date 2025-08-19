from dotenv import load_dotenv  
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

# Load environment variables from .env file
load_dotenv()

# Helper function to format retrieved documents
def format_docs(docs):
   return "\n\n".join(doc.page_content for doc in docs)

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings()

# Initialize ChatOpenAI language model
llm = ChatOpenAI()

# Connect to existing Pinecone vector store
vectorstore = PineconeVectorStore(
   embedding=embeddings, 
   index_name="ikea-product-index"
)

# Define the prompt template for IKEA customer consultation
template = """You are an IKEA customer consultant. Use the following IKEA product information to answer the customer's question.

If NO products are found in the context below, say "This product is not available in our IKEA discount catalog". 

If products ARE found, provide helpful details including price, size, color, and URL.

Always respond in Turkish and use maximum three sentences.

{context}

Question: {input}

Helpful Answer:
"""

# Create custom RAG prompt from template
custom_rag_prompt = PromptTemplate.from_template(template)

# Create chain that combines retrieved documents with LLM for answer generation
combine_docs_chain = create_stuff_documents_chain(llm, custom_rag_prompt)

def search_ikea_products(query):
   """Searches for IKEA products in Pinecone and returns AI-generated answer"""
   
   # Create retrieval chain that fetches data from Pinecone and generates answer using LLM
   retrieval_chain = create_retrieval_chain(
       retriever=vectorstore.as_retriever(search_kwargs={"k": 6}), # Retrieve top 6 similar products
       combine_docs_chain=combine_docs_chain
   )
   
   # Execute the search and get AI-generated response
   res = retrieval_chain.invoke({"input": query})
   return res["answer"]