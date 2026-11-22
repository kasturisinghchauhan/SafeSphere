
import cv2

from backend.detection.forklift_detector import IndustrialDetector

detector = IndustrialDetector()

frame = cv2.imread("videos/test.jpg")

if frame is None:
    print("Image not found!")
else:
    output, detections = detector.detect(frame)

    print("\nSafeSphere Detection Results:")

    for item in detections:
        print(item)

    print("\nTotal objects:", len(detections))

    cv2.imshow("SafeSphere Detection", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
