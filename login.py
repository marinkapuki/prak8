from fastapi import FastAPI, Response, HTTPException, Form
from fastapi.security import APIKeyCookie

app = FastAPI()
cookie_scheme = APIKeyCookie(name="session_token", auto_error=False)

@app.post("/login")
async def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...)
):
    if username != "user123" or password != "password123":
        raise HTTPException(status_code=400, detail="Invalid credentials")

    response.set_cookie(
        key="session_token",
        value="abc123xyz456",
        secure=True,
        httponly=True,
        samesite="lax",
        max_age=3600
    )
    return {"message": "Login successful"}

