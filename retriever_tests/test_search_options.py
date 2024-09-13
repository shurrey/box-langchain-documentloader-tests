import os
from dotenv import load_dotenv

from langchain_box.retrievers import BoxRetriever
from langchain_box.utilities import BoxSearchOptions, DocumentFiles, SearchTypeFilter

load_dotenv("../config/.token.env")
load_dotenv("../config/.box.env")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")
box_folder_id=os.getenv("BOX_FOLDER_ID")

query="victor"

box_search_options = BoxSearchOptions(
    ancestor_folder_ids=[box_folder_id],
    search_type_filter=[SearchTypeFilter.FILE_CONTENT],
    created_date_range=["2023-01-01T00:00:00-07:00", "2024-08-01T00:00:00-07:00,"],
    file_extensions=[DocumentFiles.DOCX, DocumentFiles.PDF],
    k=200,
    size_range=[1,1000000],
    updated_data_range=None
)

retriever = BoxRetriever( 
    box_developer_token=box_developer_token,
    box_search_options=box_search_options
)

documents = retriever.invoke(query)

print(f"documents = {documents}")