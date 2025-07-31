# Sales Analytics Microservice

A production-ready Python microservice that analyzes sales call transcripts and provides AI-powered insights through a comprehensive REST API.

> **🚀 New to this project?** See [SETUP.md](SETUP.md) for super-simple setup instructions!

## 🚀 Features

- **Real AI Processing**: Uses sentence-transformers and Hugging Face models for genuine ML insights
- **Async Architecture**: FastAPI with SQLAlchemy async for high performance
- **Smart Fallbacks**: Fast development mode with professional-grade fallback implementations
- **200+ Sample Calls**: Realistic call transcripts with proper AI analysis
- **Comprehensive API**: Full CRUD operations with advanced filtering
- **Production Ready**: Proper error handling, validation, and testing
- **Interview Optimized**: Clean codebase perfect for technical demonstrations

## 🚀 Complete Setup Guide

### Prerequisites
- **Python 3.8 or higher** (Check with: `python --version`)
- **Git** (For cloning the repository)
- **Internet connection** (For downloading ML models on first run)

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/futureKrishna/Darwix-AI.git
cd Darwix-AI
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*This may take 2-3 minutes as it downloads ML libraries*

#### 4. Start the Application
```bash
python fast_run.py
```

**That's it! 🎉** 

- Server starts at: **http://localhost:8000**
- API Documentation: **http://localhost:8000/docs**
- Interactive Demo: **http://localhost:8000/redoc**

### 🔄 How to Start Every Time

**For Daily Development (Fast Startup - 5 seconds):**
```bash
cd Darwix-AI
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
python fast_run.py
```

**For Production Testing (Real AI Models - 2-3 minutes first time):**
```bash
cd Darwix-AI  
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
python production_ml_run.py
```

### ✅ Verify Installation
```bash
# Test the server is working
curl http://localhost:8000/health
# Should return: {"status":"healthy"}

# Or run comprehensive tests
python production_test.py
# Should show: "🎉 ALL PRODUCTION TESTS PASSED!"
```

## � Daily Workflow

### Every Time You Want to Use This Application:

**Step 1: Navigate to Project**
```bash
cd Darwix-AI
```

**Step 2: Activate Virtual Environment**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac  
source venv/bin/activate
```

**Step 3: Start Server**
```bash
# For quick development/testing (recommended):
python fast_run.py

# For production features with real AI:
python production_ml_run.py
```

**Step 4: Open Browser**
- Main API: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

**Step 5: When Done**
Press `Ctrl+C` in terminal to stop server

### 🎯 Different Server Modes

| Command | Startup Time | Features | Use Case |
|---------|-------------|----------|----------|
| `python fast_run.py` | 5 seconds | Fallback AI, Full API | Development, Demos, Testing |
| `python production_ml_run.py` | 2-3 minutes | Real ML Models | Production, Interviews |
| `python interview_demo.py` | N/A | Interactive Demo | Showcasing Features |

## �📚 API Documentation

Once the server is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🔗 API Endpoints

### Health Check
```bash
GET /health
curl http://localhost:8000/health
```

### Get All Calls with Filtering
```bash
GET /api/v1/calls
# Examples:
curl "http://localhost:8000/api/v1/calls?limit=10"
curl "http://localhost:8000/api/v1/calls?agent_id=agent_001&min_sentiment=0.5"
curl "http://localhost:8000/api/v1/calls?from_date=2025-07-01&limit=20"
```

**Query Parameters**:
- `limit` (1-100, default: 50): Number of calls to return
- `offset` (default: 0): Pagination offset  
- `agent_id`: Filter by specific agent
- `from_date` / `to_date`: Date range filtering
- `min_sentiment` / `max_sentiment`: Sentiment score filtering (-1 to 1)

### Get Single Call
```bash
GET /api/v1/calls/{call_id}
curl "http://localhost:8000/api/v1/calls/call_123456"
```

### Get Call Recommendations
```bash
GET /api/v1/calls/{call_id}/recommendations
curl "http://localhost:8000/api/v1/calls/call_123456/recommendations"
```
Returns 5 most similar calls based on content embeddings.

### Agent Analytics
```bash
GET /api/v1/analytics/agents
curl "http://localhost:8000/api/v1/analytics/agents"
```
Returns agent performance leaderboard with metrics.

## 🧪 Testing

### Automated Test Suite
```bash
python production_test.py
```
Runs comprehensive tests against all endpoints with validation.

### Interactive Interview Demo  
```bash
python interview_demo.py
```
Showcases all features in an interactive demonstration.

### Manual Testing
```bash
# Test health endpoint
curl http://localhost:8000/health

# Get first 5 calls
curl "http://localhost:8000/api/v1/calls?limit=5"

# Test filtering
curl "http://localhost:8000/api/v1/calls?min_sentiment=0.8&limit=3"
```

## 🔧 Troubleshooting

### Common Issues & Solutions

#### ❌ "Python not found" or "pip not found"
```bash
# Install Python from python.org (3.8 or higher)
# Verify installation:
python --version
pip --version
```

#### ❌ "Virtual environment activation failed"
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# If that fails, try:
python -m venv venv
.\venv\Scripts\activate.bat

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### ❌ "Requirements installation failed"
```bash
# Upgrade pip first:
python -m pip install --upgrade pip

# Then install requirements:
pip install -r requirements.txt

# If still fails, install key packages individually:
pip install fastapi uvicorn sqlalchemy pydantic aiosqlite
```

#### ❌ "Port 8000 already in use"
```bash
# Kill existing processes on port 8000:
# Windows:
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Or use a different port:
uvicorn app.main:app --port 8001
```

#### ❌ "Database errors"
```bash
# Delete existing database and regenerate:
rm sales_analytics.db  # Linux/Mac
del sales_analytics.db  # Windows

# Then restart:
python fast_run.py
```

#### ❌ "ML models not loading"
This is expected! The system uses fallback implementations by default.
- `fast_run.py` - Uses fallbacks (starts in 5 seconds)
- `production_ml_run.py` - Downloads real models (2-3 minutes first time)

### Getting Help
1. Check server is running: http://localhost:8000/health
2. Run tests: `python production_test.py`
3. Try interactive demo: `python interview_demo.py`
4. Check logs in terminal for specific error messages

## 🏗️ Architecture & Technology

### Core Technologies
- **FastAPI**: Modern async web framework with automatic OpenAPI docs
- **SQLAlchemy**: Async ORM with SQLite database  
- **Pydantic**: Data validation and serialization
- **sentence-transformers**: Real embeddings using all-MiniLM-L6-v2 model
- **Hugging Face Transformers**: Sentiment analysis with CardiffNLP Twitter-RoBERTa

### AI Processing
- **Real Mode**: Uses actual ML models for production-quality results
- **Fast Mode**: Professional fallback implementations for rapid development
- **Embeddings**: 384-dimensional vectors for semantic similarity
- **Sentiment**: Multi-factor analysis including word patterns and conversational cues
- **Talk Ratio**: Intelligent agent vs customer speaking time calculation

### Database Schema
```sql
-- Main table with optimized indexing
CREATE TABLE call_records (
    id TEXT PRIMARY KEY,
    call_id TEXT UNIQUE,
    agent_id TEXT,
    customer_id TEXT,
    start_time DATETIME,
    duration_seconds INTEGER,
    transcript TEXT,
    agent_talk_ratio REAL,
    customer_sentiment_score REAL,
    content_embedding BLOB,
    created_at DATETIME
);

-- Performance indexes
CREATE INDEX idx_agent_id ON call_records(agent_id);
CREATE INDEX idx_start_time ON call_records(start_time);
```

## 📁 Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application & routes
│   ├── models.py            # SQLAlchemy database models  
│   ├── schemas.py           # Pydantic response models
│   ├── database.py          # Database connection setup
│   └── ai_insights.py       # AI/ML processing engine
├── alembic/                 # Database migrations
│   ├── env.py
│   └── versions/
├── fast_run.py              # Quick dev server with fallbacks
├── production_ml_run.py     # Production server with real AI
├── generate_data.py         # Creates 200 sample calls
├── production_test.py       # Automated API testing
├── interview_demo.py        # Interactive demonstration
├── requirements.txt         # Python dependencies
├── sales_analytics.db       # SQLite database (auto-created)
├── alembic.ini             # Migration configuration
├── docker-compose.yml       # Docker setup (optional)
├── Dockerfile              # Container definition (optional)
└── README.md               # This file
```

## 🔧 Development

### Key Files Explained

- **`fast_run.py`**: Perfect for development - quick startup with fallback AI
- **`production_ml_run.py`**: Production mode with real ML models (slower startup) 
- **`generate_data.py`**: Creates realistic call data with proper AI analysis
- **`production_test.py`**: Validates all endpoints work correctly
- **`interview_demo.py`**: Shows off features in an interactive way

### Adding Features

1. **New Endpoints**: Add to `app/main.py` with proper Pydantic validation
2. **Database Changes**: Create migration in `alembic/versions/`
3. **AI Processing**: Extend `app/ai_insights.py` with new analysis methods
4. **Testing**: Update `production_test.py` with new test cases

## 🚀 Deployment Options

### Local Development (Current Setup)
- SQLite database (included)
- Fast startup with fallbacks
- Perfect for demos and testing

### Docker (Optional)
```bash
# If you have Docker installed:
docker-compose up --build
```
*Note: Docker files are included but not required for basic operation*

### Production Deployment
- Switch to PostgreSQL in `app/database.py`
- Enable real AI models in production
- Add proper environment variable management
- Consider Redis for caching embeddings

## 💡 Features Highlight

### What Makes This Special
- ✅ **Real AI Models**: Actual sentence-transformers and Hugging Face models
- ✅ **Smart Fallbacks**: Runs instantly even without heavy ML dependencies  
- ✅ **200+ Sample Calls**: Realistic data with proper conversation patterns
- ✅ **Production Architecture**: Async FastAPI with proper error handling
- ✅ **Interview Ready**: Clean, well-documented, professional codebase
- ✅ **Comprehensive Testing**: Automated validation of all endpoints
- ✅ **Easy Demo**: Multiple ways to showcase the system

### Sample Data Quality
- **20 Realistic Agents** with consistent behavior patterns
- **Diverse Scenarios**: Technical support, billing, complaints, sales calls
- **Natural Conversations**: Proper dialogue flow between agents and customers
- **Meaningful Metrics**: Real talk ratios, sentiment scores, and embeddings
- **Time Distribution**: Calls spread across realistic time periods

## 🎯 Perfect for Job Interviews

This codebase demonstrates:
- **FastAPI Expertise**: Modern async Python web development
- **Database Design**: SQLAlchemy with proper indexing and migrations
- **AI/ML Integration**: Real models with professional fallback strategies
- **Testing Practices**: Comprehensive automated testing
- **Clean Architecture**: Well-organized, maintainable code structure
- **Documentation**: Clear, accurate, and helpful README
- **Production Readiness**: Proper error handling and validation

## 📞 Support & Questions

This is a complete, working microservice ready for demonstration. All features described are actually implemented and tested.

**Quick Verification**:
```bash
python fast_run.py        # Starts in 5 seconds
python production_test.py  # Validates everything works
python interview_demo.py   # Interactive showcase
```

---

**Built with ❤️ for technical interviews and real-world applications**