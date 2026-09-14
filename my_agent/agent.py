from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="gemini-2.5-flash",
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)



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


