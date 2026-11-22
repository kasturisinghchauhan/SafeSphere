
import pytest

from backend.risk_engine.risk_calculator import RiskCalculator


@pytest.fixture
def calculator():
    return RiskCalculator(
        prediction_horizon=5.0,
        safety_distance=100
    )


def create_worker():
    return {
        "track_id": 1,
        "label": "person",
        "center": (0, 0),
        "velocity": (0, 0)
    }


def create_forklift(x, y, vx, vy):
    return {
        "track_id": 2,
        "label": "industrial forklift",
        "center": (x, y),
        "velocity": (vx, vy)
    }


def test_high_risk(calculator):
    worker = create_worker()
    forklift = create_forklift(150, 0, -50, 0)

    result = calculator.calculate_pair_risk(
        worker, forklift
    )

    assert result["risk_level"] == "HIGH"
    assert result["ttc_seconds"] == 1.0


def test_medium_risk(calculator):
    worker = create_worker()
    forklift = create_forklift(300, 0, -50, 0)

    result = calculator.calculate_pair_risk(
        worker, forklift
    )

    assert result["risk_level"] == "MEDIUM"
    assert result["ttc_seconds"] == 4.0


def test_low_risk(calculator):
    worker = create_worker()
    forklift = create_forklift(150, 150, -50, 0)

    result = calculator.calculate_pair_risk(
        worker, forklift
    )

    assert result["risk_level"] == "LOW"


def test_analyze_worker_forklift_pairs(calculator):
    worker = create_worker()

    forklift = create_forklift(150, 0, -50, 0)

    other_object = {
        "track_id": 3,
        "label": "car",
        "center": (500, 500),
        "velocity": (0, 0)
    }

    results = calculator.analyze([
        worker,
        forklift,
        other_object
    ])

    assert len(results) == 1
    assert results[0]["worker_id"] == 1
    assert results[0]["forklift_id"] == 2
