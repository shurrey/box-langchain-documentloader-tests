import os
from dotenv import load_dotenv

from langchain_community.document_loaders.box import BoxLoader, Mode
from langchain_community.utilities.box import BoxAuthType

from box_search import BoxSearch

load_dotenv("config/.token.env")
load_dotenv("config/.box.env")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")
box_folder_id = os.getenv("BOX_FOLDER_ID")

prompt="Summarize the scripts in this folder"

loader = BoxLoader(
    mode=Mode.FOLDER,
    auth_type=BoxAuthType.TOKEN,
    box_developer_token=box_developer_token,
    box_folder_id=box_folder_id
)
docs = loader.load()

box = BoxSearch()

box.train_ai(docs)
answer = box.box_search(prompt)

print(answer)