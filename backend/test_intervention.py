
from backend.intervention.intervention_engine import (
    CounterfactualInterventionEngine
)

# Synthetic test data (not actual video measurements)
worker = {
    "track_id": 1,
    "label": "person",
    "center": [300, 300],
    "velocity": [10, 0]
}

forklift = {
    "track_id": 2,
    "label": "forklift",
    "center": [600, 300],
    "velocity": [-30, 0]
}

# Initialize intervention engine
engine = CounterfactualInterventionEngine()

# Compare all intervention scenarios
results = engine.compare(worker, forklift)

print("\nSAFESPHERE COUNTERFACTUAL ANALYSIS")
print("=" * 45)

for result in results:

    print("\nIntervention:", result["intervention"])
    print("Predicted risk:", result["predicted_risk"])
    print(
        "Closest distance:",
        result["predicted_closest_distance"],
        "pixels"
    )
    print(
        "Closest approach time:",
        result["closest_approach_time"],
        "seconds"
    )

print("\nAnalysis completed!")
