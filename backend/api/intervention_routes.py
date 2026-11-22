from fastapi import APIRouter
from pydantic import BaseModel
from backend.intervention.intervention_engine import (
    CounterfactualInterventionEngine
)

router = APIRouter(
    prefix="/intervention",
    tags=["Counterfactual Intervention"]
)

engine = CounterfactualInterventionEngine()


class ObjectState(BaseModel):
    track_id: int
    label: str
    center: list[float]
    velocity: list[float]


class InterventionRequest(BaseModel):
    worker: ObjectState
    forklift: ObjectState


@router.post("/compare")
def compare_interventions(request: InterventionRequest):

    results = engine.compare(
        request.worker.model_dump(),
        request.forklift.model_dump()
    )

    return {
        "status": "success",
        "message": "Counterfactual analysis completed",
        "results": results
    }