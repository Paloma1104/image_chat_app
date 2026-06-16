from fastapi import FastAPI
import os
from fastapi import UploadFile, File

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from FastAPI"}

@app.get("/images")
def list_images():
    if not os.path.exists("uploads"):
        return []

    return os.listdir("uploads")

@app.post("/images")
async def upload_image( file: UploadFile = File(...)):
    contents = await file.read()

    with open(
        f"uploads/{file.filename}",
        "wb"
    ) as buffer:
        buffer.write(contents)

    return {
        "filename": file.filename
    }