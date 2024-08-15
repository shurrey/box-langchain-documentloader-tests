import os
from dotenv import load_dotenv

from box_sdk_gen import (
    BoxClient,
    BoxAPIError,
    BoxSDKError,
    BoxDeveloperTokenAuth,
    FileBaseTypeField
)

load_dotenv("config/.token.env")
load_dotenv("config/.box.env")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")
box_folder_id = os.getenv("BOX_FOLDER_ID")

try:
    auth = BoxDeveloperTokenAuth(token=box_developer_token)
    box = BoxClient(auth=auth)

    print("call sdk")
    folder_contents = box.folders.get_folder_items(
        box_folder_id, fields=["id", "type"]
    )

    print(f"folder_content {folder_contents}")
    for file in folder_contents.entries:
        print(f"file {file} file.type {file.type} file.type.value() {file.type.value()}")

        print(f"file.type == FileBaseTypeField.FILE {file.type == FileBaseTypeField.FILE}")

except BoxAPIError as bae:
    raise RuntimeError(
        f"BoxAPIError: Error getting folder content: {bae.message}"
    )
except BoxSDKError as bse:
    raise RuntimeError(
        f"BoxSDKError: Error getting folder content: {bse.message}"
    )
except Exception as e:
    raise RuntimeError(
        f"Exception: Error getting folder content: {e}"
    )

print("return")