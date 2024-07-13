import os
from dotenv import load_dotenv

from langchain_box.document_loaders import BoxFolderLoader
from langchain_box.utilities import BoxAuthType

from box_search import BoxSearch

load_dotenv("../config/.token.env")
load_dotenv("../config/.box.env")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")
box_folder_id = os.getenv("BOX_FOLDER_ID")

prompt="Summarize the scripts in this folder"

loader = BoxFolderLoader(
    auth_type=BoxAuthType.TOKEN,
    box_developer_token=box_developer_token,
    box_folder_id=box_folder_id
)
docs = loader.load()
print(f"documents {docs}")

box = BoxSearch()

box.train_ai(docs)
answer = box.box_search(prompt)

print(answer)