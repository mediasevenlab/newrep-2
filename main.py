from fastapi import FastAPI
from pydantic import BaseModel
import requests
import base64
import os

app = FastAPI()

# 🔑 Используем токен из переменных окружения Render
GITHUB_TOKEN = os.getenv("GH_TOKEN")  
GITHUB_USERNAME = "mediasevenlab"
REPO_NAME = "newrep-2"
BASE_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents"

# 📌 Создаём Pydantic-модель для запроса
class FileRequest(BaseModel):
    filename: str
    content: str

def upload_file(filename, content):
    """Создаёт или обновляет файл в GitHub"""
    file_url = f"{BASE_URL}/{filename}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {
        "message": f"Обновлён {filename} через API",
        "content": base64.b64encode(content.encode()).decode(),
        "sha": None
    }
    return requests.put(file_url, headers=headers, json=data).json()

@app.post("/create-file")
async def create_file(request: FileRequest):
    """Обрабатывает запрос и загружает файл в GitHub"""
    return upload_file(request.filename, request.content)
