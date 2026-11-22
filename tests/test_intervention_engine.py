
import pytest

from backend.intervention.intervention_engine import (
    CounterfactualInterventionEngine
)


@pytest.fixture
def engine():
    return CounterfactualInterventionEngine(
        safety_distance=100
    )


def create_worker():
    return {
        "track_id": 1,
        "center": (0, 0),
        "velocity": (10, 0)
    }


def create_forklift():
    return {
        "track_id": 2,
        "center": (150, 0),
        "velocity": (-20, 0)
    }


def test_baseline_simulation(engine):
    result = engine.simulate(
        create_worker(),
        create_forklift(),
        "baseline"
    )

    assert result["intervention"] == "baseline"
    assert result["predicted_risk"] == "HIGH"
    assert result["predicted_closest_distance"] == 0


def test_reduce_forklift_speed(engine):
    result = engine.simulate(
        create_worker(),
        create_forklift(),
        "reduce_forklift_speed"
    )

    assert result["intervention"] == "reduce_forklift_speed"
    assert result["predicted_closest_distance"] == 50
    assert result["predicted_risk"] == "MEDIUM"


def test_worker_pause(engine):
    result = engine.simulate(
        create_worker(),
        create_forklift(),
        "worker_pause"
    )

    assert result["intervention"] == "worker_pause"
    assert result["predicted_risk"] == "MEDIUM"


def test_alternate_forklift_route(engine):
    result = engine.simulate(
        create_worker(),
        create_forklift(),
        "alternate_forklift_route"
    )

    assert result["intervention"] == "alternate_forklift_route"
    assert result["predicted_risk"] == "LOW"


def test_compare_all_scenarios(engine):
    results = engine.compare(
        create_worker(),
        create_forklift()
    )

    assert len(results) == 4

    expected_scenarios = [
        "baseline",
        "reduce_forklift_speed",
        "worker_pause",
        "alternate_forklift_route"
    ]

    actual_scenarios = [
        result["intervention"]
        for result in results
    ]

    assert actual_scenarios == expected_scenarios
