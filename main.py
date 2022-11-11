from fastapi import FastAPI, File, UploadFile, Header
from math import sqrt
from fastapi.responses import StreamingResponse
from PIL import Image, ImageOps
from io import BytesIO
from datetime import datetime
from pydantic import BaseModel
import uvicorn
from os import environ

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Witaj Magda"}


@app.get("/prime/{number}")
async def type_number(number: int):
    n = number
    if (n > 1) and (n <= 9223372036854775807):
        end = int(sqrt(n)) + 1
        if n == 2: end = int(sqrt(n)) + 2
        if n == 3: end = int(sqrt(n)) + 2
        for i in range(2, end):
            if (n % i == 0) and (n != i):
                return {f"Liczba {n} nie jest pierwsza"}
                break
            else:
                return {f"Liczba {n} jest pierwsza"}
    else:
        return {f"Liczba {n} jest z poza zakresu"}


@app.post("/picture/invert")
async def invert_picture(img: UploadFile = File(...)):
    original_image = Image.open(img.file)
    image_invert = ImageOps.invert(original_image)

    filtered_image = BytesIO()
    image_invert.save(filtered_image, "JPEG")
    filtered_image.seek(0)

    return StreamingResponse(filtered_image, media_type="image/jpeg")


users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "fakehashedsecret"
    }
}


def fake_hash_password(password: str):
    return "fakehashed" + password


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(users_db, token)
    return user


def authenticate_user(fake_db, username: str, password: str) -> bool:
    user = get_user(fake_db, username)
    if not user:
        return False
    if not fake_hash_password(password):
        return False
    return user


@app.get("/users/me")
async def read_users_me(username: str | None = Header(default=None), password: str | None = Header(default=None)):
    if authenticate_user(users_db, username, password):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return {current_time}
    else:
        return {"Niepoprawne dane autoryzacyjne"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=environ.get("PORT", 5000))
