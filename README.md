# Sales Analytics API

A high-performance Python microservice for analyzing sales call transcripts with AI-powered insights and real-time streaming capabilities.

## 🚀 Features

- **AI-Powered Analysis**: Sentence-transformers and Hugging Face models for semantic analysis
- **Async Architecture**: FastAPI with SQLAlchemy async for high-throughput processing
- **Real-time WebSocket Streaming**: Live sentiment analysis during active calls
- **Background Job Processing**: Automated nightly analytics recalculation
- **Smart Fallbacks**: Development mode with production-grade fallback implementations
- **200+ Sample Calls**: Realistic call transcripts with comprehensive AI analysis
- **Advanced API**: Full CRUD operations with complex filtering and recommendations
- **Production Ready**: Comprehensive error handling, validation, and monitoring
- **🔐 JWT Authentication**: Secure token-based authentication system
- **👥 Multi-user Support**: Role-based access control with user management

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
| `python production_ml_run.py` | 2-3 minutes | Real ML Models | Production, Full AI Features |
| `python api_demo.py` | N/A | Interactive Demo | Feature Demonstration |

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

### Authentication
```bash
POST /auth/login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"secret"}'

GET /auth/me
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Call Management
```bash
GET /api/v1/calls
# Examples:
curl "http://localhost:8000/api/v1/calls?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
curl "http://localhost:8000/api/v1/calls?agent_id=agent_001&min_sentiment=0.5" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
curl "http://localhost:8000/api/v1/calls?from_date=2025-07-01&limit=20" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

GET /api/v1/calls/{call_id}
curl "http://localhost:8000/api/v1/calls/call_123456" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

GET /api/v1/calls/{call_id}/recommendations
curl "http://localhost:8000/api/v1/calls/call_123456/recommendations" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Analytics & Reporting
```bash
GET /api/v1/analytics/agents
curl "http://localhost:8000/api/v1/analytics/agents" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

POST /api/v1/analytics/recalculate
curl -X POST "http://localhost:8000/api/v1/analytics/recalculate" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Real-time WebSocket Streaming
```javascript
// Connect to sentiment stream for a specific call
const ws = new WebSocket(`ws://localhost:8000/ws/sentiment/call_123456?token=${jwt_token}`);

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Live sentiment:', data.sentiment);
    console.log('Timestamp:', data.timestamp);
};
```

**Query Parameters for Call Filtering**:
- `limit` (1-100, default: 50): Number of calls to return
- `offset` (default: 0): Pagination offset  
- `agent_id`: Filter by specific agent
- `from_date` / `to_date`: Date range filtering
- `min_sentiment` / `max_sentiment`: Sentiment score filtering (-1 to 1)

## 🔐 JWT Authentication

All API endpoints (except `/health` and `/auth/login`) require JWT authentication.

### Demo Users
- **Username**: `admin` / **Password**: `secret` / **Email**: admin@salesanalytics.com
- **Username**: `analyst` / **Password**: `secret` / **Email**: analyst@salesanalytics.com  
- **Username**: `demo` / **Password**: `secret` / **Email**: demo@salesanalytics.com

### Authentication Flow

#### 1. Login to Get Token
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"secret"}'
```

#### 2. Use Token in Requests
```bash
curl -X GET "http://localhost:8000/api/v1/calls?limit=5" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### 3. Check User Info
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### PowerShell Examples
```powershell
# Login
$body = '{"username":"admin","password":"secret"}'
$response = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" -Method Post -ContentType "application/json" -Body $body
$token = $response.access_token

# Use token
$headers = @{"Authorization" = "Bearer $token"}
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/calls?limit=5" -Headers $headers
```

## 🌐 Real-time Features

### WebSocket Sentiment Streaming

The API provides real-time sentiment monitoring for active calls through WebSocket connections.

**Connection**: `ws://localhost:8000/ws/sentiment/{call_id}?token={jwt_token}`

**Features**:
- Live sentiment updates every 2 seconds
- JWT authentication for secure connections
- Automatic reconnection handling
- Real-time call monitoring capabilities

**JavaScript Example**:
```javascript
// Get JWT token first
const loginResponse = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'admin', password: 'secret' })
});
const { access_token } = await loginResponse.json();

// Connect to WebSocket
const ws = new WebSocket(`ws://localhost:8000/ws/sentiment/call_123456?token=${access_token}`);

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log(`Call ${data.call_id}: Sentiment = ${data.sentiment}`);
    // Update your UI with real-time sentiment data
};
```

### Background Job Processing

Automated analytics processing runs in the background without blocking API operations.

**Automatic Scheduling**:
- Runs nightly at 2:00 AM
- Recalculates all agent performance metrics
- Updates sentiment scores and talk ratios
- Processes embedding similarities

**Manual Triggers**:
```bash
curl -X POST "http://localhost:8000/api/v1/analytics/recalculate" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Monitoring**:
- Server logs show scheduled execution times
- Background task completion notifications  
- Error handling with detailed logging
- Non-blocking execution preserves API performance

## 🧪 Testing

### Automated Test Suite
```bash
python production_test.py
```
Runs comprehensive tests against all endpoints with validation.

### WebSocket Testing
Open `websocket_test.html` in your browser to test real-time sentiment streaming:
1. Enter a call ID (e.g., "call_123456")
2. Provide a valid JWT token from `/auth/login`
3. Click "Connect" to start receiving live sentiment updates
4. Watch real-time sentiment values stream every 2 seconds

### Interactive Demo  
```bash
python api_demo.py
```
Showcases all features in an interactive demonstration.

### Manual API Testing
```bash
# Test health endpoint
curl http://localhost:8000/health

# Login and get token
TOKEN=$(curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"secret"}' | jq -r '.access_token')

# Get first 5 calls
curl "http://localhost:8000/api/v1/calls?limit=5" \
  -H "Authorization: Bearer $TOKEN"

# Test filtering
curl "http://localhost:8000/api/v1/calls?min_sentiment=0.8&limit=3" \
  -H "Authorization: Bearer $TOKEN"

# Trigger background analytics recalculation
curl -X POST "http://localhost:8000/api/v1/analytics/recalculate" \
  -H "Authorization: Bearer $TOKEN"
```

### Postman Collection
Import `Sales_Analytics_API.postman_collection.json` for complete API testing with pre-configured requests and authentication.

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
3. Try interactive demo: `python api_demo.py`
4. Check logs in terminal for specific error messages

## 🏗️ Architecture & Technology

### Core Technologies
- **FastAPI**: Modern async web framework with automatic OpenAPI documentation
- **SQLAlchemy**: Async ORM with SQLite database and migration support
- **Pydantic**: Data validation and serialization with type safety
- **WebSockets**: Real-time bidirectional communication for live data streaming
- **Background Jobs**: FastAPI BackgroundTasks with threaded scheduling
- **sentence-transformers**: Semantic embeddings using all-MiniLM-L6-v2 model
- **Hugging Face Transformers**: Sentiment analysis with CardiffNLP Twitter-RoBERTa

### Advanced Features
- **Real-time Streaming**: WebSocket connections for live sentiment monitoring
- **Background Processing**: Automated nightly analytics recalculation at 2:00 AM
- **Manual Job Triggers**: On-demand analytics processing via API endpoints
- **JWT Authentication**: Secure token-based access control across all endpoints
- **Semantic Similarity**: Vector-based call recommendations using cosine similarity
- **Async Operations**: Non-blocking database operations and concurrent request handling

### AI Processing Modes
- **Production Mode**: Uses actual ML models for enterprise-quality results
- **Development Mode**: Professional fallback implementations for rapid development
- **Hybrid Processing**: Automatic fallback for missing ML dependencies
- **Embeddings**: 384-dimensional vectors for semantic similarity matching
- **Sentiment Analysis**: Multi-factor analysis with conversational context
- **Talk Ratio Calculation**: Intelligent agent vs customer speaking time analysis

### Background Job System
- **Scheduler**: Threading-based with precise datetime calculations
- **Execution**: Non-blocking background analytics recalculation
- **Monitoring**: Comprehensive logging with execution timestamps
- **Manual Override**: API endpoint for immediate job execution
- **Error Handling**: Robust exception handling with detailed error reporting

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
│   ├── main.py              # FastAPI app with WebSocket & background jobs
│   ├── auth.py              # JWT authentication system
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
├── api_demo.py              # Interactive demonstration
├── websocket_test.html      # WebSocket testing interface
├── Sales_Analytics_API.postman_collection.json  # Postman API collection
├── requirements.txt         # Python dependencies
├── sales_analytics.db       # SQLite database (auto-created)
├── alembic.ini             # Migration configuration
├── docker-compose.yml       # Docker setup (optional)
├── Dockerfile              # Container definition (optional)
└── README.md               # This documentation
```

## 🔧 Development

### Key Files Explained

- **`fast_run.py`**: Development server with quick startup and fallback AI
- **`production_ml_run.py`**: Production server with full ML models (slower startup) 
- **`generate_data.py`**: Creates realistic call data with comprehensive AI analysis
- **`production_test.py`**: Validates all endpoints including WebSocket functionality
- **`api_demo.py`**: Interactive showcase of all system capabilities
- **`websocket_test.html`**: Browser-based WebSocket testing interface
- **`Sales_Analytics_API.postman_collection.json`**: Complete API testing collection

### Adding Features

1. **New REST Endpoints**: Add to `app/main.py` with proper Pydantic validation
2. **WebSocket Endpoints**: Extend WebSocket handlers in `app/main.py`
3. **Background Jobs**: Add new scheduled tasks to the background job system
4. **Database Changes**: Create migrations in `alembic/versions/`
5. **AI Processing**: Extend `app/ai_insights.py` with new analysis methods
6. **Testing**: Update `production_test.py` with new test cases

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

## 💡 Core Capabilities

### Production-Grade Features
- ✅ **ML-Powered Analytics**: Actual sentence-transformers and Hugging Face models
- ✅ **Real-time Streaming**: WebSocket connections for live sentiment monitoring
- ✅ **Background Processing**: Automated nightly analytics with manual triggers
- ✅ **Smart Fallbacks**: Instant startup even without heavy ML dependencies  
- ✅ **Comprehensive Dataset**: 200+ realistic calls with proper conversation patterns
- ✅ **Enterprise Architecture**: Async FastAPI with robust error handling
- ✅ **Security**: JWT authentication across all endpoints including WebSockets
- ✅ **Monitoring**: Detailed logging and health checks
- ✅ **API Documentation**: Auto-generated OpenAPI specs with interactive testing

### Data Quality & Processing
- **20 Realistic Agents** with consistent behavioral patterns
- **Diverse Scenarios**: Technical support, billing inquiries, complaints, sales calls
- **Natural Conversations**: Authentic dialogue flow between agents and customers
- **Meaningful Metrics**: Accurate talk ratios, sentiment scores, and semantic embeddings
- **Time Distribution**: Calls distributed across realistic business hours
- **Vector Similarity**: Cosine similarity matching for call recommendations
- **Background Analytics**: Nightly recalculation of agent performance metrics

### Development Experience
- **Fast Development**: 5-second startup with fallback implementations
- **Production Testing**: Full ML pipeline with 2-3 minute initialization
- **Comprehensive Testing**: Automated validation of all endpoints and WebSocket connections
- **Interactive Demo**: Multiple showcase modes for different audiences
- **API Collection**: Complete Postman collection for thorough testing
- **WebSocket Testing**: Browser-based interface for real-time feature validation

## 🎯 Technical Implementation

This system demonstrates advanced Python development practices:
- **FastAPI Expertise**: Modern async web development with WebSocket support
- **Database Design**: SQLAlchemy with proper indexing, migrations, and async operations
- **AI/ML Integration**: Production ML models with intelligent fallback strategies
- **Real-time Systems**: WebSocket implementation for live data streaming
- **Background Processing**: Threaded job scheduling with error handling
- **Security Implementation**: JWT authentication across REST and WebSocket endpoints
- **Testing Practices**: Comprehensive automated testing including WebSocket validation
- **Clean Architecture**: Modular, maintainable code structure with proper separation of concerns
- **Production Monitoring**: Detailed logging, health checks, and error reporting
- **API Design**: RESTful endpoints with comprehensive OpenAPI documentation

## 📞 Getting Started

This is a complete, working microservice ready for production deployment. All described features are implemented and tested.

**Quick Verification**:
```bash
python fast_run.py        # Starts in 5 seconds
python production_test.py  # Validates everything works
python api_demo.py   # Interactive showcase
```

**WebSocket Testing**:
1. Start the server: `python fast_run.py`
2. Open `websocket_test.html` in your browser
3. Login via API to get JWT token
4. Connect to WebSocket and watch live sentiment streaming

**Background Jobs**:
- Automatic: Analytics recalculation runs nightly at 2:00 AM
- Manual: Trigger via `POST /api/v1/analytics/recalculate`
- Monitoring: Check server logs for execution details

---

**Built for enterprise applications and technical demonstrations**