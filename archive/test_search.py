import os
from dotenv import load_dotenv

from langchain_box.document_loaders import BoxSearchLoader
from langchain_box.utilities import BoxAuthType

from box_search import BoxSearch

load_dotenv("../config/.jwt.env")
load_dotenv("../config/.box.env")

box_jwt_path=os.getenv("BOX_JWT_PATH")
box_user_id=os.getenv("BOX_USER_ID")
box_search_query=os.getenv("BOX_SEARCH_QUERY")

prompt="Summarize Five feet and rising"

loader = BoxSearchLoader( 
    auth_type=BoxAuthType.JWT,
    box_jwt_path=box_jwt_path,
    box_user_id=box_user_id,
    box_search_query=box_search_query
)
documents = loader.load()

#print(f"documents = {documents}")

box = BoxSearch()

box.train_ai(documents)
answer = box.box_search(prompt)

print(answer)