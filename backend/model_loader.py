import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HeartRiskModel:
    """Heart risk prediction model wrapper - simplified version"""
    
    def __init__(self):
        self.is_trained = True  # Always ready
        self.feature_names = [
            'age', 'bp', 'cholesterol', 'bmi', 'diabetes', 
            'smoking', 'radiation_dose', 'treatment_site_encoded', 'sessions'
        ]
        logger.info("Model initialized (rule-based)")
    
    def encode_treatment_site(self, site: str) -> int:
        """Encode treatment site to numeric value"""
        site_map = {
            'left_chest': 2,
            'right_chest': 1,
            'chest': 2,
            'abdomen': 0,
            'head_neck': 0,
            'pelvis': 0,
            'unknown': 0
        }
        return site_map.get(site.lower(), 0)


# Global model instance
_model_instance = None


def get_model() -> HeartRiskModel:
    """Get or create the global model instance"""
    global _model_instance
    
    if _model_instance is None:
        _model_instance = HeartRiskModel()
        logger.info("Model ready for predictions")
    
    return _model_instance
