import os
import json
import socket
import requests
import webbrowser
import threading
from flask import Flask, request
from github import Github
from werkzeug.serving import make_server


def run_github_auth():
    CLIENT_ID = "Ov23licaYaAFmAgwN3p0"
    CLIENT_SECRET = "d2af713c5f91e70882f73c2b33d20c35229f6d4a"
    REDIRECT_URI = "http://localhost:8000/callback"
    TOKEN_FILE = "token.json"

    app = Flask(__name__)
    token_data = {"access_token": None}
    done_event = threading.Event()

    def save_token(token: str):
        with open(TOKEN_FILE, "w") as f:
            json.dump({"access_token": token}, f)

    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    auth_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=repo"
    )

    class Server:
        def __init__(self, app):
            self.srv = make_server("127.0.0.1", 8000, app)
            self.ctx = app.app_context()
            self.ctx.push()

        def serve_forever(self):
            self.srv.serve_forever()

        def shutdown(self):
            self.srv.shutdown()

    server = Server(app)

    @app.route("/callback")
    def callback():
        code = request.args.get("code")
        r = requests.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
            headers={"Accept": "application/json"},
        )
        token = r.json().get("access_token")
        if token:
            token_data["access_token"] = token
            save_token(token)

            g = Github(token)
            user = g.get_user()
            for repo in user.get_repos():
                print(f"{repo.name} -> {repo.clone_url}")

        done_event.set()
        threading.Thread(target=server.shutdown).start()
        return "Авторизация прошла успешно! Можно закрыть это окно."

    flask_thread = threading.Thread(target=server.serve_forever)
    flask_thread.start()

    try:
        if webbrowser.get():
            webbrowser.open(auth_url)
            print("Открываем браузер для авторизации...")
    except webbrowser.Error:
        local_ip = get_local_ip()
        print("Не удалось открыть браузер автоматически.")
        print(f"Откройте ссылку вручную: {auth_url}")
        print(f"Если вы в сети: http://{local_ip}:8000/callback")

    done_event.wait()
    flask_thread.join()

    return token_data["access_token"]


if __name__ == "__main__":
    token = run_github_auth()
    print("Полученный токен:", token)
