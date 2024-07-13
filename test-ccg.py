import os
import dotenv
from box_sdk_gen import CCGConfig, BoxCCGAuth, BoxClient, BoxAPIError, BoxSDKError

def env():
    dotenv.load_dotenv('config/.ccg.env')
    dotenv.load_dotenv('config/.box.env')
    return {
        "client_id": os.getenv("BOX_CLIENT_ID"),
        "client_secret": os.getenv("BOX_CLIENT_SECRET"),
        "enterprise_id": os.getenv("BOX_ENTERPRISE_ID"),
        "user_id": os.getenv("BOX_USER_ID"),
    }



env_vars = env()
print(f"env_vars {env_vars}")
ccg_conf = CCGConfig(
    client_id=env_vars["client_id"],
    client_secret=env_vars["client_secret"],
    # enterprise_id=env_vars["enterprise_id"],
    user_id=env_vars["user_id"],
)
print(f"ccg_conf {ccg_conf}")
auth = BoxCCGAuth(ccg_conf)
print(f"auth {auth}")
client = BoxClient(auth)
print(f"client {client}")
try:
    me = client.users.get_user_me()
    print(f"Current user: {me.name} {me.login} {me.id}")
except BoxAPIError as e:
    print(f"BoxAPIError: {e}")
except BoxSDKError as e:
    print(f"BoxSDKError: {e}")