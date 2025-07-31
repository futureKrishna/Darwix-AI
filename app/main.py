from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.database import get_db
from app.models import CallRecord
from app.schemas import *
from app.auth import (
    authenticate_user, create_access_token, get_current_user, 
    optional_auth, ACCESS_TOKEN_EXPIRE_MINUTES
)
from typing import Optional
from datetime import datetime, timedelta
import math

app = FastAPI(
    title="Sales Call Analytics API", 
    version="1.1.0",
    description="Sales call analytics API with JWT authentication"
)

def cosine_similarity(a, b):
    if not a or not b or len(a) != len(b):
        return 0.0
    
    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(x * x for x in b))
    
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    
    return dot_product / (magnitude_a * magnitude_b)

# Public endpoints (no authentication required)
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/auth/login", response_model=Token)
async def login(login_data: LoginRequest):
    """Login endpoint to get JWT token"""
    user = authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user_info": {
            "username": user["username"],
            "email": user["email"]
        }
    }

@app.get("/auth/me", response_model=UserInfo)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return {
        "username": current_user["username"],
        "email": current_user["email"]
    }

# Protected endpoints (require authentication)
@app.get("/api/v1/calls", response_model=CallsListResponse)
async def get_calls(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    agent_id: Optional[str] = Query(None),
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    min_sentiment: Optional[float] = Query(None, ge=-1, le=1),
    max_sentiment: Optional[float] = Query(None, ge=-1, le=1),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # JWT protection
):
    query = select(CallRecord)
    count_query = select(func.count(CallRecord.id))
    
    conditions = []
    if agent_id:
        conditions.append(CallRecord.agent_id == agent_id)
    if from_date:
        conditions.append(CallRecord.start_time >= from_date)
    if to_date:
        conditions.append(CallRecord.start_time <= to_date)
    if min_sentiment is not None:
        conditions.append(CallRecord.customer_sentiment_score >= min_sentiment)
    if max_sentiment is not None:
        conditions.append(CallRecord.customer_sentiment_score <= max_sentiment)
    
    if conditions:
        query = query.where(and_(*conditions))
        count_query = count_query.where(and_(*conditions))
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    query = query.order_by(CallRecord.start_time.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    calls = result.scalars().all()
    
    return CallsListResponse(
        calls=[CallRecordResponse.model_validate(call) for call in calls],
        total=total, limit=limit, offset=offset
    )

@app.get("/api/v1/calls/{call_id}", response_model=CallRecordResponse)
async def get_call(
    call_id: str, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # JWT protection
):
    query = select(CallRecord).where(CallRecord.call_id == call_id)
    result = await db.execute(query)
    call = result.scalar_one_or_none()
    
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    return CallRecordResponse.model_validate(call)

@app.get("/api/v1/calls/{call_id}/recommendations", response_model=CallRecommendationsResponse)
async def get_call_recommendations(
    call_id: str, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Basic authentication
):
    # Get target call
    query = select(CallRecord).where(CallRecord.call_id == call_id)
    result = await db.execute(query)
    target_call = result.scalar_one_or_none()
    
    if not target_call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    if not target_call.embedding:
        return CallRecommendationsResponse(similar_calls=[], coaching_nudges=[])
    
    # Get other calls
    query = select(CallRecord).where(CallRecord.call_id != call_id)
    result = await db.execute(query)
    all_calls = result.scalars().all()
    
    similarities = []
    target_embedding = target_call.embedding
    
    for call in all_calls:
        if call.embedding:
            similarity = cosine_similarity(target_embedding, call.embedding)
            similarities.append((call, similarity))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_similar = similarities[:5]
    
    similar_calls = [
        CallRecommendation(
            call_id=call.call_id,
            similarity_score=float(sim_score),
            agent_id=call.agent_id,
            customer_sentiment_score=call.customer_sentiment_score
        )
        for call, sim_score in top_similar
    ]
    
    # Generate coaching nudges based on call analysis
    coaching_nudges = generate_coaching_nudges(target_call, similar_calls)
    
    return CallRecommendationsResponse(
        similar_calls=similar_calls,
        coaching_nudges=coaching_nudges
    )

def generate_coaching_nudges(target_call, similar_calls):
    """Generate contextual coaching nudges based on call analysis"""
    nudges = []
    
    # Analyze sentiment patterns
    if target_call.customer_sentiment_score and target_call.customer_sentiment_score < 0:
        nudges.append("Practice empathy - acknowledge customer frustration before offering solutions.")
    elif target_call.customer_sentiment_score and target_call.customer_sentiment_score > 0.5:
        nudges.append("Great positive interaction! Maintain this energy in future calls.")
    
    # Analyze talk ratio
    if target_call.agent_talk_ratio and target_call.agent_talk_ratio > 0.7:
        nudges.append("Try active listening - let customers express concerns fully before responding.")
    elif target_call.agent_talk_ratio and target_call.agent_talk_ratio < 0.3:
        nudges.append("Take initiative - guide the conversation with proactive questions and solutions.")
    
    # Default professional nudges if not enough specific insights
    if len(nudges) < 3:
        default_nudges = [
            "Summarize key points to ensure customer understanding and agreement.",
            "Use positive language and avoid negative words like 'can't' or 'won't'.",
            "Ask open-ended questions to better understand customer needs.",
            "Confirm next steps and set clear expectations before ending calls.",
            "Practice patience - some customers need more time to process information."
        ]
        # Add random default nudges to reach 3 total
        import random
        remaining = 3 - len(nudges)
        nudges.extend(random.sample(default_nudges, min(remaining, len(default_nudges))))
    
    return nudges[:3]  # Return exactly 3 nudges as specified

@app.get("/api/v1/analytics/agents", response_model=List[AgentAnalytics])
async def get_agent_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Basic authentication
):
    query = select(
        CallRecord.agent_id,
        func.avg(CallRecord.customer_sentiment_score).label('avg_sentiment'),
        func.avg(CallRecord.agent_talk_ratio).label('avg_talk_ratio'),
        func.count(CallRecord.id).label('total_calls')
    ).group_by(CallRecord.agent_id).order_by(func.avg(CallRecord.customer_sentiment_score).desc())
    
    result = await db.execute(query)
    analytics = result.all()
    
    return [
        AgentAnalytics(
            agent_id=row.agent_id,
            avg_sentiment=float(row.avg_sentiment or 0),
            avg_talk_ratio=float(row.avg_talk_ratio or 0),
            total_calls=row.total_calls
        )
        for row in analytics
    ]
