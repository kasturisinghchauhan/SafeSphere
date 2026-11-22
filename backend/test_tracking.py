

import cv2
from backend.tracking.tracker import SafeSphereTracker
from backend.tracking.motion import MotionEstimator

# 1. Load warehouse video
video_path = "videos/warehouse.mp4"
output_path = "videos/motion_output.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise SystemExit("Cannot open warehouse video!")

fps = cap.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    fps = 25

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# 2. Initialize AI modules
tracker = SafeSphereTracker()
motion = MotionEstimator(fps=fps)

# 3. Create output video
writer = cv2.VideoWriter(
    output_path,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (1280, 720)
)

frame_number = 0
unique_ids = set()

print("Starting SafeSphere Motion Analysis...")

try:
    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.resize(frame, (1280, 720))

        # 4. Object detection and tracking
        tracked_objects = tracker.track(frame)

        # 5. Calculate movement and trajectory
        motion_objects = motion.update(
            tracked_objects,
            frame_number
        )

        # 6. Draw results
        for obj in motion_objects:

            track_id = obj["track_id"]
            label = obj["label"]

            x1, y1, x2, y2 = obj["bbox"]
            cx, cy = map(int, obj["center"])

            speed = obj["speed_pixels_per_second"]

            unique_ids.add(track_id)

            color = (
                (0, 255, 0)
                if label == "person"
                else (0, 165, 255)
            )

            cv2.rectangle(
                frame, (x1, y1), (x2, y2), color, 2
            )

            cv2.circle(
                frame, (cx, cy), 4, color, -1
            )

            text = f"{label} ID:{track_id} Speed:{speed:.1f}px/s"

            cv2.putText(
                frame,
                text,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )

            # Draw recent trajectory
            trajectory = obj["trajectory"]

            for i in range(1, len(trajectory)):

                p1 = tuple(map(int, trajectory[i - 1]))
                p2 = tuple(map(int, trajectory[i]))

                cv2.line(
                    frame, p1, p2, color, 2
                )

        writer.write(frame)

        frame_number += 1

        if frame_number % 50 == 0:
            print(
                f"Processed {frame_number}/{total_frames} frames"
            )

finally:
    cap.release()
    writer.release()

print("\nMotion Analysis Completed!")
print("Frames processed:", frame_number)
print("Unique tracking IDs:", len(unique_ids))
print("Output:", output_path)
