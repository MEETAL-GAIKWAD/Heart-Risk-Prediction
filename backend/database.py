from pymongo import MongoClient
from typing import List, Optional
from datetime import datetime
from schemas import PatientRecord, PatientFeatures, RiskPredictionResponse
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    """MongoDB database handler"""
    
    def __init__(self):
        # Get MongoDB connection string from environment
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        
        try:
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client['heart_risk_db']
            self.patients = self.db['patients']
            self.predictions = self.db['predictions']
            
            # Test connection
            self.client.server_info()
            logger.info("Connected to MongoDB successfully")
            
            # Create indexes
            self.predictions.create_index([("created_at", -1)])
            self.predictions.create_index([("patient_id", 1)])
            
        except Exception as e:
            logger.warning(f"MongoDB connection failed: {str(e)}. Using in-memory storage.")
            self.client = None
            self.db = None
            self.patients = None
            self.predictions = None
            # Fallback to in-memory storage
            self._memory_storage = []
    
    def save_prediction(
        self,
        patient_id: Optional[str],
        features: PatientFeatures,
        prediction: RiskPredictionResponse
    ) -> str:
        """
        Save a prediction record
        
        Args:
            patient_id: Optional patient identifier
            features: Patient features
            prediction: Prediction result
            
        Returns:
            Record ID
        """
        record = {
            'patient_id': patient_id,
            'features': features.model_dump(),
            'prediction': {
                'risk_probability': prediction.risk_probability,
                'risk_level': prediction.risk_level,
                'explanation': prediction.explanation,
                'feature_importance': prediction.feature_importance
            },
            'created_at': datetime.now()
        }
        
        if self.predictions is not None:
            try:
                result = self.predictions.insert_one(record)
                logger.info(f"Saved prediction record: {result.inserted_id}")
                return str(result.inserted_id)
            except Exception as e:
                logger.error(f"Error saving to MongoDB: {str(e)}")
                # Fallback to memory
                self._memory_storage.append(record)
                return f"mem_{len(self._memory_storage)}"
        else:
            # Use in-memory storage
            self._memory_storage.append(record)
            return f"mem_{len(self._memory_storage)}"
    
    def get_patient_history(
        self,
        patient_id: Optional[str] = None,
        limit: int = 100
    ) -> List[dict]:
        """
        Get prediction history
        
        Args:
            patient_id: Optional patient ID to filter by
            limit: Maximum number of records to return
            
        Returns:
            List of prediction records
        """
        if self.predictions is not None:
            try:
                query = {}
                if patient_id:
                    query['patient_id'] = patient_id
                
                cursor = self.predictions.find(query).sort('created_at', -1).limit(limit)
                records = list(cursor)
                
                # Convert ObjectId to string
                for record in records:
                    record['_id'] = str(record['_id'])
                
                logger.info(f"Retrieved {len(records)} records")
                return records
                
            except Exception as e:
                logger.error(f"Error retrieving from MongoDB: {str(e)}")
                return self._memory_storage[-limit:]
        else:
            # Use in-memory storage
            if patient_id:
                filtered = [r for r in self._memory_storage if r.get('patient_id') == patient_id]
                return filtered[-limit:]
            return self._memory_storage[-limit:]
    
    def get_statistics(self) -> dict:
        """Get database statistics"""
        if self.predictions is not None:
            try:
                total_predictions = self.predictions.count_documents({})
                
                # Risk level distribution
                pipeline = [
                    {
                        '$group': {
                            '_id': '$prediction.risk_level',
                            'count': {'$sum': 1}
                        }
                    }
                ]
                risk_distribution = list(self.predictions.aggregate(pipeline))
                
                # Average risk by level
                avg_pipeline = [
                    {
                        '$group': {
                            '_id': '$prediction.risk_level',
                            'avg_risk': {'$avg': '$prediction.risk_probability'}
                        }
                    }
                ]
                avg_risk = list(self.predictions.aggregate(avg_pipeline))
                
                return {
                    'total_predictions': total_predictions,
                    'risk_distribution': {item['_id']: item['count'] for item in risk_distribution},
                    'average_risk': {item['_id']: item['avg_risk'] for item in avg_risk}
                }
                
            except Exception as e:
                logger.error(f"Error getting statistics: {str(e)}")
                return self._get_memory_statistics()
        else:
            return self._get_memory_statistics()
    
    def _get_memory_statistics(self) -> dict:
        """Get statistics from in-memory storage"""
        if not self._memory_storage:
            return {
                'total_predictions': 0,
                'risk_distribution': {},
                'average_risk': {}
            }
        
        total = len(self._memory_storage)
        risk_dist = {}
        risk_sums = {}
        
        for record in self._memory_storage:
            level = record['prediction']['risk_level']
            risk_dist[level] = risk_dist.get(level, 0) + 1
            risk_sums[level] = risk_sums.get(level, 0) + record['prediction']['risk_probability']
        
        avg_risk = {level: risk_sums[level] / risk_dist[level] for level in risk_dist}
        
        return {
            'total_predictions': total,
            'risk_distribution': risk_dist,
            'average_risk': avg_risk
        }
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")


# Global database instance
_db_instance = None


def get_database() -> Database:
    """Get or create the global database instance"""
    global _db_instance
    
    if _db_instance is None:
        _db_instance = Database()
    
    return _db_instance
