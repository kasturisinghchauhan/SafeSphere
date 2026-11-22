

import cv2
import json

from backend.tracking.tracker import SafeSphereTracker
from backend.tracking.motion import MotionEstimator
from backend.risk_engine.risk_calculator import RiskCalculator
from backend.intervention.intervention_engine import (
    CounterfactualInterventionEngine
)


# 1. Load video
video_path = "videos/warehouse.mp4"
output_path = "videos/risk_output.mp4"
intervention_output = "videos/intervention_results.json"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise SystemExit("Cannot open warehouse video!")

fps = cap.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    fps = 25

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


# 2. Initialize modules
tracker = SafeSphereTracker()
motion = MotionEstimator(fps=fps)
risk_engine = RiskCalculator()
intervention_engine = CounterfactualInterventionEngine()


# 3. Create output video
writer = cv2.VideoWriter(
    output_path,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (1280, 720)
)

frame_number = 0

risk_counts = {
    "HIGH": 0,
    "MEDIUM": 0,
    "LOW": 0
}

intervention_records = []

print("Starting SafeSphere Risk Analysis...")


try:
    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.resize(frame, (1280, 720))

        # Detection and tracking
        tracked_objects = tracker.track(frame)

        # Movement estimation
        motion_objects = motion.update(
            tracked_objects,
            frame_number
        )

        # Calculate worker-forklift risks
        risks = risk_engine.analyze(motion_objects)

        # Create lookup using tracking IDs
        objects_by_id = {
            obj["track_id"]: obj
            for obj in motion_objects
        }

        # Display risk results and run counterfactual analysis
        for risk in risks:

            level = risk["risk_level"]
            risk_counts[level] += 1

            print(
                f"Worker {risk['worker_id']} | "
                f"Forklift {risk['forklift_id']} | "
                f"TTC: {risk['ttc_seconds']} | "
                f"CPA: {risk['cpa_distance_pixels']} px | "
                f"Risk: {level}"
            )

            # Run CSIE for HIGH and MEDIUM risk observations
            if level in ["HIGH", "MEDIUM"]:

                worker = objects_by_id.get(
                    risk["worker_id"]
                )

                forklift = objects_by_id.get(
                    risk["forklift_id"]
                )

                if worker is not None and forklift is not None:

                    comparisons = intervention_engine.compare(
                        worker,
                        forklift
                    )

                    # Select scenario with maximum predicted distance
                    best_scenario = max(
                        comparisons,
                        key=lambda x: x[
                            "predicted_closest_distance"
                        ]
                    )

                    record = {
                        "frame": frame_number,
                        "worker_id": risk["worker_id"],
                        "forklift_id": risk["forklift_id"],
                        "original_risk": level,
                        "scenarios": comparisons,
                        "best_scenario": best_scenario
                    }

                    intervention_records.append(record)

                    print("\n--- COUNTERFACTUAL ANALYSIS ---")

                    for scenario in comparisons:

                        print(
                            f"Intervention: "
                            f"{scenario['intervention']} | "
                            f"Predicted Risk: "
                            f"{scenario['predicted_risk']} | "
                            f"Closest Distance: "
                            f"{scenario['predicted_closest_distance']} px"
                        )

                    print(
                        "Best predicted scenario:",
                        best_scenario["intervention"]
                    )

                    print("-------------------------------\n")

        # Display object IDs
        for obj in motion_objects:

            x1, y1, x2, y2 = obj["bbox"]

            label = (
                f"{obj['label']} ID:{obj['track_id']}"
            )

            color = (
                (0, 255, 0)
                if obj["label"] == "person"
                else (0, 165, 255)
            )

            cv2.rectangle(
                frame, (x1, y1), (x2, y2), color, 2
            )

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )

        writer.write(frame)

        frame_number += 1

        if frame_number % 50 == 0:
            print(
                f"Processed {frame_number}/{total_frames}"
            )

finally:
    cap.release()
    writer.release()


# 4. Save counterfactual analysis results
with open(intervention_output, "w") as file:
    json.dump(
        intervention_records,
        file,
        indent=4
    )


print("\nSafeSphere Risk Analysis Completed!")
print("Frames processed:", frame_number)
print("Risk observations:", risk_counts)
print("Counterfactual comparisons:", len(intervention_records))
print("Risk video saved:", output_path)
print("Intervention results saved:", intervention_output)
