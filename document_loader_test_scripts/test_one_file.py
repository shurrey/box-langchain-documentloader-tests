import os
from dotenv import load_dotenv

from langchain_box.document_loaders import BoxFileLoader
from langchain_box.utilities.box_auth import BoxAuthType

from box_search import BoxSearch

load_dotenv("../config/.token.env")
load_dotenv("../config/.box.env")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")
box_file_ids=[os.getenv("BOX_FIRST_FILE")]

prompt="Summarize these documents"

loader = BoxFileLoader( 
    auth_type=BoxAuthType.TOKEN,
    box_developer_token=box_developer_token,
    box_file_ids=box_file_ids
)
documents = loader.load()

box = BoxSearch()

box.train_ai(documents)
answer = box.box_search(prompt)

print(answer)