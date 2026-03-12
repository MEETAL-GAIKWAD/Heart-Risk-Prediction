# System Architecture
## Real-Time AI-Powered Heart Risk Prediction System

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│                  React Dashboard (Port 5174)                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │  Risk    │ │ Patient  │ │  Charts  │ │  Alerts  │      │
│  │  Meter   │ │  Panel   │ │          │ │  Panel   │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST API
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND API LAYER                         │
│                FastAPI Server (Port 8000)                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Endpoints: /predict-risk, /upload-report, etc.     │  │
│  └──────────────────────────────────────────────────────┘  │
└────────┬────────┬────────┬────────┬────────┬───────────────┘
         │        │        │        │        │
         ▼        ▼        ▼        ▼        ▼
    ┌────────┐┌──────┐┌────────┐┌──────┐┌────────┐
    │   ML   ││ SHAP ││ GenAI  ││ PDF  ││MongoDB │
    │ Model  ││      ││  LLM   ││Parser││   DB   │
    └────────┘└──────┘└────────┘└──────┘└────────┘
```

## Component Details

### 1. Frontend Layer (React)
- **Technology**: React 19, Vite, Tailwind CSS
- **Components**: 6 major UI components
- **State Management**: React hooks
- **Charts**: Recharts library
- **Real-time**: 5-second update interval

### 2. API Layer (FastAPI)
- **Framework**: FastAPI with Uvicorn
- **Performance**: <200ms response time
- **CORS**: Enabled for cross-origin requests
- **Validation**: Pydantic schemas
- **Logging**: Comprehensive error tracking

### 3. ML Model Layer
- **Algorithm**: Gradient Boosting Classifier
- **Features**: 9 input features
- **Training**: Scikit-learn
- **Accuracy**: ~88% test accuracy
- **Storage**: Joblib pickle format

### 4. Explainability Layer
- **SHAP**: Feature importance calculation
- **GenAI**: OpenAI GPT-3.5-turbo (optional)
- **Templates**: Fallback explanations
- **Medical Agent**: Q&A system

### 5. Data Layer
- **Primary**: MongoDB (optional)
- **Fallback**: In-memory storage
- **Collections**: patients, predictions
- **Indexing**: created_at, patient_id

## Data Flow

### Prediction Flow
```
User Input → Frontend → API → Predictor → Model → SHAP → GenAI → Response
                                    ↓
                                Database
```

### Report Upload Flow
```
PDF Upload → API → Parser → Extract Features → Predictor → Response
```

## Technology Stack

### Backend
- Python 3.8+
- FastAPI 0.115.0
- Scikit-learn 1.5.2
- XGBoost 2.1.1
- SHAP 0.46.0
- LangChain 0.3.7
- PyMongo 4.10.1
- PDFPlumber 0.11.4

### Frontend
- React 19.2.0
- Vite 7.3.1
- Tailwind CSS 3.4.17
- Recharts 3.7.0
- Lucide React 0.563.0

### Database
- MongoDB 4.4+

### Optional
- OpenAI API (GPT-3.5-turbo)

## Deployment Architecture

```
Production Setup:

┌─────────────┐
│   Nginx     │ ← HTTPS/SSL
│ Load Balancer│
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌──────┐ ┌──────┐
│ API  │ │ API  │ ← Multiple instances
│ Node │ │ Node │
└──┬───┘ └──┬───┘
   │        │
   └────┬───┘
        ▼
   ┌─────────┐
   │ MongoDB │ ← Replica set
   │ Cluster │
   └─────────┘
```

## Security Considerations

1. **Input Validation**: Pydantic schemas
2. **File Upload**: PDF validation
3. **CORS**: Configurable origins
4. **API Keys**: Environment variables
5. **Error Handling**: Sanitized messages

## Performance Optimization

1. **Model Loading**: Once at startup
2. **SHAP Caching**: Explainer reuse
3. **Background Tasks**: Async DB writes
4. **Connection Pooling**: MongoDB
5. **Response Compression**: Gzip

## Scalability

- **Horizontal**: Multiple API instances
- **Vertical**: Increase resources
- **Caching**: Redis for predictions
- **Queue**: Celery for heavy tasks
- **CDN**: Static assets

## Monitoring

- Health check endpoint
- Performance logging
- Error tracking
- Request metrics
- Database stats

---

**Last Updated**: March 12, 2026
