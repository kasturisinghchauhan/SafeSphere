
import cv2
from backend.detection.detector import SafeSphereDetector

detector = SafeSphereDetector()

# Create a blank test image
frame = cv2.imread("videos/test.jpg")

if frame is None:
    print("Image not found. Check videos/test.jpg")
else:
    output, detections = detector.detect(frame)

    print("Detected objects:", detections)

    cv2.imshow("SafeSphere Detection", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
