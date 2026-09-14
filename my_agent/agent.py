# from google.adk.agents.llm_agent import Agent

# root_agent = Agent(
#     model="gemini-2.5-flash",
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='Answer user questions to the best of your knowledge',
# )



#------------------------- RAG ---------------------------------------



# import os

# from google.adk.agents import Agent
# from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
# from vertexai.preview import rag

# from dotenv import load_dotenv

# load_dotenv()

# ask_vertex_retrieval = VertexAiRagRetrieval(
#     name="retrieve_rag_documentation",
#     description=(
#         "Use this tool to retrieve documentation and reference materials for the question from the RAG corpus,"
#     ),
#     rag_resources=[
#         rag.RagResource(
#             # e.g. projects/123/locations/us-central1/ragCorpora/456
#             rag_corpus=os.environ.get("RAG_CORPUS")
#         )
#     ],
#     similarity_top_k=10,
#     vector_distance_threshold=0.6,
# )

# root_agent = Agent(
#     model="gemini-2.5-flash",
#     name="ask_rag_agent",
#     instruction = (
#     "You are an expert RAG documentation assistant. Your task is to answer user questions "
#     "accurately using ONLY information retrieved from the `retrieve_rag_documentation` tool.\n\n"
#     "Workflow & Rules:\n"
#     "1. Always invoke `retrieve_rag_documentation` first before generating your answer.\n"
#     "2. Base your response strictly on the retrieved documents. Do not assume or hallucinate information.\n"
#     "3. Use inline bracket citations for factual claims (e.g., [1], [Source Name]).\n"
#     "4. MANDATORY: Every response must conclude with a '### Sources' section listing all referenced materials.\n\n"
#     "Output Format Requirements:\n"
#     "- If retrieved documents contain URLs, titles, or page numbers, format each source as:\n"
#     "  - [Source #]: [Document Title / URL / File Name] (Section / Page if available)\n"
#     "- If the retrieved context does not contain the answer, explicitly state: 'I could not find relevant documentation to answer this question.' and do not fabricate sources."
#     ),
#     tools=[
#         ask_vertex_retrieval,
#     ],
# )


# ----------------------- MCP -----------------------------

import logging
import os
import asyncio

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

load_dotenv()

SYSTEM_INSTRUCTION = """
You are a specialized Customer Insights & Management Assistant.
Your primary purpose is to assist users by retrieving and generating customer profile data, lifetime values, transaction history, and customer batch reports using the available customer tools (`get_random_customer`, `get_random_customer_batch`).

Guidelines:
1. Use `get_random_customer` when the user asks for details about a specific customer ID or wants a single customer profile.
2. Use `get_random_customer_batch` when the user requests a list, group, or batch of customers (with optional tier filtering like Free, Starter, Pro, Enterprise).
3. Summarize the returned JSON data into clear, user-friendly insights or markdown tables when requested.
4. You may engage in polite conversational greetings, but if the user asks about unrelated domain topics (e.g., medical advice, complex legal issues), state clearly that you specialize in Customer Insights.
"""

def create_customer_agent() -> LlmAgent:
    """Constructs the Google ADK Customer Insights Agent connected to the Customer MCP Server."""
    logger.info("--- 🔧 Loading MCP tools from Customer MCP Server... ---")
    
    # URL of your deployed Customer MCP server (or local server)
    mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:8080/mcp")
    logger.info(f"--- 🌐 Connecting to MCP Server at: {mcp_url} ---")
    
    logger.info("--- 🤖 Creating ADK Customer Agent... ---")
    return LlmAgent(
        model="gemini-2.5-flash",
        name="customer_insights_agent",
        description="An agent that retrieves customer profiles, lifetime values, and subscription insights.",
        instruction=SYSTEM_INSTRUCTION,
        tools=[
            MCPToolset(
                connection_params=StreamableHTTPConnectionParams(
                    url=mcp_url
                )
            )
        ],
    )

root_agent = create_customer_agent()

# Example runner code to test the agent locally
if __name__ == "__main__":
    from google.adk.runners import AgentRunner
    
    async def main():
        runner = AgentRunner(agent=root_agent)
        
        # Test Query 1
        prompt = "Can you give me details for customer ID CUST-992182?"
        print(f"\nUser: {prompt}")
        response = await runner.run_async(prompt)
        print(f"Agent:\n{response.text}")

        # Test Query 2
        prompt_batch = "Generate 3 random Enterprise tier customers."
        print(f"\nUser: {prompt_batch}")
        response_batch = await runner.run_async(prompt_batch)
        print(f"Agent:\n{response_batch.text}")

    asyncio.run(main())