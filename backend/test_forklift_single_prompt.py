
import cv2
from collections import Counter
from ultralytics import YOLOWorld

model = YOLOWorld("yolov8s-world.pt")

model.set_classes([
    "person",
    "industrial forklift"
])

cap = cv2.VideoCapture("videos/warehouse.mp4")

counts = Counter()

for frame_number in range(100):

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(frame, (1280, 720))

    results = model.predict(
        source=frame,
        conf=0.01,
        imgsz=1280,
        verbose=False
    )

    for result in results:
        for box in result.boxes:

            label = model.names[int(box.cls[0])]
            counts[label] += 1

cap.release()

print("\nDETECTION WITHOUT TRACKING")
print(dict(counts))
