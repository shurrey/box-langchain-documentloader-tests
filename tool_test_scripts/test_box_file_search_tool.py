import os
from dotenv import load_dotenv

from langchain_community.tools.box.box_file_search import BoxFileSearchTool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent

load_dotenv("../config/.token.env")
load_dotenv("../config/.box.env")
load_dotenv("../config/.openai.env")

os.environ["OPENAI_API_KEY"]
os.environ["BOX_DEVELOPER_TOKEN"]
box_search_query=os.getenv("BOX_SEARCH_QUERY")

box_search_tool = BoxFileSearchTool()

tools = [box_search_tool]

model = ChatOpenAI(model="gpt-4")

agent_executor = create_react_agent(model, tools)

prompt = (
    f"find a document containing the {box_search_query}. If there are multiple documents returned,"
     "choose only the first one. Then create a script for a voiceover based on the document for a 30"
     "second commercial. The content of this commercial should entice a viewer to want to see the movie."
     "The voice should be that of a professional voice over actor, and the tone should be excited."
)

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=prompt)]}
):
    print(chunk)
    print("----")