import os
from dotenv import load_dotenv

from langchain_box.document_loaders import BoxMetadataQueryLoader
from langchain_box.utilities.box_auth import BoxAuthType

from box_search import BoxSearch

load_dotenv("../config/.token.env")
load_dotenv("../config/.box.env")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")
box_metadata_template=os.getenv("BOX_METADATA_TEMPLATE")
box_metadata_query=os.getenv("BOX_METADATA_QUERY")
box_metadata_params=os.getenv("BOX_METADATA_PARAMS")
box_enterprise_id=os.getenv("BOX_ENTERPRISE_ID")

prompt="show me what was purchased"

loader = BoxMetadataQueryLoader( 
    auth_type=BoxAuthType.TOKEN,
    box_developer_token=box_developer_token,
    box_metadata_query=box_metadata_query,
    box_metadata_template=box_metadata_template,
    box_metadata_params=box_metadata_params,
    box_enterprise_id=box_enterprise_id
)
documents = loader.load()

print(f"documents = {documents}")

box = BoxSearch()

box.train_ai(documents)
answer = box.box_search(prompt)

print(answer)