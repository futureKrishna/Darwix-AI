#!/bin/bash
# Local CI pipeline test script

set -e

echo "🔄 Running Local CI Pipeline Test"
echo "================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2 passed${NC}"
    else
        echo -e "${RED}❌ $2 failed${NC}"
        exit 1
    fi
}

# Clean previous artifacts
echo -e "${YELLOW}🧹 Cleaning previous artifacts...${NC}"
make clean
print_status $? "Cleanup"

# Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
pip install -r requirements.txt > /dev/null 2>&1
pip install -r requirements-dev.txt > /dev/null 2>&1
print_status $? "Dependency installation"

# Code formatting
echo -e "${YELLOW}🎨 Checking code formatting...${NC}"
black --check app/ > /dev/null 2>&1
print_status $? "Black formatting check"

isort --check-only app/ > /dev/null 2>&1
print_status $? "isort import sorting check"

# Linting
echo -e "${YELLOW}📝 Running linting checks...${NC}"
flake8 app/ --max-line-length=88 --extend-ignore=E203,W503 > /dev/null 2>&1
print_status $? "Flake8 linting"

# Type checking
echo -e "${YELLOW}🔍 Running type checks...${NC}"
mypy app/ --ignore-missing-imports --disallow-untyped-defs --strict-optional > /dev/null 2>&1
print_status $? "MyPy type checking"

# Security checks
echo -e "${YELLOW}🔒 Running security checks...${NC}"
bandit -r app/ -q > /dev/null 2>&1
print_status $? "Bandit security scan"

safety check > /dev/null 2>&1
print_status $? "Safety vulnerability check"

# Run tests
echo -e "${YELLOW}🧪 Running tests with coverage...${NC}"
pytest test_final_clean.py --cov=app --cov-report=term-missing --cov-fail-under=90 -v > /dev/null 2>&1
print_status $? "Test execution with 90% coverage"

# Docker build test
echo -e "${YELLOW}🐋 Testing Docker build...${NC}"
docker build -t darwix-ai:test . > /dev/null 2>&1
print_status $? "Docker image build"

# Docker run test
echo -e "${YELLOW}🚀 Testing Docker container...${NC}"
docker run -d --name test-container -p 8001:8000 darwix-ai:test > /dev/null 2>&1
sleep 10
curl -f http://localhost:8001/health > /dev/null 2>&1
HEALTH_CHECK=$?
docker stop test-container > /dev/null 2>&1
docker rm test-container > /dev/null 2>&1
print_status $HEALTH_CHECK "Docker container health check"

# Cleanup Docker image
docker rmi darwix-ai:test > /dev/null 2>&1

echo ""
echo -e "${GREEN}🎉 All CI pipeline checks passed successfully!${NC}"
echo -e "${GREEN}✅ Your code is ready for production deployment${NC}"
