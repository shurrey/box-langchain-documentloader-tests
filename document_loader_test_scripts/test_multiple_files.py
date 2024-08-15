import os
from dotenv import load_dotenv

from langchain_box.document_loaders import BoxLoader

from box_search import BoxSearch

load_dotenv("../config/.token.env")
load_dotenv("../config/.box.env")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")
box_file_ids=[os.getenv("BOX_FIRST_FILE"),os.getenv("BOX_SECOND_FILE")]

prompt="summarize these documents"

loader = BoxLoader(
    box_developer_token=box_developer_token,
    box_file_ids=box_file_ids
)
docs = loader.lazy_load()

box = BoxSearch()

box.train_ai(docs)
answer = box.box_search(prompt)

print(answer)