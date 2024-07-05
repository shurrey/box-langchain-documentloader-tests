# Import relevant functionality
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.tools.box.box_file_search import BoxFileSearchTool
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import create_react_agent


load_dotenv("config/.token.env")
load_dotenv("config/.box.env")
load_dotenv("config/.openai.env")

openai_key = os.getenv("OPENAI_API_KEY")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")
box_search_query=os.getenv("BOX_SEARCH_QUERY")

# Create the agent
memory = SqliteSaver.from_conn_string(":memory:")
model = ChatOpenAI(model="gpt-3.5-turbo-0125")
search = BoxFileSearchTool(box_developer_token=box_developer_token)
tools = [search]
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content={box_search_query})]}, config
):
    print(chunk)
    print("----")

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="Show me all of victor's lines")]}, config
):
    print(chunk)
    print("----")

