import os
from dotenv import load_dotenv

from langchain_community.document_loaders.box import BoxLoader, Mode
from langchain_community.utilities.box import BoxAuthType

from box_search import BoxSearch

load_dotenv("config/.ccg.env")
load_dotenv("config/.box.env")

box_client_id=os.getenv("BOX_CLIENT_ID")
box_client_secret=os.getenv("BOX_CLIENT_SECRET")
box_enterprise_id=os.getenv("BOX_ENTERPRISE_ID")
box_folder_id =os.getenv("BOX_FOLDER_ID")

prompt="YOUR_PROMPT"

loader = BoxLoader(
    mode=Mode.FOLDER,
    auth_type=BoxAuthType.CCG,
    box_client_id=box_client_id,
    box_client_secret=box_client_secret,
    box_enterprise_id=box_enterprise_id,
    box_folder_id=box_folder_id
)
docs = loader.load()

box = BoxSearch()

box.train_ai(docs)
answer = box.box_search(prompt)

print(answer)