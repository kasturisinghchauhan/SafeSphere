

from fastapi import FastAPI
from datetime import datetime
from backend.api.dashboard_routes import router as dashboard_router
from backend.api.intervention_routes import router as intervention_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SafeSphere",
    description="Predictive and Counterfactual Industrial Safety Intelligence",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://safe-sphere-sage.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(intervention_router)
app.include_router(dashboard_router)


@app.get("/")
def home():
    return {
        "project": "SafeSphere",
        "message": "Industrial Safety Intelligence System is running",
        "status": "Active"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
