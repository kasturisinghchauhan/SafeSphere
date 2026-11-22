
import cv2
from ultralytics import YOLOWorld

print("Loading YOLO-World...")

model = YOLOWorld("yolov8s-world.pt")

test_classes = [
    "person",
    "forklift",
    "forklift truck",
    "industrial forklift",
    "warehouse forklift"
]

model.set_classes(test_classes)

cap = cv2.VideoCapture("videos/warehouse.mp4")

if not cap.isOpened():
    print("Error: Warehouse video not found!")
    exit()

print("\nTesting forklift detection...\n")

for frame_number in range(100):

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(frame, (1280, 720))

    results = model.predict(
        source=frame,
        conf=0.10,
        verbose=False
    )

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            label = model.names[class_id]

            print(
                f"Frame: {frame_number} | "
                f"Object: {label} | "
                f"Confidence: {confidence:.3f}"
            )

cap.release()

print("\nForklift detection test completed!")
