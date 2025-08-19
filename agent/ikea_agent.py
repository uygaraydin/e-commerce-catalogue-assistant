from tools.tools import tools
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def ikea_agent(user_query: str) -> str:
   """IKEA customer service agent that helps customers find furniture and home products"""
   
   # Initialize GPT-4 language model
   llm = ChatOpenAI(model="gpt-4o")
   
   # Define the agent prompt template with instructions and format
   template = """You are an IKEA customer service assistant. Help customers find furniture and home decoration products.

Available tools: {tools}

## Instructions:
1. For product searches: Use search_ikea_products first
2. If no discounted product found in database, say "İndirimli ürün bulunamadı" then use search_external_products
3. For greetings/chat: Answer directly without tools
4. Always respond in Turkish
5. Include price, size, color, and URL in product recommendations
6. For first interaction or introduction: Say "Merhaba! Ben IKEA indirimli ürünler asistanıyım. Size mobilya ve ev dekorasyonu konularında yardımcı olabilirim. Hangi ürünü arıyorsunuz?"

## Response Format

### For Product Search:
Question: [Customer question]
Thought: This is a product search question. I should search IKEA discounted products first, then general web if needed.
Action: search_ikea_products
Action Input: [search term]
Observation: [result]
Thought: [Next step decision - use search_external_products if necessary]
Action: [search_external_products if needed]
Action Input: [search term]
Observation: [result]
Thought: Now I can provide comprehensive answer to customer.
Final Answer: [Detailed product recommendation]

### For Chat:
Question: [Customer question]
Thought: This is a chat question, I'll answer using chat_history or general knowledge.
Final Answer: [Friendly and professional answer]

IMPORTANT: Always respond in Turkish language only, regardless of the input language.

Available actions: [{tool_names}]

Question: {input}
Thought: {agent_scratchpad}"""

   # Create prompt template with required input variables
   prompt = PromptTemplate(
       template=template,
       input_variables=["tools", "chat_history", "tool_names", "input", "agent_scratchpad"]
   )
   
   # Create ReAct agent with LLM, tools, and prompt
   agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
   
   # Create agent executor to run the agent with error handling
   agent_executor = AgentExecutor(
       agent=agent, 
       tools=tools, 
       verbose=True,  # Show detailed execution steps
       handle_parsing_errors=True  # Handle any parsing errors gracefully
   )
   
   # Execute the agent with user query and return the response
   result = agent_executor.invoke({"input": user_query})
   return result["output"]