
import cv2
from ultralytics import YOLOWorld

model = YOLOWorld("yolov8s-world.pt")

model.set_classes([
    "person",
    "industrial forklift",
    "forklift truck"
])

cap = cv2.VideoCapture("videos/warehouse.mp4")

if not cap.isOpened():
    print("Could not open warehouse video!")
    exit()

for frame_number in [0, 3, 4, 7, 11]:
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()

    if not ret:
        continue

    frame = cv2.resize(frame, (1280, 720))

    results = model.predict(
        source=frame,
        conf=0.10,
        verbose=False
    )

    annotated = results[0].plot()

    cv2.imwrite(
        f"videos/forklift_frame_{frame_number}.jpg",
        annotated
    )

    print(f"Saved frame {frame_number}")

cap.release()

print("Visual verification completed!")

