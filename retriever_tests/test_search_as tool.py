import os
from dotenv import load_dotenv

from langchain import hub

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_box.retrievers import BoxRetriever
from langchain_box.utilities import BoxSearchOptions, DocumentFiles, SearchTypeFilter
from langchain_openai import ChatOpenAI
from langchain.tools.retriever import create_retriever_tool

load_dotenv("../config/.openai.env")
load_dotenv("../config/.token.env")
load_dotenv("../config/.box.env")

openai_key = os.getenv("OPENAI_API_KEY")
box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")
box_folder_id=os.getenv("BOX_FOLDER_ID")

query="victor"

box_search_options = BoxSearchOptions(
    ancestor_folder_ids=[box_folder_id],
    search_type_filter=[SearchTypeFilter.FILE_CONTENT],
    created_date_range=["2023-01-01T00:00:00-07:00", "2024-08-01T00:00:00-07:00,"],
    file_extensions=[DocumentFiles.DOCX, DocumentFiles.PDF],
    k=200,
    size_range=[1,1000000],
    updated_data_range=None
)

retriever = BoxRetriever( 
    box_developer_token=box_developer_token,
    box_search_options=box_search_options
)

box_search_tool = create_retriever_tool(
    retriever,
    "box_search_tool",
    "This tool is used to search Box and retrieve documents that match the search criteria"
)
tools = [box_search_tool]

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
prompt.messages

llm = ChatOpenAI(temperature=0)

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

result = agent_executor.invoke(
    {
        "input": "describe the character Victor"
    }
)

print(f"result {result['output']}")