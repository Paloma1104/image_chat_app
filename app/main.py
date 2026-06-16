from email.mime import image

from fastapi import FastAPI
import os
from fastapi import UploadFile, File, Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.database.models import Image
from app.database.database import engine
from app.database.database import Base

Base.metadata.create_all(bind=engine)

os.makedirs("uploads", exist_ok=True)
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from FastAPI"}

@app.get("/images")
def list_images(
        db: Session = Depends(get_db)
):
    images = db.query(Image).all()

    return [
        {
            "id": image.id,
            "filename": image.filename,
            "title": image.title,
            "notes": image.notes,
            "uploaded_at": image.uploaded_at
        }
        for image in images
    ]

@app.post("/images")
async def upload_image(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    contents = await file.read()

    file_path = os.path.join("uploads", file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    image = Image(
        filename = file.filename,
        title = file.filename,
        notes = ""
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    return {
        "id": image.id,
        "filename": image.filename
    }

@app.get("/images/{filename}")
def get_image(
    filename: str,
    db: Session = Depends(get_db)
):
    image = (
        db.query(Image)
        .filter(Image.filename == filename)
        .first()
    )

    if image is None:
        return {
            "message": "Image not found"
        }

    return {
        "id": image.id,
        "filename": image.filename,
        "title": image.title,
        "notes": image.notes,
        "uploaded_at": image.uploaded_at
    }

@app.delete("/images/{filename}")
def delete_image(
    filename: str,
    db: Session = Depends(get_db)
):
    image = (
        db.query(Image)
        .filter(Image.filename == filename)
        .first()
    )

    if image is None:
        return {
            "filename": filename,
            "message": "File not found"
        }

    file_path = os.path.join("uploads", filename)

    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(image)
    db.commit()

    return {
        "filename": filename,
        "message": "File deleted"
    }