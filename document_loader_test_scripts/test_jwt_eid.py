import os
from dotenv import load_dotenv

from langchain_box.document_loaders import BoxFolderLoader
from langchain_box.utilities import BoxAuthType

from box_search import BoxSearch

load_dotenv("../config/.jwt.env")
load_dotenv("../config/.box.env")

box_jwt_path=os.getenv("BOX_JWT_PATH")
box_folder_id = os.getenv("BOX_FOLDER_ID")

prompt="YOUR_PROMPT"

loader = BoxFolderLoader(
    auth_type=BoxAuthType.JWT,
    box_jwt_path=box_jwt_path,
    box_folder_id=box_folder_id
)
docs = loader.load()

box = BoxSearch()

box.train_ai(docs)
answer = box.box_search(prompt)

print(answer)