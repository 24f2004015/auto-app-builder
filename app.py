# app.py
from flask import Flask, request, jsonify
import os
import threading
from utils import verify_secret, post_with_retry, generate_task_id
from generator import generate_app
from deploy import create_github_repo, deploy_pages

app = Flask(__name__)
GITHUB_TOKEN = os.getenv("GITHUB_PAT")

def handle_task_async(data):
    task_id = generate_task_id(data["task"], data["round"])
    # Generate app
    code_files = generate_app(data["brief"], data.get("attachments", []))
    # Create GitHub repo
    repo_url, commit_sha = create_github_repo(task_id, code_files, GITHUB_TOKEN)
    # Deploy Pages
    pages_url = deploy_pages(task_id, GITHUB_TOKEN)
    # Send to evaluation_url
    payload = {
        "email": data["email"],
        "task": data["task"],
        "round": data["round"],
        "nonce": data["nonce"],
        "repo_url": repo_url,
        "commit_sha": commit_sha,
        "pages_url": pages_url
    }
    post_with_retry(data["evaluation_url"], payload)

@app.route("/api-endpoint", methods=["POST"])
def receive_task():
    data = request.get_json()
    if not verify_secret(data.get("secret")):
        return jsonify({"error": "Invalid secret"}), 403

    # Respond 200 immediately
    threading.Thread(target=handle_task_async, args=(data,)).start()
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

