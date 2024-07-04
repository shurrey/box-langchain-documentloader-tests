import os
from dotenv import load_dotenv

from langchain_community.document_loaders.box import BoxLoader, Mode
from langchain_community.utilities.box import BoxAuthType

from box_search import BoxSearch

load_dotenv("config/.jwt.env")
load_dotenv("config/.box.env")

box_jwt_path=os.getenv("BOX_JWT_PATH")
box_folder_id = os.getenv("BOX_FOLDER_ID")
box_user_id=os.getenv("BOX_USER_ID")

prompt="YOUR_PROMPT"

loader = BoxLoader(
    mode=Mode.FOLDER,
    auth_type=BoxAuthType.JWT,
    box_jwt_path=box_jwt_path,
    box_user_id=box_user_id,
    box_folder_id=box_folder_id
)
docs = loader.load()

box = BoxSearch()

box.train_ai(docs)
answer = box.box_search(prompt)

print(answer)