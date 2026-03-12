# Complete Setup Guide
## Real-Time AI-Powered Heart Risk Prediction System

This guide will help you set up and run the complete system locally.

## System Requirements

- **Python**: 3.8 or higher
- **Node.js**: 16 or higher
- **MongoDB**: 4.4 or higher (optional)
- **RAM**: 4GB minimum
- **Storage**: 2GB free space

## Project Structure

```
.
├── backend/                    # FastAPI backend
│   ├── main.py                # API server
│   ├── model_loader.py        # ML model
│   ├── predictor.py           # Prediction logic
│   ├── genai_explainer.py     # AI explanations
│   ├── shap_explainer.py      # Feature importance
│   ├── report_parser.py       # PDF parsing
│   ├── ai_agent.py            # Medical AI agent
│   ├── database.py            # MongoDB integration
│   ├── schemas.py             # Data models
│   ├── train_model.py         # Model training
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Backend docs
│
├── risk-dashboard/            # React frontend
│   ├── src/
│   │   ├── components/        # UI components
│   │   ├── api/              # API client
│   │   ├── App.jsx           # Main app
│   │   └── main.jsx          # Entry point
│   ├── package.json          # Node dependencies
│   └── README.md             # Frontend docs
│
├── cleaned_heart_risk_dataset.csv  # Training data
├── SETUP_GUIDE.md            # This file
└── API_DOCUMENTATION.md      # API reference
```

## Step-by-Step Setup

### STEP 1: Clone Repository

```bash
# If not already cloned
git clone https://github.com/MEETAL-GAIKWAD/-Real-Time-AI-Powered-Heart-Risk-Prediction-System-with-Radiotherapy-Intelligence
cd -Real-Time-AI-Powered-Heart-Risk-Prediction-System-with-Radiotherapy-Intelligence
```

### STEP 2: Backend Setup

#### 2.1 Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### 2.2 Configure Environment (Optional)

```bash
cp .env.example .env
```

Edit `.env` to add optional configurations:
```env
# Optional: For GenAI explanations
OPENAI_API_KEY=your_openai_api_key_here

# Optional: For MongoDB (falls back to in-memory)
MONGODB_URI=mongodb://localhost:27017/
```

#### 2.3 Train the Model

```bash
python train_model.py
```

Expected output:
```
Loading dataset from ../cleaned_heart_risk_dataset.csv
Training Gradient Boosting model...
Model trained successfully!
Train accuracy: 0.9234
Test accuracy: 0.8876
Model saved to trained_model.pkl
```

#### 2.4 Start Backend Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Verify backend is running:**
```bash
curl http://localhost:8000/health
```

### STEP 3: Frontend Setup

Open a new terminal window:

#### 3.1 Install Node Dependencies

```bash
cd risk-dashboard
npm install
```

#### 3.2 Configure Environment

```bash
cp .env.example .env
```

The `.env` file should contain:
```env
VITE_API_URL=http://localhost:8000
```

#### 3.3 Start Frontend

```bash
npm run dev
```

Expected output:
```
  VITE v7.3.1  ready in 500 ms

  ➜  Local:   http://localhost:5174/
  ➜  Network: use --host to expose
```

### STEP 4: Access the Application

Open your browser and navigate to:
```
http://localhost:5174
```

You should see the Heart Risk Prediction Dashboard!

## Testing the System

### Test 1: Manual Risk Prediction

1. Open the dashboard at `http://localhost:5174`
2. In the Patient Panel, click "Recalculate Risk"
3. The system will use the active patient's data
4. Observe the risk meter update

### Test 2: API Direct Test

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

Expected response:
```json
{
  "risk_probability": 0.81,
  "risk_level": "High",
  "explanation": "High cardiac risk due to...",
  "feature_importance": {...},
  "timestamp": "2026-03-12T10:30:00"
}
```

### Test 3: AI Agent

```bash
curl -X POST "http://localhost:8000/ask-agent" \
  -H "Content-Type: application/json" \
  -d '{
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
    }
  }'
```

## Troubleshooting

### Backend Issues

**Problem**: Model training fails
```
Solution: Ensure cleaned_heart_risk_dataset.csv is in the parent directory
```

**Problem**: Port 8000 already in use
```bash
# Use a different port
uvicorn main:app --reload --port 8001
# Update frontend .env: VITE_API_URL=http://localhost:8001
```

**Problem**: MongoDB connection fails
```
Solution: The system will automatically fall back to in-memory storage
```

### Frontend Issues

**Problem**: Port 5174 already in use
```
Solution: Vite will automatically use the next available port (5175, 5176, etc.)
```

**Problem**: API connection fails
```
Solution: 
1. Verify backend is running: curl http://localhost:8000/health
2. Check .env file has correct VITE_API_URL
3. Check browser console for CORS errors
```

**Problem**: npm install fails
```bash
# Clear cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## Optional: MongoDB Setup

### Install MongoDB (Windows)

1. Download from: https://www.mongodb.com/try/download/community
2. Install with default settings
3. MongoDB will run on `mongodb://localhost:27017/`

### Install MongoDB (Linux)

```bash
# Ubuntu/Debian
sudo apt-get install mongodb

# Start service
sudo systemctl start mongodb
```

### Verify MongoDB

```bash
# Check if MongoDB is running
mongosh
```

## Optional: OpenAI Integration

For enhanced GenAI explanations:

1. Get API key from: https://platform.openai.com/api-keys
2. Add to `backend/.env`:
```env
OPENAI_API_KEY=sk-...your-key-here
```
3. Restart backend server

## Performance Benchmarks

Expected performance metrics:

- **Prediction Time**: <200ms
- **Model Loading**: ~2 seconds (on startup)
- **Frontend Load**: <1 second
- **API Response**: <100ms (without ML)

## Production Deployment

### Backend (Docker)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
COPY cleaned_heart_risk_dataset.csv ../
RUN python train_model.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend (Build)

```bash
cd risk-dashboard
npm run build
# Deploy dist/ folder to your hosting service
```

## System Architecture

```
┌─────────────────┐
│   React UI      │  Port 5174
│  (Dashboard)    │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   FastAPI       │  Port 8000
│   Backend       │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
┌────────┐ ┌──────┐ ┌────────┐ ┌────────┐
│ ML     │ │ SHAP │ │ GenAI  │ │MongoDB │
│ Model  │ │      │ │ (GPT)  │ │   DB   │
└────────┘ └──────┘ └────────┘ └────────┘
```

## Feature Checklist

- [x] ML model training
- [x] Risk prediction API
- [x] SHAP feature importance
- [x] GenAI explanations
- [x] PDF report parsing
- [x] AI medical agent
- [x] MongoDB integration
- [x] React dashboard
- [x] Real-time updates
- [x] Interactive charts
- [x] Responsive design
- [x] Error handling
- [x] Performance optimization

## Next Steps

1. **Customize the UI**: Edit `risk-dashboard/src/components/`
2. **Add Authentication**: Implement user login
3. **Deploy to Cloud**: Use AWS, Azure, or GCP
4. **Add More Features**: Patient management, reports, etc.
5. **Improve Model**: Retrain with more data

## Support

- **Backend API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:5174
- **GitHub Issues**: [Repository Issues](https://github.com/MEETAL-GAIKWAD/-Real-Time-AI-Powered-Heart-Risk-Prediction-System-with-Radiotherapy-Intelligence/issues)

## License

MIT License - See LICENSE file for details

---

**System Status**: ✅ Complete and Ready for Demo

**Last Updated**: March 12, 2026
