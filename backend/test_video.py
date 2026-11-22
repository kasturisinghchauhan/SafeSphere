
import cv2

video_path = "videos/warehouse.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Video could not be opened!")
else:
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    duration = total_frames / fps if fps > 0 else 0

    print("Video opened successfully!")
    print("FPS:", fps)
    print("Total frames:", total_frames)
    print("Resolution:", width, "x", height)
    print("Duration:", round(duration, 2), "seconds")

cap.release()
