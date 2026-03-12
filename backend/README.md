# Heart Risk Prediction Backend API

Real-Time AI-Powered Heart Risk Prediction System with Radiotherapy Intelligence - Backend Service

## Features

- ✅ FastAPI-based REST API
- ✅ Machine Learning risk prediction (Gradient Boosting)
- ✅ SHAP-based feature importance
- ✅ GenAI clinical explanations (OpenAI integration)
- ✅ PDF medical report parsing
- ✅ AI medical agent for Q&A
- ✅ MongoDB database integration
- ✅ <200ms prediction performance
- ✅ Comprehensive error handling and logging

## Architecture

```
backend/
├── main.py                 # FastAPI application
├── model_loader.py         # ML model training and loading
├── predictor.py            # Risk prediction logic
├── schemas.py              # Pydantic data models
├── genai_explainer.py      # GenAI explanation generation
├── shap_explainer.py       # SHAP feature importance
├── report_parser.py        # PDF report parsing
├── ai_agent.py             # AI medical agent
├── database.py             # MongoDB integration
├── train_model.py          # Model training script
├── requirements.txt        # Python dependencies
└── .env.example            # Environment variables template
```

## Installation

### Prerequisites

- Python 3.8+
- MongoDB (optional - falls back to in-memory storage)
- OpenAI API key (optional - for GenAI features)

### Setup

1. **Install dependencies:**

```bash
cd backend
pip install -r requirements.txt
```

2. **Configure environment variables:**

```bash
cp .env.example .env
# Edit .env and add your API keys
```

3. **Train the model:**

```bash
python train_model.py
```

This will:
- Load the cleaned dataset
- Train a Gradient Boosting model
- Save the trained model to `trained_model.pkl`

## Running the Server

### Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## API Endpoints

### 1. Predict Risk

**POST** `/predict-risk`

Predict cardiovascular risk based on patient features.

**Request Body:**
```json
{
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
```

**Response:**
```json
{
  "risk_probability": 0.81,
  "risk_level": "High",
  "explanation": "High cardiac risk due to elevated radiation dose...",
  "feature_importance": {
    "radiation_dose": 0.41,
    "bp": 0.22,
    "cholesterol": 0.18,
    "age": 0.12,
    "bmi": 0.07
  },
  "timestamp": "2026-03-12T10:30:00"
}
```

**Performance:** <200ms

### 2. Upload Report

**POST** `/upload-report`

Upload and parse a PDF medical report.

**Request:**
- Form data with PDF file
- Optional `patient_id` query parameter

**Response:**
```json
{
  "extracted_features": {
    "age": 45,
    "bp": 130,
    ...
  },
  "prediction": {
    "risk_probability": 0.81,
    "risk_level": "High",
    ...
  },
  "raw_text": "Extracted text from PDF..."
}
```

### 3. Patient History

**GET** `/patient-history?patient_id=P001&limit=100`

Get prediction history for a patient.

**Response:**
```json
{
  "records": [
    {
      "patient_id": "P001",
      "features": {...},
      "prediction": {...},
      "created_at": "2026-03-12T10:30:00"
    }
  ],
  "total_count": 10
}
```

### 4. Ask AI Agent

**POST** `/ask-agent`

Ask the AI medical agent a question.

**Request Body:**
```json
{
  "question": "Why is my risk high?",
  "patient_features": {...},
  "prediction_result": {...}
}
```

**Response:**
```json
{
  "answer": "Your risk is high primarily due to...",
  "context_used": ["patient_features", "prediction_result"],
  "timestamp": "2026-03-12T10:30:00"
}
```

### 5. Statistics

**GET** `/statistics`

Get database statistics.

**Response:**
```json
{
  "total_predictions": 150,
  "risk_distribution": {
    "Low": 45,
    "Medium": 60,
    "High": 45
  },
  "average_risk": {
    "Low": 0.22,
    "Medium": 0.52,
    "High": 0.83
  }
}
```

### 6. Health Check

**GET** `/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-12T10:30:00",
  "model_loaded": true,
  "database": "connected"
}
```

## Risk Levels

The system classifies risk into three levels:

- **Low**: 0.0 - 0.35 (0-35%)
- **Medium**: 0.35 - 0.70 (35-70%)
- **High**: 0.70+ (70-100%)

## Feature Importance

The system uses SHAP (SHapley Additive exPlanations) to calculate feature importance:

- **radiation_dose**: Radiation exposure in Gy
- **bp**: Systolic blood pressure
- **cholesterol**: Total cholesterol level
- **age**: Patient age
- **bmi**: Body Mass Index
- **diabetes**: Diabetes status
- **smoking**: Smoking status
- **treatment_site**: Radiotherapy treatment location
- **sessions**: Number of treatment sessions

## GenAI Integration

The system can use OpenAI's GPT models for enhanced explanations:

1. Set `OPENAI_API_KEY` in `.env`
2. The system will automatically use GPT-3.5-turbo for:
   - Clinical explanations
   - AI agent responses

If no API key is provided, the system falls back to template-based explanations.

## Database

### MongoDB (Recommended)

Set `MONGODB_URI` in `.env`:
```
MONGODB_URI=mongodb://localhost:27017/
```

### In-Memory Fallback

If MongoDB is unavailable, the system automatically uses in-memory storage.

## Performance Optimization

- Model loaded once at startup
- SHAP explainer initialized on first use
- Background tasks for database writes
- Efficient feature encoding
- Response time target: <200ms

## Error Handling

All endpoints include comprehensive error handling:

- Input validation (Pydantic)
- Model fallback (rule-based prediction)
- Database fallback (in-memory storage)
- Detailed error messages
- Logging for debugging

## Testing

### Test Prediction

```bash
curl -X POST "http://localhost:8000/predict-risk" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "bp": 130,
    "cholesterol": 210,
    "bmi": 28.5,
    "diabetes": 1,
    "smoking": 0,
    "radiation_dose": 38.0,
    "treatment_site": "left_chest",
    "sessions": 25
  }'
```

### Test Health Check

```bash
curl http://localhost:8000/health
```

## Deployment

### Docker (Recommended)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

Required:
- None (all features have fallbacks)

Optional:
- `OPENAI_API_KEY`: For GenAI features
- `MONGODB_URI`: For persistent storage
- `API_HOST`: API host (default: 0.0.0.0)
- `API_PORT`: API port (default: 8000)

## Monitoring

The API includes:

- Health check endpoint
- Performance logging
- Error tracking
- Request/response logging

## Security

- CORS configured (update for production)
- Input validation
- File upload validation
- Error message sanitization

## License

MIT License

## Support

For issues or questions, please open an issue on GitHub.
