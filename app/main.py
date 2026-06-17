from email.mime import image
from fastapi import FastAPI
import os
from fastapi import UploadFile, File, Depends
from app.services.image_service import draw_detections
from sqlalchemy.orm import Session
from app.services.gemini_service import generate_image_caption
from app.database.dependencies import get_db
from app.database.models import Image, Detection
from app.services.yolo_service import detect_objects
from app.database.database import engine
from app.database.database import Base
from app.schemas import ChatRequest

from app.services.gemini_service import (
    ask_image_question
)

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

@app.post("/detect/{image_id}")
def detect_image(
    image_id: int,
    db: Session = Depends(get_db)
):
    image = (
        db.query(Image)
        .filter(Image.id == image_id)
        .first()
    )

    if image is None:
        return {
            "message": "Image not found"
        }

    file_path = os.path.join(
        "uploads",
        image.filename
    )

    detections = detect_objects(file_path)

    annotated_path = os.path.join(
        "annotated",
        f"{image.id}_detected.jpg"
    )

    draw_detections(
        file_path,
        detections,
        annotated_path
    )

    old_detections = (
        db.query(Detection)
        .filter(
            Detection.image_id == image_id
        )
        .all()
    )

    for detection in old_detections:
        db.delete(detection)

    db.commit()

    for detection in detections:

        db_detection = Detection(
            image_id=image_id,
            label=detection["label"],
            confidence=detection["confidence"],
            x1=detection["x1"],
            y1=detection["y1"],
            x2=detection["x2"],
            y2=detection["y2"]
        )

        db.add(db_detection)

    db.commit()

    return detections

@app.post("/caption/{image_id}")
def generate_caption(
    image_id: int,
    db: Session = Depends(get_db)
):

    image = (
        db.query(Image)
        .filter(Image.id == image_id)
        .first()
    )

    if image is None:
        return {
            "message": "Image not found"
        }

    file_path = os.path.join(
        "uploads",
        image.filename
    )

    caption = generate_image_caption(
        file_path
    )

    return {
        "image_id": image_id,
        "caption": caption
    }

@app.post("/chat/{image_id}")
def chat_with_image(
    image_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    image = (
        db.query(Image)
        .filter(Image.id == image_id)
        .first()
    )

    if image is None:
        return {
            "message": "Image not found"
        }

    file_path = os.path.join(
        "uploads",
        image.filename
    )

    answer = ask_image_question(
        file_path,
        request.question
    )

    return {
        "question": request.question,
        "answer": answer
    }