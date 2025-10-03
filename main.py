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

    g = Github(auth=Auth.Token(token))
    opt = [(1, "Использовать существующий репозиторий"), (2, "Создать новый репозиторий"), (3, "Выйти")]
    q = button_dialog(title = "Генератор установочных .sh", text = f"Вы вошли в github как {g.get_user().name}", buttons=opt)
    if q == 1:
        sel = radiolist_dialog(title="выберите репозиторий", values=[(i.name, i.name) for i in g.get_user().get_repos()]).run()
        

if __name__ == "__main__":
    main()