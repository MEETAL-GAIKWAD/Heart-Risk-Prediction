import os
from typing import Optional, List
from schemas import PatientFeatures, RiskPredictionResponse, AgentQuery, AgentResponse
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MedicalAIAgent:
    """AI agent for answering medical questions about risk predictions"""
    
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.use_llm = self.openai_key is not None
    
    def answer_question(
        self,
        question: str,
        patient_features: Optional[PatientFeatures] = None,
        prediction_result: Optional[RiskPredictionResponse] = None
    ) -> AgentResponse:
        """
        Answer a medical question about risk prediction
        
        Args:
            question: User's question
            patient_features: Optional patient features for context
            prediction_result: Optional prediction result for context
            
        Returns:
            AgentResponse with answer and context used
        """
        
        if self.use_llm:
            try:
                return self._answer_with_llm(question, patient_features, prediction_result)
            except Exception as e:
                logger.warning(f"LLM answer failed: {str(e)}, using template")
                return self._answer_with_template(question, patient_features, prediction_result)
        else:
            return self._answer_with_template(question, patient_features, prediction_result)
    
    def _answer_with_llm(
        self,
        question: str,
        patient_features: Optional[PatientFeatures],
        prediction_result: Optional[RiskPredictionResponse]
    ) -> AgentResponse:
        """Answer using OpenAI LLM"""
        from langchain_openai import ChatOpenAI
        from langchain.prompts import ChatPromptTemplate
        
        # Build context
        context_parts = []
        
        if patient_features:
            context_parts.append(f"""
Patient Profile:
- Age: {patient_features.age} years
- Blood Pressure: {patient_features.bp} mmHg
- Cholesterol: {patient_features.cholesterol} mg/dL
- BMI: {patient_features.bmi:.1f}
- Diabetes: {'Yes' if patient_features.diabetes == 1 else 'No'}
- Smoking: {'Yes' if patient_features.smoking == 1 else 'No'}
- Radiation Dose: {patient_features.radiation_dose} Gy
- Treatment Site: {patient_features.treatment_site}
- Treatment Sessions: {patient_features.sessions}
""")
        
        if prediction_result:
            context_parts.append(f"""
Risk Assessment:
- Risk Probability: {prediction_result.risk_probability:.1%}
- Risk Level: {prediction_result.risk_level}
- Explanation: {prediction_result.explanation}
""")
            
            if prediction_result.feature_importance:
                sorted_features = sorted(
                    prediction_result.feature_importance.items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                importance_text = "\n".join([
                    f"  - {feat}: {imp:.1%}" for feat, imp in sorted_features[:5]
                ])
                context_parts.append(f"""
Top Contributing Factors:
{importance_text}
""")
        
        context = "\n".join(context_parts)
        
        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a medical AI assistant specializing in cardiovascular risk assessment 
            for radiotherapy patients. Provide accurate, evidence-based answers to patient questions.
            
            Guidelines:
            - Be clear and professional
            - Explain medical concepts in accessible language
            - Reference specific patient data when available
            - Emphasize that this is a risk assessment tool, not a diagnosis
            - Recommend consulting with healthcare providers for medical decisions
            """),
            ("user", """Context:
{context}

Patient Question: {question}

Provide a helpful, accurate answer based on the available information.""")
        ])
        
        formatted_prompt = prompt.format_messages(
            context=context if context else "No patient data available.",
            question=question
        )
        
        # Get LLM response
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
        response = llm.invoke(formatted_prompt)
        
        # Track context used
        context_used = []
        if patient_features:
            context_used.append("patient_features")
        if prediction_result:
            context_used.append("prediction_result")
            if prediction_result.feature_importance:
                context_used.append("feature_importance")
        
        return AgentResponse(
            answer=response.content,
            context_used=context_used,
            timestamp=datetime.now()
        )
    
    def _answer_with_template(
        self,
        question: str,
        patient_features: Optional[PatientFeatures],
        prediction_result: Optional[RiskPredictionResponse]
    ) -> AgentResponse:
        """Answer using template-based approach"""
        
        question_lower = question.lower()
        context_used = []
        
        # Pattern matching for common questions
        if any(word in question_lower for word in ['why', 'high', 'risk']):
            answer = self._explain_high_risk(patient_features, prediction_result)
            context_used = ["patient_features", "prediction_result"]
        
        elif any(word in question_lower for word in ['factor', 'contribute', 'cause']):
            answer = self._explain_factors(patient_features, prediction_result)
            context_used = ["patient_features", "feature_importance"]
        
        elif any(word in question_lower for word in ['radiation', 'dose', 'radiotherapy']):
            answer = self._explain_radiation(patient_features)
            context_used = ["patient_features"]
        
        elif any(word in question_lower for word in ['improve', 'reduce', 'lower']):
            answer = self._suggest_improvements(patient_features, prediction_result)
            context_used = ["patient_features", "prediction_result"]
        
        elif any(word in question_lower for word in ['what', 'mean', 'explain']):
            answer = self._explain_prediction(prediction_result)
            context_used = ["prediction_result"]
        
        else:
            answer = self._general_answer(question, patient_features, prediction_result)
            context_used = ["general_knowledge"]
        
        return AgentResponse(
            answer=answer,
            context_used=context_used,
            timestamp=datetime.now()
        )
    
    def _explain_high_risk(
        self,
        features: Optional[PatientFeatures],
        prediction: Optional[RiskPredictionResponse]
    ) -> str:
        """Explain why risk is high"""
        if not prediction:
            return "I need prediction results to explain the risk level."
        
        if prediction.risk_level == "Low":
            return f"Your risk is actually LOW ({prediction.risk_probability:.1%}). {prediction.explanation}"
        
        answer = f"Your risk is {prediction.risk_level} ({prediction.risk_probability:.1%}). "
        
        if features:
            risk_factors = []
            if features.radiation_dose > 30:
                risk_factors.append(f"high radiation dose ({features.radiation_dose} Gy)")
            if features.bp > 140:
                risk_factors.append(f"elevated blood pressure ({features.bp} mmHg)")
            if features.cholesterol > 240:
                risk_factors.append(f"high cholesterol ({features.cholesterol} mg/dL)")
            if features.diabetes == 1:
                risk_factors.append("diabetes")
            if features.smoking == 1:
                risk_factors.append("smoking")
            if features.age > 65:
                risk_factors.append(f"age ({features.age} years)")
            
            if risk_factors:
                answer += "The main contributing factors are: " + ", ".join(risk_factors) + ". "
        
        answer += prediction.explanation
        return answer
    
    def _explain_factors(
        self,
        features: Optional[PatientFeatures],
        prediction: Optional[RiskPredictionResponse]
    ) -> str:
        """Explain contributing factors"""
        if not prediction or not prediction.feature_importance:
            return """The main factors affecting cardiovascular risk in radiotherapy patients include:
1. Radiation dose and treatment site
2. Blood pressure levels
3. Cholesterol levels
4. Age
5. Diabetes and smoking status
6. BMI and overall health"""
        
        sorted_features = sorted(
            prediction.feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        answer = "Based on your specific case, the top contributing factors are:\n\n"
        
        for i, (feat, importance) in enumerate(sorted_features[:5], 1):
            feat_name = feat.replace('_', ' ').title()
            answer += f"{i}. {feat_name}: {importance:.1%} contribution\n"
        
        answer += "\nThese factors were identified using advanced machine learning analysis of your health profile."
        return answer
    
    def _explain_radiation(self, features: Optional[PatientFeatures]) -> str:
        """Explain radiation impact"""
        if not features:
            return """Radiation therapy can affect the heart, especially when treating areas near the chest. 
The risk depends on the total dose, treatment site, and number of sessions. Modern techniques 
minimize cardiac exposure, but long-term monitoring is important."""
        
        answer = f"Your treatment involves {features.radiation_dose} Gy delivered over {features.sessions} sessions to the {features.treatment_site}. "
        
        if features.radiation_dose > 30:
            answer += """This is a significant dose that requires careful cardiac monitoring. 
Radiation can cause inflammation and damage to heart tissue over time, potentially leading to 
coronary artery disease, valve problems, or heart muscle damage. """
        elif features.radiation_dose > 0:
            answer += """This is a moderate dose. While modern radiotherapy techniques minimize cardiac exposure, 
some risk remains, especially with chest treatments. """
        
        if features.treatment_site.lower() in ['left_chest', 'chest']:
            answer += """The treatment site is close to the heart, which increases the importance of 
cardiac monitoring and risk factor management."""
        
        return answer
    
    def _suggest_improvements(
        self,
        features: Optional[PatientFeatures],
        prediction: Optional[RiskPredictionResponse]
    ) -> str:
        """Suggest risk reduction strategies"""
        if not features:
            return """General strategies to reduce cardiovascular risk:
1. Maintain healthy blood pressure (<130/80 mmHg)
2. Control cholesterol levels
3. Quit smoking
4. Maintain healthy weight (BMI 18.5-24.9)
5. Regular exercise (150 min/week)
6. Healthy diet (Mediterranean or DASH diet)
7. Manage diabetes if present
8. Regular cardiac monitoring"""
        
        suggestions = []
        
        if features.bp > 130:
            suggestions.append("• Control blood pressure through medication, diet (low sodium), and stress management")
        
        if features.cholesterol > 200:
            suggestions.append("• Lower cholesterol with statins, dietary changes, and increased fiber intake")
        
        if features.smoking == 1:
            suggestions.append("• Quit smoking - this is one of the most impactful changes you can make")
        
        if features.bmi > 25:
            suggestions.append("• Achieve healthy weight through balanced diet and regular exercise")
        
        if features.diabetes == 1:
            suggestions.append("• Optimize blood sugar control (target HbA1c <7%)")
        
        suggestions.append("• Regular cardiovascular exercise (150 minutes per week)")
        suggestions.append("• Follow a heart-healthy diet (Mediterranean or DASH diet)")
        suggestions.append("• Regular cardiac monitoring and follow-up appointments")
        
        answer = "Here are personalized recommendations to reduce your cardiovascular risk:\n\n"
        answer += "\n".join(suggestions)
        answer += "\n\nAlways consult with your healthcare provider before making significant lifestyle changes."
        
        return answer
    
    def _explain_prediction(self, prediction: Optional[RiskPredictionResponse]) -> str:
        """Explain the prediction"""
        if not prediction:
            return "I need prediction results to provide an explanation."
        
        return f"""Your cardiovascular risk assessment shows:

Risk Level: {prediction.risk_level}
Risk Probability: {prediction.risk_probability:.1%}

{prediction.explanation}

This assessment is based on machine learning analysis of your health profile and radiotherapy 
treatment parameters. It helps identify patients who may benefit from closer monitoring and 
preventive interventions."""
    
    def _general_answer(
        self,
        question: str,
        features: Optional[PatientFeatures],
        prediction: Optional[RiskPredictionResponse]
    ) -> str:
        """General answer for unmatched questions"""
        return """I'm here to help answer questions about cardiovascular risk assessment for radiotherapy patients.

I can help with:
- Explaining your risk level and contributing factors
- Understanding the impact of radiation therapy on heart health
- Identifying ways to reduce your cardiovascular risk
- Interpreting your risk assessment results

Please ask a specific question, and I'll provide detailed information based on your health profile."""


def get_ai_agent() -> MedicalAIAgent:
    """Get AI agent instance"""
    return MedicalAIAgent()
