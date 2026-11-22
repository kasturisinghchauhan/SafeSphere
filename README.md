SafeSphere – Predictive and Counterfactual Industrial Safety Intelligence

SafeSphere is a computer vision-based industrial safety project designed to analyze warehouse environments, detect workers and forklifts, estimate their movement, and identify potential collision risks.

The system uses motion prediction and counterfactual simulations to compare possible safety interventions. A web dashboard displays the processed video, risk information, and intervention results.

Key Features

Worker and Forklift Detection: Detects people and forklifts in warehouse video.

Object Tracking: Tracks detected objects across video frames using ByteTrack.

Motion Analysis: Estimates object positions, movement, and trajectories.

Collision Risk Prediction: Uses Time-to-Collision (TTC) and Closest Point of Approach (CPA) calculations.

Counterfactual Intervention Engine: Compares different hypothetical safety actions.

Interactive Dashboard: Displays video, risk summaries, and intervention history.

REST API: Provides dashboard data through FastAPI endpoints.

Automated Testing: Includes tests for risk calculations, interventions, and API endpoints.

Counterfactual Safety Interventions

SafeSphere compares four scenarios:

Baseline: Evaluates the situation without an intervention.

Reduce Forklift Speed: Simulates reducing forklift velocity.

Worker Pause: Simulates temporarily stopping worker movement.

Alternate Forklift Route: Simulates changing the forklift's movement direction.

These are simulated scenarios, not real-world control commands.

Technology Stack

Component

Technologies

Programming Language

Python, JavaScript

Computer Vision

OpenCV, Ultralytics YOLO

Object Tracking

ByteTrack

Motion and Risk Analysis

NumPy, Python

Backend

FastAPI, Uvicorn

Frontend

React, Vite

Icons

Lucide React

Testing

Pytest

Video Processing

OpenCV, FFmpeg through imageio-ffmpeg

Project Structure

SafeSphereee/
│
├── backend/
│   ├── api/
│   ├── detection/
│   ├── tracking/
│   ├── prediction/
│   ├── risk_engine/
│   ├── intervention/
│   ├── database/
│   └── main.py
│
├── frontend/
│   ├── src/
│   └── package.json
│
├── datasets/
├── models/
├── videos/
│   ├── warehouse.mp4
│   ├── risk_output.mp4
│   ├── risk_output_browser.mp4
│   └── intervention_results.json
│
├── tests/
│   ├── test_risk_calculator.py
│   ├── test_intervention_engine.py
│   └── test_dashboard_api.py
│
├── requirements.txt
└── README.md

Installation and Setup

1. Clone the Repository

git clone <your-repository-url>
cd SafeSphereee

2. Create and Activate Python Virtual Environment

python -m venv .venv
.\.venv\Scripts\Activate.ps1

3. Install Python Dependencies

pip install -r requirements.txt

4. Install Frontend Dependencies

Open a terminal in the project root and run:

cd frontend
npm install

Running the Project

The backend and frontend must run in separate terminals.

Start Backend

From the project root:

python -m uvicorn backend.main:app --reload

Backend URL:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

Start Frontend

In another terminal:

cd frontend
npm run dev

Frontend URL:

http://localhost:5173

API Endpoints

Endpoint

Description

/

Project status

/health

Backend health check

/dashboard/summary

Risk and intervention summary

/dashboard/interventions

Intervention records

/dashboard/video

Processed warehouse video

Demo Results

The current demonstration processed a warehouse video containing 541 frames.

Metric

Result

Frames Processed

541

HIGH Risk Observations

113

MEDIUM Risk Observations

12

LOW Risk Observations

336

Intervention Records

125

Counterfactual Scenarios Compared

500

Note: The risk counts represent observations from the demonstration pipeline. The 125 intervention records are compared across four scenarios each, producing 500 scenario evaluations. These are not 500 separate incidents.

Running Automated Tests

From the project root:

python -m pytest tests -v

Current test result: 15 tests passed.

The test suite covers:

Risk classification and worker-forklift pair analysis.

Counterfactual intervention simulations.

Dashboard API responses and error handling.

Limitations

Distance calculations currently use pixels and are not calibrated to real-world metres.

Tracking IDs may become fragmented across frames.

Object detection can produce false positives.

Motion prediction uses simplified movement assumptions.

Alternate-route simulation does not account for actual warehouse layouts or physical constraints.

Intervention results are hypothetical and have not been validated as operational safety recommendations.

SafeSphere is a research and demonstration project. It is not a certified industrial safety system and should not replace workplace safety procedures, trained supervision, or physical safety mechanisms.

Future Improvements

Improve object detection and tracking reliability.

Add camera calibration for real-world distance estimation.

Introduce uncertainty-aware collision prediction.

Add warehouse-layout-aware route planning.

Evaluate the system using larger and more diverse industrial datasets.

Improve intervention validation and performance evaluation.

Project: SafeSphere – Predictive and Counterfactual Industrial Safety Intelligence

Type: Individual Computer Vision Project