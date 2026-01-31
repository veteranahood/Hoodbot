import json, os
USER_FILE="user_config.json"
def save_user(user):
    with open(USER_FILE,"w") as f: json.dump(user,f)
def load_user():
    if os.path.exists(USER_FILE):
        with open(USER_FILE,"r") as f: return json.load(f)
    return None
