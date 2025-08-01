@echo off
REM Local CI pipeline test script for Windows

setlocal enabledelayedexpansion

echo 🔄 Running Local CI Pipeline Test
echo =================================

REM Function to check status
set "error_occurred=0"

echo 🧹 Cleaning previous artifacts...
if exist "htmlcov" rd /s /q "htmlcov"
if exist "coverage.xml" del "coverage.xml"
if exist ".pytest_cache" rd /s /q ".pytest_cache"
if exist ".mypy_cache" rd /s /q ".mypy_cache"
echo ✅ Cleanup completed

echo 📦 Installing dependencies...
pip install -r requirements.txt >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ Failed to install production dependencies
    set "error_occurred=1"
    goto :end
)

pip install -r requirements-dev.txt >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ Failed to install development dependencies  
    set "error_occurred=1"
    goto :end
)
echo ✅ Dependencies installed

echo 🎨 Checking code formatting...
black --check app\ >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ Black formatting check failed
    set "error_occurred=1"
    goto :end
)
echo ✅ Black formatting check passed

isort --check-only app\ >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ isort import sorting check failed
    set "error_occurred=1" 
    goto :end
)
echo ✅ isort import sorting check passed

echo 📝 Running linting checks...
flake8 app\ --max-line-length=88 --extend-ignore=E203,W503 >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ Flake8 linting failed
    set "error_occurred=1"
    goto :end
)
echo ✅ Flake8 linting passed

echo 🔍 Running type checks...
mypy app\ --ignore-missing-imports --disallow-untyped-defs --strict-optional >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ MyPy type checking failed
    set "error_occurred=1"
    goto :end
)
echo ✅ MyPy type checking passed

echo 🔒 Running security checks...
bandit -r app\ -q >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ Bandit security scan failed
    set "error_occurred=1"
    goto :end
)
echo ✅ Bandit security scan passed

safety check >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ Safety vulnerability check failed
    set "error_occurred=1"
    goto :end
)
echo ✅ Safety vulnerability check passed

echo 🧪 Running tests with coverage...
pytest test_final_clean.py --cov=app --cov-report=term-missing --cov-fail-under=90 -v >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ Test execution failed
    set "error_occurred=1"
    goto :end
)
echo ✅ Tests passed with 90%+ coverage

echo 🐋 Testing Docker build...
docker build -t darwix-ai:test . >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ Docker image build failed
    set "error_occurred=1"
    goto :end
)
echo ✅ Docker image build passed

echo 🚀 Testing Docker container...
docker run -d --name test-container -p 8001:8000 darwix-ai:test >nul 2>&1
timeout /t 10 /nobreak >nul
curl -f http://localhost:8001/health >nul 2>&1
set "health_check=!errorlevel!"
docker stop test-container >nul 2>&1
docker rm test-container >nul 2>&1

if !health_check! neq 0 (
    echo ❌ Docker container health check failed
    set "error_occurred=1"
    goto :end
)
echo ✅ Docker container health check passed

REM Cleanup Docker image
docker rmi darwix-ai:test >nul 2>&1

:end
if !error_occurred! equ 0 (
    echo.
    echo 🎉 All CI pipeline checks passed successfully!
    echo ✅ Your code is ready for production deployment
) else (
    echo.
    echo ❌ CI pipeline failed. Please fix the issues and try again.
    exit /b 1
)

endlocal
