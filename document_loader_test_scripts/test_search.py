import os
from dotenv import load_dotenv

from langchain_box.document_loaders import BoxSearchLoader
from langchain_box.utilities import BoxAuthType

from box_search import BoxSearch

load_dotenv("../config/.token.env")
load_dotenv("../config/.box.env")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")
box_search_query=os.getenv("BOX_SEARCH_QUERY")

prompt="Summarize Five feet and rising"

loader = BoxSearchLoader( 
    auth_type=BoxAuthType.TOKEN,
    box_developer_token=box_developer_token,
    box_search_query=box_search_query
)
documents = loader.load()

#print(f"documents = {documents}")

box = BoxSearch()

box.train_ai(documents)
answer = box.box_search(prompt)

print(answer)