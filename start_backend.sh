#!/bin/bash
# Quick start script for backend

echo "🚀 Starting Heart Risk Prediction Backend..."
echo ""

# Check if in backend directory
if [ ! -f "main.py" ]; then
    echo "📁 Changing to backend directory..."
    cd backend
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Train model if not exists
if [ ! -f "trained_model.pkl" ]; then
    echo "🤖 Training ML model..."
    python train_model.py
fi

# Start server
echo "🌐 Starting API server..."
echo "📍 API will be available at: http://localhost:8000"
echo "📚 API docs at: http://localhost:8000/docs"
echo ""
uvicorn main:app --reload --host 0.0.0.0 --port 8000
