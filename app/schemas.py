from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CallRecordResponse(BaseModel):
    id: str
    call_id: str
    agent_id: str
    customer_id: str
    language: str
    start_time: datetime
    duration_seconds: int
    transcript: str
    agent_talk_ratio: Optional[float] = None
    customer_sentiment_score: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class CallRecommendation(BaseModel):
    call_id: str
    similarity_score: float
    agent_id: str
    customer_sentiment_score: Optional[float]

class CallRecommendationsResponse(BaseModel):
    similar_calls: List[CallRecommendation]
    coaching_nudges: List[str]

class AgentAnalytics(BaseModel):
    agent_id: str
    avg_sentiment: float
    avg_talk_ratio: float
    total_calls: int

class CallsListResponse(BaseModel):
    calls: List[CallRecordResponse]
    total: int
    limit: int
    offset: int
