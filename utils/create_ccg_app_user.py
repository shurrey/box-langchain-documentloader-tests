import os
from dotenv import load_dotenv

from box_sdk_gen import (
    BoxClient,
    BoxCCGAuth,
    CCGConfig,
    CreateCollaborationItem,
    CreateCollaborationItemTypeField,
    CreateCollaborationAccessibleBy,
    CreateCollaborationAccessibleByTypeField,
    CreateCollaborationRole
)

load_dotenv("../config/.ccg.env")
load_dotenv("../config/.box.env")

box_client_id=os.getenv("BOX_CLIENT_ID")
box_client_secret=os.getenv("BOX_CLIENT_SECRET")
box_enterprise_id=os.getenv("BOX_ENTERPRISE_ID")
box_folder_id =os.getenv("BOX_FOLDER_ID")

try:
    ccg_config = CCGConfig(
        client_id=box_client_id,
        client_secret=box_client_secret,
        enterprise_id=box_enterprise_id
    )

    auth = BoxCCGAuth(config=ccg_config)
    box = BoxClient(auth=auth)

    user = box.users.create_user("langchain-integration-test", is_platform_access_only=True)

    print(f"User: {user}")

    box.user_collaborations.create_collaboration(
    CreateCollaborationItem(
        type=CreateCollaborationItemTypeField.FOLDER.value, id=box_folder_id
    ),
    CreateCollaborationAccessibleBy(
        type=CreateCollaborationAccessibleByTypeField.USER.value,
        id=user.id,
    ),
    CreateCollaborationRole.EDITOR.value,
)
except Exception as ex:
    print (f"Exception: {ex}")