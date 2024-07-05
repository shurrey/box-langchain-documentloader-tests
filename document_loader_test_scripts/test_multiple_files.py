import os
from dotenv import load_dotenv

from langchain_community.document_loaders.box import BoxLoader, Mode
from langchain_community.utilities.box import BoxAuthType

from box_search import BoxSearch

load_dotenv("../config/.token.env")
load_dotenv("../config/.box.env")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")
box_file_ids=[os.getenv("BOX_FIRST_FILE"),os.getenv("BOX_SECOND_FILE")]

prompt="prompt"

loader = BoxLoader(
    mode=Mode.FILES,
    auth_type=BoxAuthType.TOKEN,
    box_developer_token=box_developer_token,
    box_file_ids=box_file_ids
)
docs = loader.load()

box = BoxSearch()

box.train_ai(docs)
answer = box.box_search(prompt)

print(answer)