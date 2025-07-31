from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class CallRecord(Base):
    __tablename__ = "call_records"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    call_id = Column(String(100), unique=True, nullable=False, index=True)
    agent_id = Column(String(100), nullable=False, index=True)  # Index as required
    customer_id = Column(String(100), nullable=False)
    language = Column(String(10), nullable=False, default="en")
    start_time = Column(DateTime, nullable=False, index=True)  # Index as required
    duration_seconds = Column(Integer, nullable=False)
    transcript = Column(Text, nullable=False)
    agent_talk_ratio = Column(Float, index=True)  # Index for analytics queries
    customer_sentiment_score = Column(Float, index=True)  # Index for filtering
    embedding_json = Column(Text)  # Storing embeddings as JSON for SQLite compatibility
    created_at = Column(DateTime, server_default=func.now(), index=True)
    
    # Composite indexes for common query patterns
    __table_args__ = (
        Index('idx_agent_start_time', 'agent_id', 'start_time'),  # Agent performance queries
        Index('idx_sentiment_time', 'customer_sentiment_score', 'start_time'),  # Sentiment analysis
        Index('idx_agent_sentiment', 'agent_id', 'customer_sentiment_score'),  # Agent sentiment analysis
    )
    
    @property
    def embedding(self):
        """
        Get embedding as Python list from JSON storage
        Note: Using JSON storage instead of vector extension for SQLite compatibility
        In production with PostgreSQL, would use pgvector extension
        """
        if self.embedding_json:
            import json
            try:
                return json.loads(self.embedding_json)
            except:
                return None
        return None
    
    @embedding.setter
    def embedding(self, value):
        """Set embedding by converting Python list to JSON string"""
        if value is not None:
            import json
            self.embedding_json = json.dumps(value)
        else:
            self.embedding_json = None

# Comment explaining index choices (as requested in requirements):
"""
Index Strategy Explanation:

1. agent_id (B-tree index): Required for filtering calls by agent, used in analytics queries
2. start_time (B-tree index): Required for date range filtering, temporal queries
3. agent_talk_ratio & customer_sentiment_score (B-tree indexes): For analytics filtering
4. Composite indexes:
   - idx_agent_start_time: Optimizes agent performance queries over time periods
   - idx_sentiment_time: Optimizes sentiment analysis over time
   - idx_agent_sentiment: Optimizes per-agent sentiment analysis

Full-text search considerations:
- For SQLite: Using simple LIKE queries on transcript (basic full-text capability)
- For PostgreSQL production: Would add tsvector column with GIN index for full-text search:
  transcript_search tsvector GENERATED ALWAYS AS (to_tsvector('english', transcript)) STORED
  CREATE INDEX idx_transcript_gin ON call_records USING GIN(transcript_search);
  
- Alternative: pg_trgm extension for fuzzy text matching:
  CREATE EXTENSION pg_trgm;
  CREATE INDEX idx_transcript_trgm ON call_records USING GIN(transcript gin_trgm_ops);

Current implementation uses JSON for embeddings (SQLite compatible).
Production PostgreSQL would use pgvector extension for native vector operations.
"""
