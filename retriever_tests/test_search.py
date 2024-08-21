import os
from dotenv import load_dotenv

from langchain_box.retrievers import BoxRetriever

load_dotenv("../config/.token.env")
load_dotenv("../config/.box.env")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")

query="victor"

retriever = BoxRetriever( 
    box_developer_token=box_developer_token
)

documents = retriever.invoke(query)

print(f"documents = {documents}")