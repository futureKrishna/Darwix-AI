A Python microservice that ingests sales call transcripts, stores them durably, and serves actionable conversation analytics through a REST API.

## Features

- **Async Data Ingestion**: Processes 200+ call transcripts using asyncio
- **AI-Powered Insights**: Sentiment analysis, talk ratio calculation, and semantic similarity
- **Full-Text Search**: PostgreSQL with pg_trgm extension for transcript search
- **REST API**: FastAPI with comprehensive endpoints
- **Vector Similarity**: Cosine similarity for call recommendations
- **LLM Integration**: OpenAI integration for coaching recommendations

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone and setup**:
```bash
git clone <repository>
cd sales-analytics-microservice
```

2. **Set environment variables** (optional):
```bash
export OPENAI_API_KEY="your-openai-key"  # Optional for coaching nudges
```

3. **Start the services**:
```bash
docker-compose up --build
```

This will:
- Start PostgreSQL database
- Run database migrations
- Generate and ingest 200 synthetic call records
- Start the FastAPI server on http://localhost:8000

### Manual Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Setup PostgreSQL**:
```bash
createdb sales_analytics
export DATABASE_URL="postgresql+asyncpg://user:password@localhost/sales_analytics"
```

3. **Run migrations**:
```bash
alembic upgrade head
```

4. **Generate and ingest data**:
```bash
python run_ingestion.py
```

5. **Start the server**:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### GET /api/v1/calls
Get calls with filtering and pagination.

**Query Parameters**:
- `limit` (int): Number of calls to return (1-100, default: 50)
- `offset` (int): Pagination offset (default: 0)
- `agent_id` (str): Filter by agent ID
- `from_date` (datetime): Filter calls from this date
- `to_date` (datetime): Filter calls until this date
- `min_sentiment` (float): Minimum sentiment score (-1 to 1)
- `max_sentiment` (float): Maximum sentiment score (-1 to 1)

**Example**:
```bash
curl "http://localhost:8000/api/v1/calls?limit=10&agent_id=agent_001&min_sentiment=0.5"
```

### GET /api/v1/calls/{call_id}
Get complete details of a specific call.

**Example**:
```bash
curl "http://localhost:8000/api/v1/calls/call_123456"
```

### GET /api/v1/calls/{call_id}/recommendations
Get 5 most similar calls and 3 coaching nudges for a specific call.

**Example**:
```bash
curl "http://localhost:8000/api/v1/calls/call_123456/recommendations"
```

### GET /api/v1/analytics/agents
Get agent performance leaderboard with averages for sentiment, talk ratio, and call count.

**Example**:
```bash
curl "http://localhost:8000/api/v1/analytics/agents"
```

## Testing

Run the API tests:
```bash
python test_api.py
```

## Architecture

### Data Models
- **CallRecord**: Main model storing call data and AI insights
- **Indexes**: Optimized for agent_id, start_time, and full-text search

### AI Processing
- **Sentence Transformers**: all-MiniLM-L6-v2 for embeddings
- **Sentiment Analysis**: CardiffNLP Twitter-RoBERTa model
- **Talk Ratio**: Agent vs customer word count (excluding fillers)
- **Similarity**: Cosine similarity on sentence embeddings

### Database Schema
```sql
-- Key indexes for performance
CREATE INDEX idx_agent_id ON call_records(agent_id);
CREATE INDEX idx_start_time ON call_records(start_time);
CREATE INDEX idx_transcript_gin_trgm ON call_records USING gin(transcript gin_trgm_ops);
```

The `pg_trgm` extension provides better partial matching and typo tolerance compared to basic full-text search, making it ideal for searching through conversational transcripts.

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: Optional, for enhanced coaching recommendations

## Data Generation

The system generates realistic synthetic call transcripts including:
- **20 agents** with consistent IDs
- **Multiple conversation topics**: billing, technical support, complaints
- **Realistic dialogue patterns** between agents and customers
- **Varied call durations** and timestamps

## Performance Considerations

- **Batch Processing**: Ingestion processes calls in configurable batches
- **Async Operations**: All I/O operations use asyncio for concurrency
- **Database Indexing**: Optimized indexes for common query patterns
- **Embedding Caching**: AI insights stored to avoid recomputation

## Development

### Project Structure
```
├── app/
│   ├── models.py          # SQLAlchemy models
│   ├── database.py        # Database configuration
│   ├── schemas.py         # Pydantic models
│   ├── services.py        # Business logic
│   ├── ingestion.py       # Data pipeline
│   ├── ai_insights.py     # AI processing
│   ├── data_generator.py  # Synthetic data
│   └── main.py           # FastAPI app
├── alembic/              # Database migrations
├── data/                 # Generated datasets
├── requirements.txt      # Dependencies
├── docker-compose.yml    # Container orchestration
└── README.md            # Documentation
```

### Adding New Features

1. **Models**: Add to `app/models.py` and create migration
2. **API**: Add endpoints to `app/main.py` with proper validation
3. **Services**: Implement business logic in `app/services.py`
4. **Tests**: Update `test_api.py` with new test cases

## Monitoring

- Health check endpoint: `GET /health`
- Database connection pooling with SQLAlchemy
- Comprehensive error handling and logging
- Request/response validation with Pydantic

## Deployment

The service is containerized and ready for deployment:
- Docker multi-stage builds for optimization
- Health checks for container orchestration
- Environment-based configuration
- Database migration automation