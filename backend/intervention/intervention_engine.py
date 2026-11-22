
import math


class CounterfactualInterventionEngine:

    def __init__(self, safety_distance=100):
        self.safety_distance = safety_distance

    def simulate(self, worker, forklift, intervention):

        wx, wy = worker["center"]
        wvx, wvy = worker["velocity"]

        fx, fy = forklift["center"]
        fvx, fvy = forklift["velocity"]

        # Apply hypothetical intervention
        if intervention == "reduce_forklift_speed":
            fvx *= 0.5
            fvy *= 0.5

        elif intervention == "worker_pause":
            wvx = 0
            wvy = 0

        elif intervention == "alternate_forklift_route":
            # Simplified hypothetical route change
            fvx, fvy = -fvy, fvx

        # Relative motion
        rx = fx - wx
        ry = fy - wy

        rvx = fvx - wvx
        rvy = fvy - wvy

        velocity_squared = rvx ** 2 + rvy ** 2

        if velocity_squared < 1e-6:
            closest_time = 0
        else:
            closest_time = -(
                rx * rvx + ry * rvy
            ) / velocity_squared

        closest_time = max(0, min(closest_time, 5))

        closest_x = rx + rvx * closest_time
        closest_y = ry + rvy * closest_time

        closest_distance = math.hypot(
            closest_x, closest_y
        )

        risk = (
            "HIGH"
            if closest_distance < self.safety_distance * 0.5
            else "MEDIUM"
            if closest_distance < self.safety_distance
            else "LOW"
        )

        return {
            "intervention": intervention,
            "predicted_closest_distance": round(
                closest_distance, 2
            ),
            "closest_approach_time": round(
                closest_time, 2
            ),
            "predicted_risk": risk
        }

    def compare(self, worker, forklift):

        scenarios = [
            "baseline",
            "reduce_forklift_speed",
            "worker_pause",
            "alternate_forklift_route"
        ]

        results = []

        for scenario in scenarios:

            result = self.simulate(
                worker,
                forklift,
                scenario
            )

            results.append(result)

        return results
