
from ultralytics import YOLOWorld


class SafeSphereTracker:

    def __init__(self):
        print("Initializing SafeSphere ByteTrack...")

        self.model = YOLOWorld("yolov8s-world.pt")

        # Use only one forklift prompt to avoid duplicate labels
        self.model.set_classes([
            "person",
            "industrial forklift"
        ])

        print("SafeSphere Tracker Ready!")

    def track(self, frame):

        results = self.model.track(
            source=frame,
            persist=True,
            tracker="backend/tracking/safesphere_bytetrack.yaml",
            conf=0.01,
            imgsz=1280,
            verbose=False
        )

        tracked_objects = []

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                if box.id is None:
                    continue

                track_id = int(box.id[0])
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                label = self.model.names[class_id]

                x1, y1, x2, y2 = map(
                    int, box.xyxy[0].tolist()
                )

                tracked_objects.append({
                    "track_id": track_id,
                    "label": label,
                    "confidence": confidence,
                    "bbox": [x1, y1, x2, y2]
                })

        return tracked_objects
