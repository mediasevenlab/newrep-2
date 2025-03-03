from fastapi import FastAPI
import requests
import base64
import os

app = FastAPI()

GITHUB_TOKEN = os.getenv("GH_TOKEN")  
GITHUB_USERNAME = "mediasevenlab"
REPO_NAME = "newrep-1"
BASE_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents"

def upload_file(filename, content):
    file_url = f"{BASE_URL}/{filename}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {
        "message": f"Обновлён {filename} через API",
        "content": base64.b64encode(content.encode()).decode(),
        "sha": None
    }
    return requests.put(file_url, headers=headers, json=data).json()

@app.post("/create-file")
async def create_file(filename: str, content: str):
    return upload_file(filename, content)
