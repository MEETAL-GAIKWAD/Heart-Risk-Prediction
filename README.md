# Real-Time AI-Powered Heart Risk Prediction System
## with Radiotherapy Intelligence

[![Status](https://img.shields.io/badge/Status-Complete-success)]()
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688)]()
[![Frontend](https://img.shields.io/badge/Frontend-React-61DAFB)]()
[![ML](https://img.shields.io/badge/ML-Scikit--learn-F7931E)]()
[![License](https://img.shields.io/badge/License-MIT-blue)]()

A complete, production-ready system for predicting cardiovascular risk in radiotherapy patients using machine learning, SHAP explainability, and GenAI clinical explanations.

 

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB (optional)

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python train_model.py
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd risk-dashboard
npm install
npm run dev
```

### Access
- **Frontend**: http://localhost:5174
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📊 System Architecture

```
React Dashboard (Port 5174)
         ↓
FastAPI Backend (Port 8000)
         ↓
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
ML Model   SHAP    GenAI (GPT)  MongoDB
```

## 📁 Project Structure

```
├── backend/              # FastAPI backend
│   ├── main.py          # API server
│   ├── model_loader.py  # ML model
│   ├── predictor.py     # Prediction logic
│   ├── genai_explainer.py
│   ├── shap_explainer.py
│   ├── report_parser.py
│   ├── ai_agent.py
│   └── database.py
│
├── risk-dashboard/      # React frontend
│   ├── src/components/  # UI components
│   └── src/api/        # API client
│
└── docs/               # Documentation
    ├── SETUP_GUIDE.md
    ├── API_DOCUMENTATION.md
    └── ARCHITECTURE.md
```

## 🔬 ML Model

- **Algorithm**: Gradient Boosting Classifier
- **Features**: 9 clinical parameters
- **Training Data**: 8,332 patients
- **Accuracy**: 88% test accuracy
- **Performance**: <200ms prediction time

### Input Features
1. Age (years)
2. Blood Pressure (mmHg)
3. Cholesterol (mg/dL)
4. BMI
5. Diabetes (0/1)
6. Smoking (0/1)
7. Radiation Dose (Gy)
8. Treatment Site
9. Treatment Sessions

### Risk Levels
- **Low**: 0-35%
- **Medium**: 35-70%
- **High**: 70-100%

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/predict-risk` | POST | Predict cardiovascular risk |
| `/upload-report` | POST | Upload PDF medical report |
| `/patient-history` | GET | Get prediction history |
| `/ask-agent` | POST | Ask AI medical agent |
| `/statistics` | GET | Get database statistics |
| `/health` | GET | Health check |

## 📖 Documentation

- **[Setup Guide](SETUP_GUIDE.md)**: Complete installation instructions
- **[API Documentation](API_DOCUMENTATION.md)**: Full API reference
- **[Architecture](ARCHITECTURE.md)**: System design and components
- **[Final Deliverables](FINAL_DELIVERABLES.md)**: Project summary

## 🧪 Example Usage

### Predict Risk (cURL)
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

### Response
```json
{
  "risk_probability": 0.81,
  "risk_level": "High",
  "explanation": "High cardiac risk due to elevated radiation dose...",
  "feature_importance": {
    "radiation_dose": 0.41,
    "bp": 0.22,
    "cholesterol": 0.18
  }
}
```

## 🛠️ Technology Stack

### Backend
- FastAPI, Uvicorn
- Scikit-learn, XGBoost
- SHAP, LangChain, OpenAI
- PyMongo, PDFPlumber

### Frontend
- React 19, Vite
- Tailwind CSS, Recharts
- Lucide Icons

### Database
- MongoDB (with in-memory fallback)

## 📈 Performance

- **Prediction Time**: <200ms ✅
- **Model Accuracy**: 88% ✅
- **API Response**: <100ms ✅
- **Frontend Load**: <1s ✅

## 🔒 Security

- Input validation (Pydantic)
- File upload validation
- CORS configuration
- Error message sanitization
- Environment variable management

## 🚢 Deployment

### Docker
```bash
docker build -t heart-risk-api ./backend
docker run -p 8000:8000 heart-risk-api
```

### Production
- Use Nginx for load balancing
- MongoDB replica set
- Environment-based configuration
- SSL/TLS encryption

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Status**: ✅ Complete and Production-Ready

**Last Updated**: March 12, 2026