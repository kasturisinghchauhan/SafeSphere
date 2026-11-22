
from pathlib import Path
import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

VIDEO_PATH = PROJECT_ROOT / "videos" / "risk_output_browser.mp4"
RESULTS_PATH = PROJECT_ROOT / "videos" / "intervention_results.json"


@router.get("/video")
def get_risk_video():

    if not VIDEO_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Risk video not found"
        )

    return FileResponse(
    path=VIDEO_PATH,
    media_type="video/mp4",
    headers={"Content-Disposition": "inline"}
    )


@router.get("/interventions")
def get_interventions():

    if not RESULTS_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Intervention results not found"
        )

    with open(RESULTS_PATH, "r") as file:
        records = json.load(file)

    return {
        "total_records": len(records),
        "records": records
    }


@router.get("/summary")
def get_dashboard_summary():

    if not RESULTS_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Intervention results not found"
        )

    with open(RESULTS_PATH, "r") as file:
        records = json.load(file)

    risk_counts = {
        "HIGH": 0,
        "MEDIUM": 0
    }

    for record in records:
        level = record.get("original_risk")

        if level in risk_counts:
            risk_counts[level] += 1

    return {
        "intervention_triggered_observations": len(records),
        "risk_distribution_in_records": risk_counts
    }
