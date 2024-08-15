import os
from dotenv import load_dotenv

from langchain_box.tools import BoxAIAskTool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent


load_dotenv("../config/.token.env")
load_dotenv("../config/.box.env")
load_dotenv("../config/.openai.env")

os.environ["OPENAI_API_KEY"]
os.environ["BOX_DEVELOPER_TOKEN"]
box_developer_token = os.getenv("BOX_DEVELOPER_TOKEN")
box_file_ids=[os.getenv("BOX_FIRST_FILE")]

box_ai_tool = BoxAIAskTool(box_developer_token=box_developer_token, box_file_ids=box_file_ids)

tools = [box_ai_tool]

model = ChatOpenAI(model="gpt-4")

agent_executor = create_react_agent(model, tools)

prompt = (
    f"Summarize the script with Box. Based on the summary, create a script for a voiceover based "
     "on the document for a 30 second commercial. The content of this commercial should entice a "
     "viewer to want to see the movie. The voice should be that of a professional voice over actor, "
     "and the tone should be excited."
)

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=prompt)]}
):
    print(chunk)
    print("----")