from fastapi import FastAPI
import os
from fastapi import UploadFile, File

os.makedirs("uploads", exist_ok=True)
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

    file_path = os.path.join("uploads", file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    return {
        "filename": file.filename
    }

@app.get("/images/{filename}")
def get_image(filename: str):

    file_path = os.path.join("uploads", filename)

    return {
        "filename": filename,
        "exists": os.path.exists(file_path)
    }

@app.delete("/images/{filename}")
def delete_image(filename: str):
    file_path = os.path.join("uploads", filename)
    if not os.path.isfile(file_path):
        return {
            "filename": filename,
            "message": "File not found"
        }
    os.remove(file_path)
    return {
        "filename": filename,
        "message": "File deleted"
    }