import os
from dotenv import load_dotenv

from langchain_box.document_loaders import BoxFolderLoader
from langchain_box.utilities import BoxAuthType

from box_search import BoxSearch

load_dotenv("../config/.ccg.env")
load_dotenv("../config/.box.env")

box_client_id=os.getenv("BOX_CLIENT_ID")
box_client_secret=os.getenv("BOX_CLIENT_SECRET")
box_user_id=os.getenv("BOX_USER_ID")
box_folder_id =os.getenv("BOX_FOLDER_ID")

prompt="YOUR_PROMPT"

loader = BoxFolderLoader(
    auth_type=BoxAuthType.CCG,
    box_client_id=box_client_id,
    box_client_secret=box_client_secret,
    box_user_id=box_user_id,
    box_folder_id=box_folder_id
)
docs = loader.load()

box = BoxSearch()

box.train_ai(docs)
answer = box.box_search(prompt)

print(answer)