import os
from dotenv import load_dotenv

from langchain_box.document_loaders import BoxLoader
from langchain_box.utilities import BoxAuth, BoxAuthType

load_dotenv("../config/.ccg.env")
load_dotenv("../config/.box.env")

box_client_id=os.getenv("BOX_CLIENT_ID")
box_client_secret=os.getenv("BOX_CLIENT_SECRET")
box_user_id=os.getenv("BOX_USER_ID")
box_file_ids=[os.getenv("BOX_FIRST_FILE")]

prompt="Summarize these documents"

auth = BoxAuth(
    auth_type=BoxAuthType.CCG,
    box_client_id=box_client_id,
    box_client_secret=box_client_secret,
    box_user_id=box_user_id
)

loader = BoxLoader( 
    box_auth=auth,
    box_file_ids=box_file_ids
)

documents = loader.load()

print(f"document {documents}")