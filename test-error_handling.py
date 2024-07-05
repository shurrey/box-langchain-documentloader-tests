import os
from dotenv import load_dotenv

from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth, BoxSDKError

load_dotenv("config/.token.env")
load_dotenv("config/.box.env")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")
box_search_query=os.getenv("BOX_SEARCH_QUERY")
                    
try:
    auth = BoxDeveloperTokenAuth(token=box_developer_token)
    box_client = BoxClient(auth=auth)

    me = box_client.users.get_user_me()
    print(f"My user ID is {me.id}")
except BoxSDKError as bse:
    print(f"BoxSDKError: {bse.message}")