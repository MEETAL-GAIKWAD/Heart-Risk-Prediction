from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import tempfile
import os
from pathlib import Path

from schemas import (
    PatientFeatures,
    RiskPredictionResponse,
    PatientHistoryResponse,
    UploadReportResponse,
    AgentQuery,
    AgentResponse,
    PatientRecord
)
from predictor import predict_risk, get_risk_factors
from genai_explainer import generate_explanation, get_risk_recommendations
from shap_explainer import calculate_feature_importance
from report_parser import parse_medical_report
from ai_agent import get_ai_agent
from database import get_database
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Heart Risk Prediction API",
    description="Real-Time AI-Powered Heart Risk Prediction System with Radiotherapy Intelligence",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Heart Risk Prediction API...")
    
    # Initialize database
    db = get_database()
    logger.info("Database initialized")
    
    # Load model
    from model_loader import get_model
    model = get_model()
    logger.info(f"Model loaded: {model.is_trained}")
    
    logger.info("API ready to serve requests")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down API...")
    db = get_database()
    db.close()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Heart Risk Prediction API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "predict": "/predict-risk",
            "upload": "/upload-report",
            "history": "/patient-history",
            "agent": "/ask-agent",
            "stats": "/statistics"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from model_loader import get_model
    model = get_model()
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": model.is_trained,
        "database": "connected"
    }


@app.post("/predict-risk", response_model=RiskPredictionResponse)
async def predict_risk_endpoint(
    features: PatientFeatures,
    background_tasks: BackgroundTasks,
    patient_id: str = None
):
    """
    Predict cardiovascular risk based on patient features
    
    - **age**: Patient age in years (0-120)
    - **bp**: Systolic blood pressure in mmHg (60-200)
    - **cholesterol**: Cholesterol level in mg/dL (100-400)
    - **bmi**: Body Mass Index (10-60)
    - **diabetes**: Diabetes status (0=No, 1=Yes)
    - **smoking**: Smoking status (0=No, 1=Yes)
    - **radiation_dose**: Radiation dose in Gy (0-100)
    - **treatment_site**: Treatment site (e.g., left_chest, right_chest)
    - **sessions**: Number of radiotherapy sessions (0-50)
    
    Returns risk probability, risk level, and clinical explanation
    """
    start_time = time.time()
    
    try:
        logger.info(f"Prediction request for patient: {patient_id}")
        
        # Step 1: Predict risk
        risk_probability, risk_level = predict_risk(features)
        
        # Step 2: Calculate feature importance (SHAP)
        feature_importance = calculate_feature_importance(features)
        
        # Step 3: Generate explanation
        explanation = generate_explanation(
            risk_probability,
            risk_level,
            features,
            feature_importance
        )
        
        # Create response
        response = RiskPredictionResponse(
            risk_probability=risk_probability,
            risk_level=risk_level,
            explanation=explanation,
            feature_importance=feature_importance,
            timestamp=datetime.now()
        )
        
        # Save to database (background task)
        background_tasks.add_task(
            save_prediction_to_db,
            patient_id,
            features,
            response
        )
        
        # Log performance
        elapsed_time = (time.time() - start_time) * 1000
        logger.info(f"Prediction completed in {elapsed_time:.2f}ms")
        
        if elapsed_time > 200:
            logger.warning(f"Prediction took longer than target: {elapsed_time:.2f}ms")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/upload-report", response_model=UploadReportResponse)
async def upload_report(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    patient_id: str = None
):
    """
    Upload and parse medical report (PDF)
    
    Extracts patient features from the report and returns risk prediction
    """
    start_time = time.time()
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        logger.info(f"Processing uploaded report: {file.filename}")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Parse report
            extracted_features, raw_text = parse_medical_report(tmp_path)
            logger.info(f"Extracted features from report")
            
            # Predict risk
            risk_probability, risk_level = predict_risk(extracted_features)
            
            # Calculate feature importance
            feature_importance = calculate_feature_importance(extracted_features)
            
            # Generate explanation
            explanation = generate_explanation(
                risk_probability,
                risk_level,
                extracted_features,
                feature_importance
            )
            
            # Create prediction response
            prediction = RiskPredictionResponse(
                risk_probability=risk_probability,
                risk_level=risk_level,
                explanation=explanation,
                feature_importance=feature_importance,
                timestamp=datetime.now()
            )
            
            # Save to database (background task)
            if background_tasks:
                background_tasks.add_task(
                    save_prediction_to_db,
                    patient_id,
                    extracted_features,
                    prediction
                )
            
            # Create response
            response = UploadReportResponse(
                extracted_features=extracted_features,
                prediction=prediction,
                raw_text=raw_text
            )
            
            elapsed_time = (time.time() - start_time) * 1000
            logger.info(f"Report processed in {elapsed_time:.2f}ms")
            
            return response
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_path)
            
    except Exception as e:
        logger.error(f"Error processing report: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Report processing failed: {str(e)}")


@app.get("/patient-history")
async def get_patient_history(
    patient_id: str = None,
    limit: int = 100
):
    """
    Get patient prediction history
    
    - **patient_id**: Optional patient ID to filter by
    - **limit**: Maximum number of records to return (default: 100)
    """
    try:
        db = get_database()
        records = db.get_patient_history(patient_id, limit)
        
        return {
            "records": records,
            "total_count": len(records),
            "patient_id": patient_id
        }
        
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")


@app.post("/ask-agent", response_model=AgentResponse)
async def ask_agent(query: AgentQuery):
    """
    Ask the AI medical agent a question
    
    The agent can answer questions about:
    - Risk assessment results
    - Contributing factors
    - Radiation therapy impact
    - Risk reduction strategies
    """
    try:
        logger.info(f"Agent query: {query.question}")
        
        agent = get_ai_agent()
        response = agent.answer_question(
            query.question,
            query.patient_features,
            query.prediction_result
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error in agent query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Agent query failed: {str(e)}")


@app.get("/statistics")
async def get_statistics():
    """Get database statistics"""
    try:
        db = get_database()
        stats = db.get_statistics()
        return stats
        
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")


@app.get("/risk-recommendations")
async def get_recommendations(risk_level: str):
    """
    Get clinical recommendations based on risk level
    
    - **risk_level**: Risk level (Low, Medium, High)
    """
    try:
        from genai_explainer import get_risk_recommendations
        from schemas import PatientFeatures
        
        # Create dummy features for general recommendations
        dummy_features = PatientFeatures(
            age=50, bp=120, cholesterol=200, bmi=25.0,
            diabetes=0, smoking=0, radiation_dose=0,
            treatment_site="unknown", sessions=0
        )
        
        recommendations = get_risk_recommendations(risk_level, dummy_features)
        
        return {
            "risk_level": risk_level,
            "recommendations": recommendations
        }
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")


# Background task functions
def save_prediction_to_db(
    patient_id: str,
    features: PatientFeatures,
    prediction: RiskPredictionResponse
):
    """Background task to save prediction to database"""
    try:
        db = get_database()
        record_id = db.save_prediction(patient_id, features, prediction)
        logger.info(f"Saved prediction to database: {record_id}")
    except Exception as e:
        logger.error(f"Error saving to database: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
