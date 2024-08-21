import os
from dotenv import load_dotenv

from langchain_box.retrievers import BoxRetriever


load_dotenv("../config/.token.env")
load_dotenv("../config/.box.env")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")
box_file_ids = [os.getenv("BOX_FIRST_FILE")]
box_ai_prompt=os.getenv("BOX_AI_PROMPT")

prompt="List all the props"

retriever = BoxRetriever( 
    box_developer_token=box_developer_token,
    box_file_ids=box_file_ids
)

documents = retriever.invoke(prompt)

print(f"documents = {documents}")