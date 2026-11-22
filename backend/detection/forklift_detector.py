
import cv2
from ultralytics import YOLOWorld


class IndustrialDetector:

    def __init__(self):
        # Load open-vocabulary YOLO model
        self.model = YOLOWorld("yolov8s-world.pt")

        # Define objects required by SafeSphere
        self.model.set_classes(["person", "forklift"])

    def detect(self, frame):

        results = self.model.predict(
            source=frame,
            conf=0.25,
            verbose=False
        )

        detections = []

        for result in results:
            for box in result.boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                label = self.model.names[class_id]

                x1, y1, x2, y2 = map(
                    int, box.xyxy[0].tolist()
                )

                detections.append({
                    "label": label,
                    "confidence": confidence,
                    "bbox": [x1, y1, x2, y2]
                })

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"{label} {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        return frame, detections
