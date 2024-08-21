import os
from dotenv import load_dotenv

from langchain_box.document_loaders import BoxLoader
from langchain_box.utilities import BoxAuth, BoxAuthType

load_dotenv("../config/.token.env")
load_dotenv("../config/.box.env")

os.environ["BOX_DEVELOPER_TOKEN"] = os.getenv("BOX_DEVELOPER_TOKEN")
box_file_ids=[os.getenv("BOX_FIRST_FILE")]

prompt="Summarize these documents"

loader = BoxLoader( 
    box_file_ids=box_file_ids
)

documents = loader.load()

print(f"document {documents}")