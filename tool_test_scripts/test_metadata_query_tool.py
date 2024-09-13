import json
import os
from typing import List
from dotenv import load_dotenv

from langchain_box.document_loaders import BoxLoader
from langchain_box.utilities import BoxAuth, BoxAuthType

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent

from box_sdk_gen import BoxAPIError, BoxSDKError

load_dotenv("../config/.jwt.env")
load_dotenv("../config/.box.env")
load_dotenv("../config/.openai.env")

os.environ["OPENAI_API_KEY"]
box_jwt_path = os.getenv("BOX_JWT_PATH")
box_enterprise_id = os.getenv("BOX_ENTERPRISE_ID")
box_user_id = os.getenv("BOX_USER_ID")

@tool
def box_metadata_tool(amount: int) -> List[Document]:
    """
        Retrieve files based on a MetadataQuery search

        Takes an int argument that corresponds to the amount
        in dollars that you wish to search for documents that 
        exceed the that amount. Format of the argument should
        be an int equal to the dollar amount.
    """
    
    print(f"amount {amount}")
    amount: int = 0
    query: str = "total >= :amount and documentType = :type"
    template: str = "InvoicePO"
    params: dict[str,str] = {
        "amount" : str(amount),
        "type" : "Invoice"
    }
    print(f"params {params}")

    auth = BoxAuth(
        auth_type=BoxAuthType.JWT,
        box_jwt_path=box_jwt_path,
        box_user_id=box_user_id 
    )

    box = auth.get_client()
    
    files = []
    
    try:
        results = box.search.search_by_metadata_query(
            f"enterprise_{box_enterprise_id}.{template}",
            ancestor_folder_id="260935730128",
            query=query,
            query_params=params,
        )
        print(f"results {results}")
    except BoxAPIError as bae:
        raise RuntimeError(
            f"BoxAPIError: Error getting Metadata query results: {bae.message}"
        )
    except BoxSDKError as bse:
        raise RuntimeError(
            f"BoxSDKError: Error getting Metadata query results: {bse.message}"
        )

    for file in results.entries:
        print(f"file {file}")
        if file is not None:
            files.append(file.id)

    print(f"files {files}")
    loader = BoxLoader(box_auth=auth, box_file_ids=files)

    docs=loader.load()

    print(f"docs {docs}")

    return docs

tools = [box_metadata_tool]

model = ChatOpenAI(model="gpt-4")

agent_executor = create_react_agent(model, tools)

prompt = (
    "Get all documents that have a total value great than $100 "
    "and list all line items greater than $20 in the format "
    "\"Company name: invoice number | item | amount \""
)

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=prompt)]}
):
    print(chunk)
    print("----")

response = chunk['agent']['messages'][0].content
print(f"Response : {response}")