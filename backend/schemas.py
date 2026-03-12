from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime


class PatientFeatures(BaseModel):
    """Input features for risk prediction"""
    age: int = Field(..., ge=0, le=120, description="Patient age in years")
    bp: int = Field(..., ge=60, le=200, description="Systolic blood pressure")
    cholesterol: int = Field(..., ge=100, le=400, description="Cholesterol level mg/dL")
    bmi: float = Field(..., ge=10, le=60, description="Body Mass Index")
    diabetes: int = Field(..., ge=0, le=1, description="Diabetes status (0=No, 1=Yes)")
    smoking: int = Field(..., ge=0, le=1, description="Smoking status (0=No, 1=Yes)")
    radiation_dose: float = Field(..., ge=0, le=100, description="Radiation dose in Gy")
    treatment_site: str = Field(..., description="Treatment site (e.g., left_chest, right_chest)")
    sessions: int = Field(..., ge=0, le=50, description="Number of radiotherapy sessions")

    class Config:
        json_schema_extra = {
            "example": {
                "age": 45,
                "bp": 130,
                "cholesterol": 210,
                "bmi": 28.5,
                "diabetes": 1,
                "smoking": 0,
                "radiation_dose": 38.0,
                "treatment_site": "left_chest",
                "sessions": 25
            }
        }


class RiskPredictionResponse(BaseModel):
    """Response from risk prediction"""
    risk_probability: float = Field(..., description="Risk probability (0.0 to 1.0)")
    risk_level: str = Field(..., description="Risk level: Low, Medium, or High")
    explanation: str = Field(..., description="Clinical reasoning for the prediction")
    feature_importance: Optional[Dict[str, float]] = Field(None, description="SHAP feature importance scores")
    timestamp: datetime = Field(default_factory=datetime.now)


class PatientRecord(BaseModel):
    """Patient record for database storage"""
    patient_id: Optional[str] = None
    features: PatientFeatures
    prediction: RiskPredictionResponse
    created_at: datetime = Field(default_factory=datetime.now)


class UploadReportResponse(BaseModel):
    """Response from PDF report upload"""
    extracted_features: PatientFeatures
    prediction: RiskPredictionResponse
    raw_text: Optional[str] = None


class PatientHistoryResponse(BaseModel):
    """Response for patient history"""
    records: List[PatientRecord]
    total_count: int


class AgentQuery(BaseModel):
    """Query for AI medical agent"""
    question: str = Field(..., description="Medical question about risk prediction")
    patient_features: Optional[PatientFeatures] = None
    prediction_result: Optional[RiskPredictionResponse] = None

    class Config:
        json_schema_extra = {
            "example": {
                "question": "Why is my risk high?",
                "patient_features": {
                    "age": 45,
                    "bp": 130,
                    "cholesterol": 210,
                    "bmi": 28.5,
                    "diabetes": 1,
                    "smoking": 0,
                    "radiation_dose": 38.0,
                    "treatment_site": "left_chest",
                    "sessions": 25
                }
            }
        }


class AgentResponse(BaseModel):
    """Response from AI medical agent"""
    answer: str
    context_used: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)
