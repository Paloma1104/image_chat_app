from app.services.yolo_service import detect_objects

print(
    detect_objects(
        "uploads/street.jpeg"
    )
)