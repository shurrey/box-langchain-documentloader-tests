import os
from dotenv import load_dotenv

from langchain_box.document_loaders import BoxAILoader, BoxAIMode
from langchain_box.utilities import BoxAuthType

from box_search import BoxSearch

load_dotenv("../config/.token.env")
load_dotenv("../config/.box.env")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")
box_file_ids = [os.getenv("BOX_FIRST_FILE"),os.getenv("BOX_SECOND_FILE")]
box_ai_prompt=os.getenv("BOX_AI_PROMPT")

prompt="list all the characters for each script"

loader = BoxAILoader( 
    mode=BoxAIMode.ASK,
    auth_type=BoxAuthType.TOKEN,
    box_developer_token=box_developer_token,
    box_file_ids=box_file_ids,
    box_ai_prompt=box_ai_prompt
)
documents = loader.load()

print(f"documents = {documents}")

box = BoxSearch()

box.train_ai(documents)
answer = box.box_search(prompt)

print(answer)