

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

if not cap.isOpened():
    print("Video could not be opened!")
    exit()

ret, frame = cap.read()

if not ret:
    print("Could not read frame!")
    exit()

frame = cv2.resize(frame, (1280, 720))

print("\n========== PREDICT RESULTS ==========")

predictions = model.predict(
    source=frame,
    conf=0.05,
    imgsz=1280,
    verbose=False
)

for result in predictions:
    for box in result.boxes:
        class_id = int(box.cls[0])
        print({
            "label": model.names[class_id],
            "confidence": round(float(box.conf[0]), 3)
        })

print("\n========== TRACK RESULTS ==========")

tracked = model.track(
    source=frame,
    persist=True,
    tracker="backend/tracking/safesphere_bytetrack.yaml",
    conf=0.01,
    imgsz=1280,
    verbose=False
)

for result in tracked:
    for box in result.boxes:
        class_id = int(box.cls[0])
        track_id = int(box.id[0]) if box.id is not None else None

        print({
            "label": model.names[class_id],
            "confidence": round(float(box.conf[0]), 3),
            "track_id": track_id
        })

cap.release()
print("\nDiagnostic completed!")
