from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

results = model("uploads/street.jpeg")

result = results[0]

img = cv2.imread("uploads/street.jpeg")

for box in result.boxes:

    cls_id = int(box.cls[0])

    confidence = float(box.conf[0])

    label = model.names[cls_id]

    x1, y1, x2, y2 = map(
        int,
        box.xyxy[0].tolist()
    )

    cv2.rectangle(
        img,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        2
    )

    cv2.putText(
        img,
        f"{label} {confidence:.2f}",
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 0),
        2
    )

cv2.imwrite(
    "annotated/street_detected.jpeg",
    img
)