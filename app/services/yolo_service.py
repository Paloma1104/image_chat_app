from ultralytics import YOLO

model = YOLO("yolov8n.pt")


def detect_objects(image_path):

    results = model(image_path)

    result = results[0]

    detections = []

    for box in result.boxes:

        cls_id = int(box.cls[0])

        confidence = float(box.conf[0])

        label = model.names[cls_id]

        x1, y1, x2, y2 = map(
            int,
            box.xyxy[0].tolist()
        )

        detections.append(
            {
                "label": label,
                "confidence": confidence,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            }
        )

    return detections