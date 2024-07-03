import os
from dotenv import load_dotenv

from langchain_community.document_loaders.box import BoxLoader, Mode, AuthType

from box_search import BoxSearch

load_dotenv("config/.token.env")
load_dotenv("config/.box.env")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")
box_file_ids=[os.getenv("BOX_FIRST_FILE")]

prompt="Show me all of victor's lines"

loader = BoxLoader( 
    mode=Mode.FILES,
    auth_type=AuthType.TOKEN,
    box_developer_token=box_developer_token,
    box_file_ids=box_file_ids
)
documents = loader.load()

box = BoxSearch()

box.train_ai(documents)
answer = box.box_search(prompt)

print(answer)