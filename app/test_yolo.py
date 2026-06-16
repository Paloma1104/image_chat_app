from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model("uploads/street.jpeg")

result = results[0]

for box in result.boxes:

    cls_id = int(box.cls[0])

    confidence = float(box.conf[0])

    label = model.names[cls_id]

    bbox = box.xyxy[0].tolist()

    print(
        label,
        confidence,
        bbox
    )