from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import base64
import os

app = FastAPI()

# 🔑 Используем GitHub-токен из переменных окружения Render
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

@app.post("/create-file")
async def create_file(request: FileRequest):
    """Создаёт или обновляет файл в GitHub"""
    file_url = f"{BASE_URL}/{request.filename}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    # Проверяем, существует ли файл, чтобы получить его SHA
    sha = get_file_sha(request.filename)

    data = {
        "message": f"Обновлён {request.filename} через API",
        "content": base64.b64encode(request.content.encode()).decode(),
        "sha": sha  # Если файл есть, он будет обновлён
    }

    response = requests.put(file_url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        return {"message": f"✅ Файл '{request.filename}' успешно создан/обновлён!"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

@app.delete("/delete-file")
async def delete_file(filename: str):
    """Удаляет файл из GitHub"""
    sha = get_file_sha(filename)
    if not sha:
        raise HTTPException(status_code=404, detail="❌ Файл не найден")

    file_url = f"{BASE_URL}/{filename}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {
        "message": f"Удалён {filename} через API",
        "sha": sha
    }

    response = requests.delete(file_url, headers=headers, json=data)
    
    if response.status_code == 200:
        return {"message": f"✅ Файл '{filename}' успешно удалён!"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))  # Render может передавать порт через переменную окружения
    uvicorn.run(app, host="0.0.0.0", port=port)
