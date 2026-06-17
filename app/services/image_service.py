import cv2


def draw_detections(
    image_path,
    detections,
    output_path
):
    img = cv2.imread(image_path)

    for detection in detections:

        x1 = int(detection["x1"])
        y1 = int(detection["y1"])
        x2 = int(detection["x2"])
        y2 = int(detection["y2"])

        label = detection["label"]

        confidence = detection["confidence"]

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
        output_path,
        img
    )