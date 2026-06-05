from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from routes import auth, complaints, dashboard, localities, feedback, officers

# Ensure local static uploads folder exists for local storage fallback
os.makedirs("static/uploads", exist_ok=True)

app = FastAPI(
    title="Municipal Public Grievance Management System API",
    description="Backend API for managing municipal complaints, officers, localities, and feedback.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registration
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(complaints.router, prefix="/api/complaints", tags=["Complaints"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(localities.router, prefix="/api/localities", tags=["Localities"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["Feedback"])
app.include_router(officers.router, prefix="/api/officers", tags=["Officers"])

# Mount static files folder to serve uploaded complaint evidence and feedback images locally
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Municipal Public Grievance Management System API is running",
        "docs": "/docs",
    }
