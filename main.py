from fastapi import FastAPI, Response, Depends, HTTPException, Request, Form
from fastapi.security import APIKeyCookie
from typing import Optional

app = FastAPI()

# Имитация базы данных пользователей
fake_users_db = {
    "user123": {
        "username": "user123",
        "password": "password123",  # Хэшируйте пароли в реальном проекте!
        "profile": {"email": "user123@example.com", "role": "user"}
    }
}

cookie_scheme = APIKeyCookie(name="session_token", auto_error=False)

def generate_session_token() -> str:
    return "abc123xyz456"  # Используйте UUID или JWT в реальном приложении.

# Проверка токена
async def get_current_user(session_token: Optional[str] = Depends(cookie_scheme)):
    if session_token != generate_session_token():
        raise HTTPException(
            status_code=401,
            detail={"message": "Unauthorized"}  # Формат ошибки из задания
        )
    return fake_users_db["user123"]

@app.post("/login")
async def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...)
):
    user = fake_users_db.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    response.set_cookie(
        key="session_token",
        value=generate_session_token(),
        secure=True,
        httponly=True,
        samesite="lax",
        max_age=3600
    )
    return {"message": "Login successful"}

@app.get("/user")
async def get_user_profile(user: dict = Depends(get_current_user)):
    return {
        "username": user["username"],
        "email": user["profile"]["email"],
        "role": user["profile"]["role"]
    }

