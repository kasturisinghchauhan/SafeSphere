
import cv2
from ultralytics import YOLOWorld

model = YOLOWorld("yolov8s-world.pt")

model.set_classes([
    "person",
    "forklift",
    "forklift truck",
    "industrial forklift",
    "warehouse forklift"
])

cap = cv2.VideoCapture("videos/warehouse.mp4")

ret, frame = cap.read()
cap.release()

if not ret:
    print("Video frame could not be read!")
    exit()

frame = cv2.resize(frame, (1280, 720))

print("\n========== PREDICT RESULTS ==========")

predict_results = model.predict(
    source=frame,
    conf=0.10,
    imgsz=1280,
    verbose=False
)

for result in predict_results:
    for box in result.boxes:
        class_id = int(box.cls[0])
        print({
            "label": model.names[class_id],
            "confidence": round(float(box.conf[0]), 3)
        })

print("\n========== TRACK RESULTS ==========")

track_results = model.track(
    source=frame,
    persist=True,
    tracker="backend/tracking/safesphere_bytetrack.yaml",
    conf=0.10,
    imgsz=1280,
    verbose=False
)

for result in track_results:
    for box in result.boxes:
        class_id = int(box.cls[0])

        track_id = (
            int(box.id[0])
            if box.id is not None
            else None
        )

        print({
            "label": model.names[class_id],
            "confidence": round(float(box.conf[0]), 3),
            "track_id": track_id
        })

print("\nComparison completed!")
