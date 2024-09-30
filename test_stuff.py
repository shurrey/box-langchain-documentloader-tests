import os
from dotenv import load_dotenv

from box_sdk_gen import (
    BoxClient,
    BoxAPIError,
    BoxSDKError,
    CCGConfig,
    BoxCCGAuth,
    CreateAiAskMode,
    AiItemBase,
    AiItemBaseTypeField,
    FileBaseTypeField
)

load_dotenv("config/.ccg.env")
load_dotenv("config/.box.env")

box_client_id=os.getenv("BOX_CLIENT_ID")
box_client_secret=os.getenv("BOX_CLIENT_SECRET")
box_user_id = os.getenv("BOX_USER_ID")
box_file_id = os.getenv("BOX_FIRST_FILE")



ccg_config = CCGConfig(
    client_id=box_client_id,
    client_secret=box_client_secret,
    user_id=box_user_id,
)
auth = BoxCCGAuth(config=ccg_config)

box = BoxClient(auth=auth)

ai_mode = CreateAiAskMode.SINGLE_ITEM_QA.value

items = []

item = AiItemBase(
            id="1594603535740",
            type=AiItemBaseTypeField.FILE.value
        )

items.append(item)

response = box.ai.create_ai_ask(mode=ai_mode, prompt="summarize this file", items=items, include_citations=True)

answer = response.answer
citations = response.citations

for citation in citations:
    content = citation.content
    name = citation.name
    id = citation.id
    type = citation.type.value

    print("+-------------------------------------------------------------------")
    print(f"| name: {name}")
    print(f"| id: {id}")
    print(f"| type: {type}")
    print("+-------------------------------------------------------------------")
    print(f"{content}")
    print("+-------------------------------------------------------------------\n\n\n")

print(f"{answer}")