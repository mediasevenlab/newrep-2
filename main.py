from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import base64
import os

app = FastAPI()

# 🔑 Используем токен из Render Environment Variables
GITHUB_TOKEN = os.getenv("GH_TOKEN")  
GITHUB_USERNAME = "mediasevenlab"
REPO_NAME = "newrep-2"
BASE_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents"

class FileRequest(BaseModel):
    filename: str
    content: str

def get_file_sha(filename):
    """Получает SHA файла перед удалением"""
    file_url = f"{BASE_URL}/{filename}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(file_url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("sha")
    return None

@app.delete("/delete-file")
async def delete_file(filename: str):
    """Удаляет файл из репозитория"""
    sha = get_file_sha(filename)
    if not sha:
        raise HTTPException(status_code=404, detail="Файл не найден")

    file_url = f"{BASE_URL}/{filename}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {
        "message": f"Удалён {filename} через API",
        "sha": sha
    }

    response = requests.delete(file_url, headers=headers, json=data)
    
    if response.status_code == 200:
        return {"message": f"✅ Файл {filename} успешно удалён!"}
    else:
        return {"error": response.json()}

