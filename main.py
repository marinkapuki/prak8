from fastapi import FastAPI, Response, Depends, HTTPException, Request, Form
from fastapi.security import APIKeyCookie
from typing import Optional

app = FastAPI()

# Имитация базы данных пользователей (для примера)
fake_users_db = {
    "user123": {
        "username": "user123",
        "password": "password123", 
        "profile": {"email": "user123@example.com", "role": "user"}
    }
}

# Настройка cookie-аутентификации
cookie_scheme = APIKeyCookie(name="session_token", auto_error=False)

# Генерация уникального токена (упрощённый пример)
def generate_session_token() -> str:
    return "abc123xyz456"  

# Проверка валидности токена
async def get_current_user(session_token: Optional[str] = Depends(cookie_scheme)):
    if session_token != "abc123xyz456":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return fake_users_db["user123"]  # Возвращаем данные пользователя
