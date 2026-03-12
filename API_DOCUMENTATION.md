# API Documentation
## Heart Risk Prediction System API

Base URL: `http://localhost:8000`

Interactive Docs: `http://localhost:8000/docs`

## Authentication

Currently, no authentication is required. For production, implement JWT or OAuth2.

## Endpoints Overview

| Method | Endpoint | Description | Performance |
|--------|----------|-------------|-------------|
| GET | `/` | Root endpoint | <10ms |
| GET | `/health` | Health check | <10ms |
| POST | `/predict-risk` | Predict risk | <200ms |
| POST | `/upload-report` | Upload PDF report | <2s |
| GET | `/patient-history` | Get history | <50ms |
| POST | `/ask-agent` | Ask AI agent | <1s |
| GET | `/statistics` | Get stats | <50ms |
| GET | `/risk-recommendations` | Get recommendations | <10ms |

---

## 1. Root Endpoint

### GET `/`

Get API information and available endpoints.

**Response:**
```json
{
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
```

---

## 2. Health Check

### GET `/health`

Check API health and model status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-12T10:30:00.000Z",
  "model_loaded": true,
  "database": "connected"
}
```

**Status Codes:**
- `200`: Healthy
- `503`: Service unavailable

---

## 3. Predict Risk

### POST `/predict-risk`

Predict cardiovascular risk based on patient features.

**Query Parameters:**
- `patient_id` (optional): Patient identifier for tracking

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

**Field Descriptions:**

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| age | integer | 0-120 | Patient age in years |
| bp | integer | 60-200 | Systolic blood pressure (mmHg) |
| cholesterol | integer | 100-400 | Total cholesterol (mg/dL) |
| bmi | float | 10-60 | Body Mass Index |
| diabetes | integer | 0-1 | Diabetes status (0=No, 1=Yes) |
| smoking | integer | 0-1 | Smoking status (0=No, 1=Yes) |
| radiation_dose | float | 0-100 | Radiation dose (Gy) |
| treatment_site | string | - | Treatment location |
| sessions | integer | 0-50 | Number of radiotherapy sessions |

**Treatment Sites:**
- `left_chest`
- `right_chest`
- `chest`
- `abdomen`
- `head_neck`
- `pelvis`
- `unknown`

**Response:**
```json
{
  "risk_probability": 0.81,
  "risk_level": "High",
  "explanation": "High cardiac risk due to elevated radiation dose of 38 Gy combined with hypertension (BP: 130 mmHg) and diabetes. The 25-session radiotherapy course to the left_chest poses additional cardiac risk due to proximity to the heart. Close cardiovascular monitoring and aggressive risk factor modification are strongly recommended.",
  "feature_importance": {
    "radiation_dose": 0.41,
    "bp": 0.22,
    "cholesterol": 0.18,
    "age": 0.12,
    "diabetes": 0.04,
    "bmi": 0.02,
    "smoking": 0.01,
    "treatment_site": 0.00,
    "sessions": 0.00
  },
  "timestamp": "2026-03-12T10:30:00.000Z"
}
```

**Risk Levels:**
- `Low`: 0.0 - 0.35 (0-35%)
- `Medium`: 0.35 - 0.70 (35-70%)
- `High`: 0.70+ (70-100%)

**Status Codes:**
- `200`: Success
- `422`: Validation error
- `500`: Server error

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/predict-risk?patient_id=P001" \
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

**Example (JavaScript):**
```javascript
const response = await fetch('http://localhost:8000/predict-risk', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    age: 45,
    bp: 130,
    cholesterol: 210,
    bmi: 28.5,
    diabetes: 1,
    smoking: 0,
    radiation_dose: 38.0,
    treatment_site: 'left_chest',
    sessions: 25
  })
});
const data = await response.json();
```

---

## 4. Upload Report

### POST `/upload-report`

Upload and parse a PDF medical report.

**Query Parameters:**
- `patient_id` (optional): Patient identifier

**Request:**
- Content-Type: `multipart/form-data`
- Field: `file` (PDF file)

**Response:**
```json
{
  "extracted_features": {
    "age": 45,
    "bp": 130,
    "cholesterol": 210,
    "bmi": 28.5,
    "diabetes": 1,
    "smoking": 0,
    "radiation_dose": 38.0,
    "treatment_site": "left_chest",
    "sessions": 25
  },
  "prediction": {
    "risk_probability": 0.81,
    "risk_level": "High",
    "explanation": "...",
    "feature_importance": {...},
    "timestamp": "2026-03-12T10:30:00.000Z"
  },
  "raw_text": "Patient Report\nAge: 45 years\nBlood Pressure: 130/85 mmHg..."
}
```

**Supported Formats:**
- PDF only

**Extraction Patterns:**
The parser looks for:
- Age: "age: 45", "45 years old"
- BP: "blood pressure: 130/85", "BP: 130"
- Cholesterol: "cholesterol: 210 mg/dL"
- BMI: "BMI: 28.5"
- Diabetes: "diabetes: yes/no"
- Smoking: "smoking: yes/no"
- Radiation: "radiation dose: 38 Gy"
- Treatment site: "treatment site: left_chest"
- Sessions: "sessions: 25"

**Status Codes:**
- `200`: Success
- `400`: Invalid file type
- `422`: Validation error
- `500`: Processing error

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/upload-report?patient_id=P001" \
  -F "file=@medical_report.pdf"
```

**Example (JavaScript):**
```javascript
const formData = new FormData();
formData.append('file', pdfFile);

const response = await fetch('http://localhost:8000/upload-report', {
  method: 'POST',
  body: formData
});
const data = await response.json();
```

---

## 5. Patient History

### GET `/patient-history`

Get prediction history records.

**Query Parameters:**
- `patient_id` (optional): Filter by patient ID
- `limit` (optional): Max records (default: 100)

**Response:**
```json
{
  "records": [
    {
      "_id": "65f1234567890abcdef12345",
      "patient_id": "P001",
      "features": {
        "age": 45,
        "bp": 130,
        ...
      },
      "prediction": {
        "risk_probability": 0.81,
        "risk_level": "High",
        ...
      },
      "created_at": "2026-03-12T10:30:00.000Z"
    }
  ],
  "total_count": 10,
  "patient_id": "P001"
}
```

**Status Codes:**
- `200`: Success
- `500`: Server error

**Example (cURL):**
```bash
curl "http://localhost:8000/patient-history?patient_id=P001&limit=50"
```

---

## 6. Ask AI Agent

### POST `/ask-agent`

Ask the AI medical agent a question about risk assessment.

**Request Body:**
```json
{
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
  },
  "prediction_result": {
    "risk_probability": 0.81,
    "risk_level": "High",
    "explanation": "...",
    "feature_importance": {...}
  }
}
```

**Common Questions:**
- "Why is my risk high?"
- "Which factor contributed most?"
- "What does radiation dose mean for heart risk?"
- "How can I reduce my risk?"
- "What is the impact of my blood pressure?"

**Response:**
```json
{
  "answer": "Your risk is High (81%) primarily due to several factors: high radiation dose (38 Gy), elevated blood pressure (130 mmHg), high cholesterol (210 mg/dL), and diabetes. The radiation dose is the strongest predictor at 41% contribution. The treatment site (left_chest) is close to the heart, which increases the importance of cardiac monitoring and risk factor management.",
  "context_used": [
    "patient_features",
    "prediction_result",
    "feature_importance"
  ],
  "timestamp": "2026-03-12T10:30:00.000Z"
}
```

**Status Codes:**
- `200`: Success
- `422`: Validation error
- `500`: Server error

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/ask-agent" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Why is my risk high?",
    "patient_features": {...}
  }'
```

---

## 7. Statistics

### GET `/statistics`

Get database statistics and analytics.

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

**Status Codes:**
- `200`: Success
- `500`: Server error

---

## 8. Risk Recommendations

### GET `/risk-recommendations`

Get clinical recommendations based on risk level.

**Query Parameters:**
- `risk_level` (required): "Low", "Medium", or "High"

**Response:**
```json
{
  "risk_level": "High",
  "recommendations": [
    "Immediate cardiology consultation recommended",
    "Consider cardiac imaging (echocardiogram, stress test)",
    "Aggressive risk factor modification required",
    "Optimize blood pressure control (target <130/80 mmHg)",
    "Initiate or intensify lipid-lowering therapy",
    "Optimize glycemic control (HbA1c <7%)",
    "Long-term cardiac surveillance protocol",
    "Regular exercise (150 min/week moderate activity)",
    "Mediterranean diet or DASH diet recommended"
  ]
}
```

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common Error Codes:**
- `400`: Bad Request (invalid input)
- `422`: Validation Error (Pydantic validation failed)
- `500`: Internal Server Error

**Validation Error Example:**
```json
{
  "detail": [
    {
      "loc": ["body", "age"],
      "msg": "ensure this value is less than or equal to 120",
      "type": "value_error.number.not_le"
    }
  ]
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production:
- Implement rate limiting (e.g., 100 requests/minute)
- Use API keys for tracking
- Monitor usage patterns

---

## CORS Configuration

The API allows all origins (`*`) for development. For production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## Performance Targets

| Endpoint | Target | Typical |
|----------|--------|---------|
| `/predict-risk` | <200ms | 150ms |
| `/upload-report` | <2s | 1.5s |
| `/patient-history` | <50ms | 30ms |
| `/ask-agent` | <1s | 800ms |
| `/statistics` | <50ms | 20ms |

---

## WebSocket Support

Not currently implemented. Future enhancement for real-time updates.

---

## Versioning

Current version: `1.0.0`

Future versions will use URL versioning:
- `/v1/predict-risk`
- `/v2/predict-risk`

---

## SDK Examples

### Python

```python
import requests

def predict_risk(features):
    response = requests.post(
        'http://localhost:8000/predict-risk',
        json=features
    )
    return response.json()

result = predict_risk({
    'age': 45,
    'bp': 130,
    'cholesterol': 210,
    'bmi': 28.5,
    'diabetes': 1,
    'smoking': 0,
    'radiation_dose': 38.0,
    'treatment_site': 'left_chest',
    'sessions': 25
})
print(result)
```

### JavaScript/TypeScript

```typescript
interface PatientFeatures {
  age: number;
  bp: number;
  cholesterol: number;
  bmi: number;
  diabetes: 0 | 1;
  smoking: 0 | 1;
  radiation_dose: number;
  treatment_site: string;
  sessions: number;
}

async function predictRisk(features: PatientFeatures) {
  const response = await fetch('http://localhost:8000/predict-risk', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(features)
  });
  return await response.json();
}
```

---

## Testing

Use the interactive API documentation at:
```
http://localhost:8000/docs
```

This provides:
- Try-it-out functionality
- Request/response examples
- Schema validation
- Authentication testing

---

## Support

- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **GitHub**: [Repository](https://github.com/MEETAL-GAIKWAD/-Real-Time-AI-Powered-Heart-Risk-Prediction-System-with-Radiotherapy-Intelligence)

---

**Last Updated**: March 12, 2026
