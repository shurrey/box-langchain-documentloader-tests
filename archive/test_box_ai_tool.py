import os
from typing import List
from dotenv import load_dotenv

from langchain_box.document_loaders import BoxLoader
from langchain_box.utilities import BoxAuth, BoxAuthType, BoxAPIWrapper, BoxSearchOptions

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


load_dotenv("../config/.jwt.env")
load_dotenv("../config/.box.env")
load_dotenv("../config/.openai.env")
load_dotenv("../config/.mongo.env")

os.environ["OPENAI_API_KEY"]
box_jwt_path = os.getenv("BOX_JWT_PATH")
box_developer_token = os.getenv("BOX_DEVELOPER_TOKEN")
mongo_password = os.getenv("MONGO_PASSWORD")

company_name = "My Fake Enterprise"
box_file_ids=["1594603535740"]

@tool
def mongo_data_tool(company_name: str):
    """
        Create a new client and connect to the server
    """

    uri = f"mongodb+srv://shurrey:{mongo_password}@langchaintest.ppgqzd9.mongodb.net/?retryWrites=true&w=majority&appName=LangchainTest"
    

    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        db = client.get_database("my_crm")

        customer = db.get_collection("customers").find_one(filter={ 'company_name': company_name})

        print(f"customers {customer}")

        return customer
    except Exception as e:
        print(e)

@tool
def box_text_tool() -> List[Document]:
    auth = BoxAuth(
        auth_type=BoxAuthType.JWT,
        box_jwt_path=box_jwt_path 
    )

    docs = BoxLoader(
        box_auth=auth,
        box_file_ids=box_file_ids
    )

    return docs

tools = [box_text_tool, mongo_data_tool]

model = ChatOpenAI(model="gpt-4")

agent_executor = create_react_agent(model, tools)

prompt = (
    f"Retrieve the company information from mongodb for {company_name}. "
    "Get the text representation of file id 1594603535740.  "
    "Then provide a report that summarizes the contracts and lists key points and gaps. "
    "The report should be in valid HTML. "
)

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=prompt)]}
):
    print(chunk)
    print("----")

response = chunk['agent']['messages'][0].content
print(f"Response : {response}")