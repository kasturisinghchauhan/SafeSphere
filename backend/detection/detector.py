
import cv2
from ultralytics import YOLO


class SafeSphereDetector:

    def __init__(self):
        # Load pretrained YOLO model
        self.model = YOLO("yolo11n.pt")

    def detect(self, frame):

        # Run YOLO on the video frame
        results = self.model(frame, verbose=False)

        detections = []

        for result in results:
            for box in result.boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                # COCO class 0 represents a person
                if class_id != 0:
                    continue

                x1, y1, x2, y2 = map(
                    int, box.xyxy[0].tolist()
                )

                detections.append({
                    "label": "Worker",
                    "confidence": confidence,
                    "bbox": [x1, y1, x2, y2]
                })

                # Draw bounding box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                # Display label
                cv2.putText(
                    frame,
                    f"Worker {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        return frame, detections
