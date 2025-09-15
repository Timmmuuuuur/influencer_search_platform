@echo off
REM Influencer Search Platform Startup Script for Windows

echo 🚀 Starting Influencer Search Platform...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16 or higher.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist "backend\.env" (
    echo ⚠️  .env file not found. Creating from template...
    copy "backend\env.example" "backend\.env"
    echo 📝 Please edit backend\.env with your API keys before running again.
    echo    Required keys: OPENAI_API_KEY, YOUTUBE_API_KEY, EMAIL_USERNAME, EMAIL_PASSWORD
    pause
    exit /b 1
)

REM Start backend
echo 🔧 Starting backend server...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

REM Start backend server in background
echo 🚀 Starting FastAPI server on http://localhost:8000
start /B uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo 🎨 Starting frontend server...
cd ..\frontend

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo 📦 Installing Node.js dependencies...
    npm install
)

REM Start frontend server
echo 🚀 Starting Next.js server on http://localhost:3000
start /B npm run dev

echo.
echo ✅ Platform is running!
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo Press any key to stop both servers
pause >nul

echo 🛑 Stopping servers...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
echo ✅ Servers stopped
