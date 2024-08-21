import os
from dotenv import load_dotenv

from langchain_box.document_loaders import BoxLoader

from box_search import BoxSearch

load_dotenv("../config/.token.env")
load_dotenv("../config/.box.env")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")
box_file_ids=[os.getenv("BOX_FIRST_FILE")]

prompt="Summarize these documents"

loader = BoxLoader( 
    box_developer_token=box_developer_token,
    box_file_ids=box_file_ids,
    character_limit=10
)

documents = loader.lazy_load()

print(f"documents {list(documents)}")