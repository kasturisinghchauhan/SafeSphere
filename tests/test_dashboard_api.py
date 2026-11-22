
import json

import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.api import dashboard_routes


@pytest.fixture
def client():
    return TestClient(app)


def create_results_file(tmp_path):
    records = [
        {"original_risk": "HIGH", "worker_id": 1},
        {"original_risk": "HIGH", "worker_id": 2},
        {"original_risk": "MEDIUM", "worker_id": 3},
        {"original_risk": "LOW", "worker_id": 4}
    ]

    file_path = tmp_path / "intervention_results.json"

    with open(file_path, "w") as file:
        json.dump(records, file)

    return file_path, records


def test_dashboard_summary(client, tmp_path, monkeypatch):
    file_path, records = create_results_file(tmp_path)

    monkeypatch.setattr(
        dashboard_routes, "RESULTS_PATH", file_path
    )

    response = client.get("/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["intervention_triggered_observations"] == 4
    assert data["risk_distribution_in_records"] == {
        "HIGH": 2,
        "MEDIUM": 1
    }


def test_dashboard_interventions(client, tmp_path, monkeypatch):
    file_path, records = create_results_file(tmp_path)

    monkeypatch.setattr(
        dashboard_routes, "RESULTS_PATH", file_path
    )

    response = client.get("/dashboard/interventions")

    assert response.status_code == 200

    data = response.json()

    assert data["total_records"] == 4
    assert data["records"] == records


def test_summary_missing_file(client, tmp_path, monkeypatch):
    missing_file = tmp_path / "missing.json"

    monkeypatch.setattr(
        dashboard_routes, "RESULTS_PATH", missing_file
    )

    response = client.get("/dashboard/summary")

    assert response.status_code == 404
    assert response.json()["detail"] == "Intervention results not found"


def test_interventions_missing_file(client, tmp_path, monkeypatch):
    missing_file = tmp_path / "missing.json"

    monkeypatch.setattr(
        dashboard_routes, "RESULTS_PATH", missing_file
    )

    response = client.get("/dashboard/interventions")

    assert response.status_code == 404
    assert response.json()["detail"] == "Intervention results not found"


def test_dashboard_video(client, tmp_path, monkeypatch):
    video_file = tmp_path / "test_video.mp4"
    video_content = b"test video content"
    video_file.write_bytes(video_content)

    monkeypatch.setattr(
        dashboard_routes, "VIDEO_PATH", video_file
    )

    response = client.get("/dashboard/video")

    assert response.status_code == 200
    assert response.headers["content-type"] == "video/mp4"
    assert response.headers["content-disposition"] == "inline"
    assert response.content == video_content


def test_video_missing_file(client, tmp_path, monkeypatch):
    missing_video = tmp_path / "missing.mp4"

    monkeypatch.setattr(
        dashboard_routes, "VIDEO_PATH", missing_video
    )

    response = client.get("/dashboard/video")

    assert response.status_code == 404
    assert response.json()["detail"] == "Risk video not found"
