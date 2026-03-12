#!/bin/bash
# Quick start script for frontend

echo "🚀 Starting Heart Risk Prediction Frontend..."
echo ""

# Check if in risk-dashboard directory
if [ ! -f "package.json" ]; then
    echo "📁 Changing to risk-dashboard directory..."
    cd risk-dashboard
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
fi

# Start development server
echo "🌐 Starting development server..."
echo "📍 Dashboard will be available at: http://localhost:5174"
echo ""
npm run dev
