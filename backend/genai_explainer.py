import os
from typing import Dict, Optional
from schemas import PatientFeatures
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_explanation(
    risk_score: float,
    risk_level: str,
    features: PatientFeatures,
    feature_importance: Optional[Dict[str, float]] = None
) -> str:
    """
    Generate clinical explanation for risk prediction
    
    Args:
        risk_score: Predicted risk probability (0-1)
        risk_level: Risk level (Low/Medium/High)
        features: Patient features
        feature_importance: Optional SHAP feature importance scores
        
    Returns:
        Clinical explanation string
    """
    
    # Use LLM if API key is available, otherwise use template-based explanation
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if openai_key:
        try:
            return _generate_llm_explanation(risk_score, risk_level, features, feature_importance)
        except Exception as e:
            logger.warning(f"LLM explanation failed: {str(e)}, using template")
            return _generate_template_explanation(risk_score, risk_level, features, feature_importance)
    else:
        return _generate_template_explanation(risk_score, risk_level, features, feature_importance)


def _generate_llm_explanation(
    risk_score: float,
    risk_level: str,
    features: PatientFeatures,
    feature_importance: Optional[Dict[str, float]] = None
) -> str:
    """Generate explanation using OpenAI LLM"""
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    
    # Prepare feature importance text
    importance_text = ""
    if feature_importance:
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        importance_text = "\n".join([f"- {feat}: {imp:.2%}" for feat, imp in sorted_features[:5]])
    
    # Create prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a clinical AI assistant specializing in cardiovascular risk assessment 
        for radiotherapy patients. Provide clear, professional explanations of risk predictions."""),
        ("user", """Analyze this patient's cardiovascular risk:

Risk Score: {risk_score:.1%}
Risk Level: {risk_level}

Patient Profile:
- Age: {age} years
- Blood Pressure: {bp} mmHg
- Cholesterol: {cholesterol} mg/dL
- BMI: {bmi:.1f}
- Diabetes: {diabetes_status}
- Smoking: {smoking_status}
- Radiation Dose: {radiation_dose} Gy
- Treatment Site: {treatment_site}
- Treatment Sessions: {sessions}

{importance_section}

Provide a concise clinical explanation (2-3 sentences) focusing on:
1. The primary risk factors contributing to this assessment
2. The specific impact of radiotherapy exposure
3. Key clinical considerations

Keep the tone professional but accessible.""")
    ])
    
    # Format the prompt
    diabetes_status = "Yes" if features.diabetes == 1 else "No"
    smoking_status = "Yes" if features.smoking == 1 else "No"
    importance_section = f"Top Contributing Factors:\n{importance_text}" if importance_text else ""
    
    formatted_prompt = prompt.format_messages(
        risk_score=risk_score,
        risk_level=risk_level,
        age=features.age,
        bp=features.bp,
        cholesterol=features.cholesterol,
        bmi=features.bmi,
        diabetes_status=diabetes_status,
        smoking_status=smoking_status,
        radiation_dose=features.radiation_dose,
        treatment_site=features.treatment_site,
        sessions=features.sessions,
        importance_section=importance_section
    )
    
    # Get LLM response
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
    response = llm.invoke(formatted_prompt)
    
    return response.content


def _generate_template_explanation(
    risk_score: float,
    risk_level: str,
    features: PatientFeatures,
    feature_importance: Optional[Dict[str, float]] = None
) -> str:
    """Generate explanation using template-based approach"""
    
    explanation_parts = []
    
    # Opening statement based on risk level
    if risk_level == "High":
        explanation_parts.append(
            f"This patient presents with HIGH cardiovascular risk ({risk_score:.1%} probability)."
        )
    elif risk_level == "Medium":
        explanation_parts.append(
            f"This patient presents with MODERATE cardiovascular risk ({risk_score:.1%} probability)."
        )
    else:
        explanation_parts.append(
            f"This patient presents with LOW cardiovascular risk ({risk_score:.1%} probability)."
        )
    
    # Identify key risk factors
    risk_factors = []
    
    # Radiation exposure
    if features.radiation_dose > 30:
        risk_factors.append(
            f"elevated radiation exposure ({features.radiation_dose} Gy to {features.treatment_site})"
        )
    elif features.radiation_dose > 0:
        risk_factors.append(
            f"moderate radiation exposure ({features.radiation_dose} Gy)"
        )
    
    # Cardiovascular factors
    if features.bp > 140:
        risk_factors.append(f"hypertension (BP: {features.bp} mmHg)")
    elif features.bp > 130:
        risk_factors.append(f"elevated blood pressure ({features.bp} mmHg)")
    
    if features.cholesterol > 240:
        risk_factors.append(f"high cholesterol ({features.cholesterol} mg/dL)")
    elif features.cholesterol > 200:
        risk_factors.append(f"elevated cholesterol ({features.cholesterol} mg/dL)")
    
    # Metabolic factors
    if features.diabetes == 1:
        risk_factors.append("diabetes mellitus")
    
    if features.bmi > 30:
        risk_factors.append(f"obesity (BMI: {features.bmi:.1f})")
    elif features.bmi > 25:
        risk_factors.append(f"overweight (BMI: {features.bmi:.1f})")
    
    # Lifestyle factors
    if features.smoking == 1:
        risk_factors.append("active smoking")
    
    # Age factor
    if features.age > 65:
        risk_factors.append(f"advanced age ({features.age} years)")
    elif features.age > 50:
        risk_factors.append(f"age-related risk ({features.age} years)")
    
    # Build explanation
    if risk_factors:
        if len(risk_factors) == 1:
            explanation_parts.append(f"The primary contributing factor is {risk_factors[0]}.")
        elif len(risk_factors) == 2:
            explanation_parts.append(
                f"Key contributing factors include {risk_factors[0]} and {risk_factors[1]}."
            )
        else:
            factors_text = ", ".join(risk_factors[:-1]) + f", and {risk_factors[-1]}"
            explanation_parts.append(f"Multiple risk factors are present, including {factors_text}.")
    
    # Radiotherapy-specific considerations
    if features.radiation_dose > 0:
        if features.treatment_site.lower() in ['left_chest', 'chest']:
            explanation_parts.append(
                f"The {features.sessions}-session radiotherapy course to the {features.treatment_site} "
                "poses additional cardiac risk due to proximity to the heart."
            )
        else:
            explanation_parts.append(
                f"The {features.sessions}-session radiotherapy course may contribute to "
                "long-term cardiovascular effects."
            )
    
    # Clinical recommendations based on risk level
    if risk_level == "High":
        explanation_parts.append(
            "Close cardiovascular monitoring and aggressive risk factor modification are strongly recommended."
        )
    elif risk_level == "Medium":
        explanation_parts.append(
            "Regular cardiovascular monitoring and lifestyle modifications are advised."
        )
    else:
        explanation_parts.append(
            "Routine cardiovascular surveillance is recommended as part of standard care."
        )
    
    return " ".join(explanation_parts)


def get_risk_recommendations(risk_level: str, features: PatientFeatures) -> list:
    """
    Generate clinical recommendations based on risk level and patient features
    """
    recommendations = []
    
    if risk_level == "High":
        recommendations.append("Immediate cardiology consultation recommended")
        recommendations.append("Consider cardiac imaging (echocardiogram, stress test)")
        recommendations.append("Aggressive risk factor modification required")
    
    if features.bp > 140:
        recommendations.append("Optimize blood pressure control (target <130/80 mmHg)")
    
    if features.cholesterol > 200:
        recommendations.append("Initiate or intensify lipid-lowering therapy")
    
    if features.diabetes == 1:
        recommendations.append("Optimize glycemic control (HbA1c <7%)")
    
    if features.smoking == 1:
        recommendations.append("Smoking cessation counseling and support")
    
    if features.bmi > 25:
        recommendations.append("Weight management and dietary counseling")
    
    if features.radiation_dose > 30:
        recommendations.append("Long-term cardiac surveillance protocol")
        recommendations.append("Consider cardioprotective medications")
    
    recommendations.append("Regular exercise (150 min/week moderate activity)")
    recommendations.append("Mediterranean diet or DASH diet recommended")
    
    return recommendations
