"""
Script to train the heart risk prediction model
Run this before starting the API server
"""

import sys
from pathlib import Path
from model_loader import HeartRiskModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Train and save the model"""
    logger.info("Starting model training...")
    
    # Check if dataset exists
    dataset_path = Path("../cleaned_heart_risk_dataset.csv")
    if not dataset_path.exists():
        logger.error(f"Dataset not found at {dataset_path}")
        logger.error("Please ensure cleaned_heart_risk_dataset.csv is in the parent directory")
        sys.exit(1)
    
    # Create model
    model = HeartRiskModel()
    
    # Train model
    success = model.train_model(str(dataset_path))
    
    if not success:
        logger.error("Model training failed")
        sys.exit(1)
    
    # Save model
    model_path = Path("trained_model.pkl")
    model.save_model(str(model_path))
    
    logger.info(f"Model successfully trained and saved to {model_path}")
    logger.info("You can now start the API server with: uvicorn main:app --reload")


if __name__ == "__main__":
    main()
