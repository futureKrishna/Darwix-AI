# Sales Analytics API

[![CI Pipeline](https://github.com/futureKrishna/Darwix-AI/workflows/CI%20Pipeline/badge.svg)](https://github.com/futureKrishna/Darwix-AI/actions)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)](https://www.docker.com)
[![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen.svg)](./htmlcov/index.html)

A high-performance Python microservice for analyzing sales call transcripts with AI-powered insights, real-time streaming capabilities, and comprehensive CI/CD pipeline.

## 🚀 Features

### Core Functionality
- **🤖 AI-Powered Analysis**: Sentence-transformers and Hugging Face models for semantic analysis
- **⚡ Async Architecture**: FastAPI with SQLAlchemy async for high-throughput processing
- **🔄 Real-time WebSocket Streaming**: Live sentiment analysis during active calls
- **⏰ Background Job Processing**: Automated nightly analytics recalculation with scheduler
- **🎯 Smart Fallbacks**: Development mode with production-grade fallback implementations
- **📊 200+ Sample Calls**: Realistic call transcripts with comprehensive AI analysis
- **🔍 Advanced API**: Full CRUD operations with complex filtering and recommendations
- **🛡️ Production Ready**: Comprehensive error handling, validation, and monitoring

### Security & Authentication
- **🔐 JWT Authentication**: Secure token-based authentication system
- **👥 Multi-user Support**: Role-based access control with user management
- **🔒 Security Scanning**: Automated vulnerability detection with Bandit and Safety

### DevOps & CI/CD
- **🔄 CI/CD Pipeline**: Comprehensive GitHub Actions workflow with testing, security, and Docker deployment
- **🐋 Containerization**: Docker and Docker Compose support for easy deployment
- **📈 Code Quality**: Black, isort, flake8, pylint, and mypy for code quality
- **🧪 Test Coverage**: 94% test coverage with pytest and comprehensive test suite
- **📝 Pre-commit Hooks**: Automated code quality checks on every commit

## 🛠️ Tech Stack

### Backend
- **FastAPI 0.104.1** - Modern, fast web framework for building APIs
- **Python 3.11+** - Latest Python features and performance improvements
- **SQLAlchemy 2.0** - Modern async ORM with declarative_base
- **SQLite + aiosqlite** - Lightweight, serverless database
- **Pydantic V2** - Data validation with ConfigDict (deprecation warnings fixed)
- **JWT (python-jose)** - Secure authentication tokens
- **Uvicorn** - Lightning-fast ASGI server

### AI & ML
- **sentence-transformers** - State-of-the-art text embeddings
- **transformers** - Hugging Face model library
- **numpy** - Numerical computing for ML operations

### DevOps & Deployment
- **Docker & Docker Compose** - Containerization and orchestration
- **GitHub Actions** - CI/CD pipeline automation
- **Alembic** - Database migrations
- **pytest** - Comprehensive testing framework

### Development Tools
- **Black** - Code formatting
- **isort** - Import sorting
- **flake8 & pylint** - Code linting
- **mypy** - Static type checking
- **Bandit** - Security vulnerability scanning
- **pre-commit** - Git hooks for code quality

## 🏃‍♂️ Quick Start

### Prerequisites
- **Python 3.11+** (Check with: `python --version`)
- **Git** (For cloning the repository)
- **Docker** (Optional, for containerized deployment)

### 1. Clone & Setup
```bash
git clone https://github.com/futureKrishna/Darwix-AI.git
cd Darwix-AI

# Create virtual environment
python -m venv venv
# Windows
venv\\Scripts\\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the Application
```bash
# Fast development mode (5 seconds startup)
python fast_run.py

# Production mode with real AI models (2-3 minutes first time)
python production_ml_run.py
```

### 3. Access the API
- **🌐 Server**: http://localhost:8000
- **📚 API Documentation**: http://localhost:8000/docs
- **🔍 Interactive Demo**: http://localhost:8000/redoc

### 4. Test the API
```bash
# Test basic health check
curl http://localhost:8000/health

# Run comprehensive tests
python production_test.py

# Run full test suite
pytest test_final_clean.py -v
```

### 5. Test WebSocket (Real-time Features)
```javascript
// Open browser developer console and run:
const ws = new WebSocket('ws://localhost:8000/ws/sentiment/call_f7a5985b-5220-4361-b627-f9fa1a841763');
ws.onmessage = (event) => console.log('Sentiment:', JSON.parse(event.data));
```

*See [WEBSOCKET_TESTING.md](./WEBSOCKET_TESTING.md) for detailed WebSocket testing guide.*

## 🔐 Authentication

### Default Credentials
```
Username: admin
Password: secret

Alternative users: analyst, demo (same password)
```

### API Usage Example
```bash
# 1. Login to get token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "secret"}'

# 2. Use token in requests
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  "http://localhost:8000/api/v1/calls"
```

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Login and get JWT token |
| GET | `/auth/me` | Get current user info |

### Call Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/calls` | List calls with filtering & pagination |
| GET | `/api/v1/calls/{call_id}` | Get specific call details |
| GET | `/api/v1/calls/{call_id}/recommendations` | Get AI recommendations |
| GET | `/api/v1/analytics/agents` | Get agent performance analytics |
| POST | `/api/v1/analytics/recalculate` | Trigger analytics recalculation |

### Real-time Features
| Method | Endpoint | Description |
|--------|----------|-------------|
| WebSocket | `/ws/sentiment/{call_id}` | Real-time sentiment streaming |
| GET | `/health` | Health check endpoint |

> **💡 WebSocket Testing**: See [WEBSOCKET_TESTING.md](./WEBSOCKET_TESTING.md) for multiple ways to test real-time functionality, including browser console, Python scripts, and online tools.

### Query Parameters (Calls Endpoint)
- `limit` (1-100): Number of results per page
- `offset` (≥0): Pagination offset
- `agent_id`: Filter by specific agent
- `from_date` / `to_date`: Date range filtering
- `min_sentiment` / `max_sentiment`: Sentiment score filtering (-1 to 1)
- `language`: Filter by call language

## 🐋 Docker Deployment

### Quick Docker Setup
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t darwix-ai .
docker run -p 8000:8000 darwix-ai
```

### Production Docker Deployment
```bash
# Pull from Docker Hub (when available)
docker pull futurekrishna/darwix-ai:latest
docker run -p 8000:8000 futurekrishna/darwix-ai:latest
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow
The project includes a comprehensive CI/CD pipeline that runs on every push and pull request:

#### Pipeline Jobs
1. **🧪 Test Job** - Runs tests with 90% coverage requirement
2. **🔒 Security Job** - Bandit security scanning and vulnerability checks
3. **🐋 Docker Job** - Docker image building and testing
4. **📝 Lint Job** - Code formatting and quality checks
5. **⚡ Performance Job** - Performance testing (main branch only)
6. **📢 Notification Job** - Pipeline status notifications

#### Local CI Testing
```bash
# Run full local CI pipeline
make ci-local

# Or use platform-specific scripts
./test-ci.sh      # Linux/Mac
test-ci.bat       # Windows

# Individual checks
make test         # Run tests with coverage
make lint         # Run linting checks
make format       # Format code
make type-check   # Run type checking
make security     # Run security scans
```

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

# Available make commands
make help
```

## 📊 Testing & Coverage

### Test Coverage: 94%
- **app/ai_insights.py**: 100%
- **app/models.py**: 100%
- **app/auth.py**: 100%
- **Overall Coverage**: 94%

### Running Tests
```bash
# Run all tests with coverage
pytest test_final_clean.py --cov=app --cov-report=html

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m auth          # Authentication tests only

# Run with different verbosity levels
pytest -v               # Verbose output
pytest -s               # Show print statements
pytest --tb=short       # Short traceback format
```

### Test Categories
- **Unit Tests**: Individual function and method testing
- **Integration Tests**: API endpoint and database testing
- **Authentication Tests**: JWT and security testing
- **WebSocket Tests**: Real-time streaming functionality
- **Scheduler Tests**: Background job processing
- **AI Tests**: Machine learning model integration

## 🎯 Performance & Scalability

### Key Metrics
- **Startup Time**: <5 seconds (development mode)
- **Response Time**: <100ms (average API response)
- **Throughput**: 1000+ requests/second (with proper hardware)
- **Database**: Optimized with indexes on frequently queried fields
- **Memory Usage**: <200MB (base application)

### Scalability Features
- **Async Operations**: All database operations are asynchronous
- **Connection Pooling**: SQLAlchemy async engine with connection pooling
- **Background Processing**: Non-blocking analytics recalculation
- **Efficient Queries**: Optimized SQL queries with proper indexing
- **Pagination**: Built-in pagination for large datasets

## 🚀 Production Deployment

### Environment Variables
```bash
# Optional configuration
JWT_SECRET_KEY="your-secret-key"          # JWT secret (default provided)
DATABASE_URL="sqlite+aiosqlite:///./sales_analytics.db"  # Database URL
OPENAI_API_KEY="your-openai-key"          # For enhanced AI features
TESTING="1"                               # Disable scheduler during testing
```

### Production Checklist
- [ ] Change JWT secret key
- [ ] Set up proper logging
- [ ] Configure reverse proxy (nginx)
- [ ] Set up SSL/TLS certificates
- [ ] Configure monitoring and alerting
- [ ] Set up backup strategy
- [ ] Scale with multiple workers: `uvicorn app.main:app --workers 4`

## 🔧 Development

### Code Quality Standards
- **Formatting**: Black (88 character line length)
- **Import Sorting**: isort with Black profile
- **Linting**: flake8 and pylint with custom rules
- **Type Checking**: mypy with strict settings
- **Security**: Bandit security linting
- **Testing**: pytest with 90% coverage minimum

### Architecture Overview
```
Sales Analytics API
├── app/
│   ├── main.py           # FastAPI application and routes
│   ├── models.py         # SQLAlchemy database models
│   ├── schemas.py        # Pydantic data validation models
│   ├── database.py       # Database connection and session management
│   ├── auth.py           # JWT authentication and authorization
│   └── ai_insights.py    # AI/ML processing and insights
├── alembic/              # Database migrations
├── .github/workflows/    # CI/CD pipeline
├── tests/                # Test suite
└── docs/                 # Documentation
```

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run tests: `make test`
5. Run CI checks: `make ci-local`
6. Commit with conventional commits: `git commit -m "feat: add new feature"`
7. Push and create a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Write comprehensive tests
- Update documentation
- Ensure 90%+ test coverage
- Pass all CI/CD checks

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Troubleshooting

### Common Issues

#### Startup Issues
```bash
# If you get import errors
pip install -r requirements.txt

# If database errors occur
alembic upgrade head

# If port is in use
lsof -ti:8000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :8000   # Windows
```

#### Authentication Issues
- Default credentials: `admin` / `secret`
- Token expires in 30 minutes
- Check JWT secret key configuration

#### Performance Issues
- Use production mode for better performance: `python production_ml_run.py`
- Consider increasing worker count: `uvicorn app.main:app --workers 4`
- Monitor memory usage with large datasets

### Getting Help
- 📧 Email: support@darwix-ai.com
- 🐛 Issues: [GitHub Issues](https://github.com/futureKrishna/Darwix-AI/issues)
- 📚 Documentation: Check `/docs` endpoint when server is running
- 💬 Discussions: [GitHub Discussions](https://github.com/futureKrishna/Darwix-AI/discussions)

## 🙏 Acknowledgments

- **FastAPI** team for the excellent framework
- **Hugging Face** for transformers and model hosting
- **SQLAlchemy** team for the robust ORM
- **GitHub Actions** for reliable CI/CD
- **Docker** for containerization platform

---

**Built with ❤️ for enterprise applications and technical demonstrations**

[![Star this repo](https://img.shields.io/github/stars/futureKrishna/Darwix-AI?style=social)](https://github.com/futureKrishna/Darwix-AI/stargazers)
[![Fork this repo](https://img.shields.io/github/forks/futureKrishna/Darwix-AI?style=social)](https://github.com/futureKrishna/Darwix-AI/fork)