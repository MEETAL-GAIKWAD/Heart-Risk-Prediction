@echo off
REM Quick start script for frontend (Windows)

echo 🚀 Starting Heart Risk Prediction Frontend...
echo.

REM Check if in risk-dashboard directory
if not exist "package.json" (
    echo 📁 Changing to risk-dashboard directory...
    cd risk-dashboard
)

REM Check if node_modules exists
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    call npm install
)

REM Create .env if not exists
if not exist ".env" (
    echo ⚙️ Creating .env file...
    copy .env.example .env
)

REM Start development server
echo 🌐 Starting development server...
echo 📍 Dashboard will be available at: http://localhost:5174
echo.
npm run dev
