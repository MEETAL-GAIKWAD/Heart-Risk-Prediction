from typing import Dict
from schemas import PatientFeatures
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_feature_importance(features: PatientFeatures) -> Dict[str, float]:
    """
    Calculate rule-based feature importance for a single prediction
    
    Args:
        features: PatientFeatures object
        
    Returns:
        Dictionary mapping feature names to importance scores
    """
    importance = {}
    total_score = 0
    
    # Radiation dose - typically most important for radiotherapy patients
    radiation_score = min(features.radiation_dose / 50, 1.0) * 0.35
    importance['radiation_dose'] = radiation_score
    total_score += radiation_score
    
    # Blood pressure
    bp_score = 0.25 if features.bp > 140 else (0.15 if features.bp > 130 else 0.08)
    importance['bp'] = bp_score
    total_score += bp_score
    
    # Cholesterol
    chol_score = 0.20 if features.cholesterol > 240 else (0.12 if features.cholesterol > 200 else 0.05)
    importance['cholesterol'] = chol_score
    total_score += chol_score
    
    # Age
    age_score = 0.18 if features.age > 65 else (0.12 if features.age > 50 else 0.05)
    importance['age'] = age_score
    total_score += age_score
    
    # BMI
    bmi_score = 0.12 if features.bmi > 30 else (0.08 if features.bmi > 25 else 0.03)
    importance['bmi'] = bmi_score
    total_score += bmi_score
    
    # Diabetes
    diabetes_score = 0.15 if features.diabetes == 1 else 0.02
    importance['diabetes'] = diabetes_score
    total_score += diabetes_score
    
    # Smoking
    smoking_score = 0.15 if features.smoking == 1 else 0.02
    importance['smoking'] = smoking_score
    total_score += smoking_score
    
    # Treatment sessions
    sessions_score = 0.10 if features.sessions > 30 else (0.06 if features.sessions > 20 else 0.03)
    importance['sessions'] = sessions_score
    total_score += sessions_score
    
    # Treatment site
    site_score = 0.08 if features.treatment_site.lower() in ['left_chest', 'chest'] else 0.03
    importance['treatment_site'] = site_score
    total_score += site_score
    
    # Normalize
    if total_score > 0:
        importance = {k: v / total_score for k, v in importance.items()}
    
    logger.info(f"Feature importance calculated: {importance}")
    return importance
