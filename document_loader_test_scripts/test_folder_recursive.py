import os
from dotenv import load_dotenv

from langchain_box.document_loaders import BoxLoader

from box_search import BoxSearch

load_dotenv("../config/.token.env")
load_dotenv("../config/.box.env")
load_dotenv("../config/.tesseract.env")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")
box_folder_id = "0"

os.environ["PATH"] += os.pathsep + os.getenv("TESSERACT_PATH")

prompt="summarize all"

loader = BoxLoader(
    box_developer_token=box_developer_token,
    box_folder_id=box_folder_id,
    recursive=True,
    get_images=True
)
docs = loader.lazy_load()

print(f"docs {docs}")
box = BoxSearch()

box.train_ai(docs)
answer = box.box_search(prompt)

print(answer)