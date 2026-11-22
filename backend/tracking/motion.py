
from collections import defaultdict, deque
import math


class MotionEstimator:

    def __init__(self, fps=25, history_size=30):
        self.fps = fps
        self.history = defaultdict(
            lambda: deque(maxlen=history_size)
        )

        self.previous_positions = {}

    def update(self, tracked_objects, frame_number):

        current_time = frame_number / self.fps
        motion_results = []

        for obj in tracked_objects:

            track_id = obj["track_id"]
            x1, y1, x2, y2 = obj["bbox"]

            # Calculate object centre
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            current_position = (center_x, center_y)

            velocity_x = 0.0
            velocity_y = 0.0
            speed = 0.0

            # Calculate movement using previous position
            if track_id in self.previous_positions:

                old_x, old_y, old_time = (
                    self.previous_positions[track_id]
                )

                time_difference = current_time - old_time

                if time_difference > 0:

                    velocity_x = (
                        center_x - old_x
                    ) / time_difference

                    velocity_y = (
                        center_y - old_y
                    ) / time_difference

                    speed = math.sqrt(
                        velocity_x ** 2 + velocity_y ** 2
                    )

            # Save current position
            self.previous_positions[track_id] = (
                center_x, center_y, current_time
            )

            self.history[track_id].append(
                current_position
            )

            motion_results.append({
                **obj,
                "center": [
                    round(center_x, 2),
                    round(center_y, 2)
                ],
                "velocity": [
                    round(velocity_x, 2),
                    round(velocity_y, 2)
                ],
                "speed_pixels_per_second": round(speed, 2),
                "trajectory": list(self.history[track_id])
            })

        return motion_results
