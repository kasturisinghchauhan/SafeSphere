
import math


class RiskCalculator:

    def __init__(self, prediction_horizon=5.0, safety_distance=100):
        self.prediction_horizon = prediction_horizon
        self.safety_distance = safety_distance

    def calculate_pair_risk(self, worker, forklift):

        # Worker position and velocity
        wx, wy = worker["center"]
        wvx, wvy = worker["velocity"]

        # Forklift position and velocity
        fx, fy = forklift["center"]
        fvx, fvy = forklift["velocity"]

        # Relative position and velocity
        rx = fx - wx
        ry = fy - wy

        rvx = fvx - wvx
        rvy = fvy - wvy

        # Current distance
        current_distance = math.hypot(rx, ry)

        # Relative speed squared
        velocity_squared = rvx ** 2 + rvy ** 2

        # Calculate closest point of approach (CPA)
        if velocity_squared < 1e-6:
            cpa_time = 0.0
        else:
            cpa_time = -(
                rx * rvx + ry * rvy
            ) / velocity_squared

        cpa_time = max(
            0.0,
            min(cpa_time, self.prediction_horizon)
        )

        # Predicted distance at CPA
        closest_x = rx + rvx * cpa_time
        closest_y = ry + rvy * cpa_time

        cpa_distance = math.hypot(
            closest_x, closest_y
        )

        # Calculate estimated TTC using safety distance
        ttc = None

        a = velocity_squared
        b = 2 * (rx * rvx + ry * rvy)
        c = rx ** 2 + ry ** 2 - self.safety_distance ** 2

        if current_distance <= self.safety_distance:
            ttc = 0.0

        elif a > 1e-6:

            discriminant = b ** 2 - 4 * a * c

            if discriminant >= 0:

                t1 = (-b - math.sqrt(discriminant)) / (2 * a)
                t2 = (-b + math.sqrt(discriminant)) / (2 * a)

                positive_times = [
                    t for t in [t1, t2]
                    if t >= 0
                ]

                if positive_times:
                    ttc = min(positive_times)

        # Preliminary risk classification
        if cpa_distance <= self.safety_distance:

            if ttc is not None and ttc <= 2:
                risk_level = "HIGH"
            elif ttc is not None and ttc <= 5:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"

        else:
            risk_level = "LOW"

        return {
            "worker_id": worker["track_id"],
            "forklift_id": forklift["track_id"],
            "current_distance_pixels": round(current_distance, 2),
            "ttc_seconds": (
                round(ttc, 2) if ttc is not None else None
            ),
            "cpa_time_seconds": round(cpa_time, 2),
            "cpa_distance_pixels": round(cpa_distance, 2),
            "risk_level": risk_level
        }

    def analyze(self, motion_objects):

        workers = [
            obj for obj in motion_objects
            if obj["label"] == "person"
        ]

        forklifts = [
            obj for obj in motion_objects
            if obj["label"] in ["forklift", "industrial forklift"]
        ]

        results = []

        for worker in workers:
            for forklift in forklifts:

                result = self.calculate_pair_risk(
                    worker, forklift
                )

                results.append(result)

        return results
