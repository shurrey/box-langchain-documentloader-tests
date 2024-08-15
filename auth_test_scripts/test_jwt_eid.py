import os
from dotenv import load_dotenv

from langchain_box.document_loaders import BoxLoader
from langchain_box.utilities import BoxAuth, BoxAuthType

load_dotenv("../config/.jwt.env")
load_dotenv("../config/.box.env")

box_jwt_path=os.getenv("BOX_JWT_PATH")
box_file_ids=[os.getenv("BOX_FIRST_FILE")]

prompt="Summarize these documents"

auth = BoxAuth(
    auth_type=BoxAuthType.JWT,
    box_jwt_path=box_jwt_path
)

loader = BoxLoader( 
    box_auth=auth,
    box_file_ids=box_file_ids
)

documents = loader.load()

print(f"document {documents}")