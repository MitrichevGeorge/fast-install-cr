import json
from pathlib import Path
from GHOAuth import run_github_auth
from prompt_toolkit.shortcuts import button_dialog, radiolist_dialog
from github import Github, Auth

TOKEN_FILE = Path.home() / ".config" / "myapp" / "token.json"
TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)

def bad_token(token):
    try:
        g = Github(auth=Auth.Token(token))
        g.get_user().login
        return False
    except:
        return True

def save_token(token_data):
    with open(TOKEN_FILE, "w") as f:
        json.dump({"access_token": token_data}, f)

def load_token():
    if not TOKEN_FILE.exists():
        return None
    with open(TOKEN_FILE, "r") as f:
        return json.load(f)["access_token"]
    
def main():
    token = load_token()
    if (token is None) or bad_token(token):
        token = run_github_auth()
        save_token(token)

    

if __name__ == "__main__":
    main()