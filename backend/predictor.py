from typing import Tuple
from schemas import PatientFeatures
from model_loader import get_model
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def predict_risk(features: PatientFeatures) -> Tuple[float, str]:
    """
    Predict heart risk based on patient features
    
    Args:
        features: PatientFeatures object with patient data
        
    Returns:
        Tuple of (risk_probability, risk_level)
        
    Risk levels:
        - Low: 0.0 - 0.35
        - Medium: 0.35 - 0.70
        - High: 0.70+
    """
    try:
        # Get model (for encoding)
        model = get_model()
        
        # Use rule-based prediction
        risk_probability, risk_level = _calculate_risk(features)
        
        logger.info(f"Prediction: {risk_probability:.3f} ({risk_level})")
        
        return risk_probability, risk_level
        
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return _calculate_risk(features)


def _calculate_risk(features: PatientFeatures) -> Tuple[float, str]:
    """
    Rule-based prediction using clinical risk factors
    """
    risk_score = 0.0
    
    # Age factor (0-0.25)
    if features.age > 65:
        risk_score += 0.25
    elif features.age > 50:
        risk_score += 0.15
    elif features.age > 35:
        risk_score += 0.05
    
    # Blood pressure factor (0-0.20)
    if features.bp > 140:
        risk_score += 0.20
    elif features.bp > 130:
        risk_score += 0.12
    elif features.bp > 120:
        risk_score += 0.05
    
    # Cholesterol factor (0-0.15)
    if features.cholesterol > 240:
        risk_score += 0.15
    elif features.cholesterol > 200:
        risk_score += 0.08
    
    # BMI factor (0-0.10)
    if features.bmi > 30:
        risk_score += 0.10
    elif features.bmi > 25:
        risk_score += 0.05
    
    # Diabetes factor (0-0.10)
    if features.diabetes == 1:
        risk_score += 0.10
    
    # Smoking factor (0-0.10)
    if features.smoking == 1:
        risk_score += 0.10
    
    # Radiation dose factor (0-0.30) - most important for radiotherapy patients
    radiation_factor = min(features.radiation_dose / 100, 0.30)
    risk_score += radiation_factor
    
    # Sessions factor (0-0.10)
    if features.sessions > 30:
        risk_score += 0.10
    elif features.sessions > 20:
        risk_score += 0.05
    
    # Treatment site factor (0-0.05)
    if features.treatment_site.lower() in ['left_chest', 'chest']:
        risk_score += 0.05
    
    # Normalize to 0-1 range
    risk_probability = min(risk_score, 1.0)
    
    # Determine risk level
    if risk_probability < 0.35:
        risk_level = "Low"
    elif risk_probability < 0.70:
        risk_level = "Medium"
    else:
        risk_level = "High"
    
    return risk_probability, risk_level



def get_risk_factors(features: PatientFeatures) -> dict:
    """
    Identify which risk factors are present for a patient
    """
    factors = {}
    
    if features.age > 50:
        factors['age'] = f"Age {features.age} (elevated risk)"
    
    if features.bp > 130:
        factors['blood_pressure'] = f"BP {features.bp} mmHg (hypertension)"
    
    if features.cholesterol > 200:
        factors['cholesterol'] = f"Cholesterol {features.cholesterol} mg/dL (elevated)"
    
    if features.bmi > 25:
        factors['bmi'] = f"BMI {features.bmi:.1f} (overweight/obese)"
    
    if features.diabetes == 1:
        factors['diabetes'] = "Diabetes present"
    
    if features.smoking == 1:
        factors['smoking'] = "Active smoker"
    
    if features.radiation_dose > 30:
        factors['radiation'] = f"High radiation dose ({features.radiation_dose} Gy)"
    elif features.radiation_dose > 0:
        factors['radiation'] = f"Radiation exposure ({features.radiation_dose} Gy)"
    
    if features.sessions > 20:
        factors['sessions'] = f"Multiple treatment sessions ({features.sessions})"
    
    return factors
