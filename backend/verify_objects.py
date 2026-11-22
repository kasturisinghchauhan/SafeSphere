
import cv2
from collections import Counter
from backend.tracking.tracker import SafeSphereTracker

cap = cv2.VideoCapture("videos/warehouse.mp4")
tracker = SafeSphereTracker()

counts = Counter()
ids = set()

frame_number = 0

while frame_number < 100:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(frame, (1280, 720))

    objects = tracker.track(frame)

    for obj in objects:
        counts[obj["label"]] += 1
        ids.add((obj["label"], obj["track_id"]))

    frame_number += 1

cap.release()

print("\nOBJECT DETECTION REPORT")
print("Frames checked:", frame_number)
print("Detection counts:", dict(counts))
print("Unique tracked objects:", ids)
print("Unique object count:", len(ids))
