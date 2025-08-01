#!/usr/bin/env python3
"""
Sample data generator for Sales Analytics Microservice
Creates realistic call records with proper embeddings and analysis
"""
import asyncio
import os
import random
import json
import uuid
from datetime import datetime, timedelta
from typing import List
import sys

# Add the app directory to Python path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import AsyncSessionLocal, engine
from app.models import Base, CallRecord
from app.ai_insights import AIInsightsProcessor
from sqlalchemy import select, func

# Sample data for generating realistic call records
AGENT_IDS = [
    "AGT001", "AGT002", "AGT003", "AGT004", "AGT005",
    "AGT006", "AGT007", "AGT008", "AGT009", "AGT010"
]

CUSTOMER_IDS = [
    f"CUST{str(i).zfill(3)}" for i in range(1, 151)  # 150 unique customers
]

SAMPLE_TRANSCRIPTS = [
    """Agent: Hello! Thank you for calling customer support. How can I help you today?
Customer: Hi, I'm having trouble with my recent order. It hasn't arrived yet.
Agent: I'm sorry to hear that. Can you provide me with your order number?
Customer: Yes, it's ORD-12345.
Agent: Let me check that for you. I see your order was shipped 3 days ago. Let me track it for you.
Customer: Okay, thank you.
Agent: Good news! Your package is out for delivery today and should arrive by 6 PM.
Customer: Oh great! Thank you so much for checking that.
Agent: You're welcome! Is there anything else I can help you with?
Customer: No, that's all. Thanks again!
Agent: Have a wonderful day!""",

    """Agent: Good morning! How can I assist you today?
Customer: I'm really frustrated. I've been trying to cancel my subscription for weeks.
Agent: I understand your frustration. Let me help you with that right away.
Customer: I've called three times already and nobody seems to know how to do it.
Agent: I apologize for the poor experience. I'll make sure we get this resolved today.
Customer: This is ridiculous. I just want to cancel.
Agent: I've found your account. I can process the cancellation immediately. Would you like me to do that now?
Customer: Yes, please. Finally someone who can help.
Agent: Done! Your subscription is cancelled and you'll receive a confirmation email shortly.
Customer: Thank you. That wasn't so hard, was it?
Agent: Again, I apologize for the previous experiences. Is there anything else I can help with?
Customer: No, that's it. Thanks for actually helping.""",

    """Agent: Thank you for calling. How may I help you?
Customer: Hi, I need to update my billing address.
Agent: I'd be happy to help with that. Can you verify your account information first?
Customer: Sure, my phone number is 555-0123.
Agent: Perfect. What's the new address you'd like to use?
Customer: It's 123 Main Street, Anytown, State 12345.
Agent: Let me update that for you. All done! Your new billing address is now active.
Customer: That was easy. Thank you!
Agent: You're welcome! Anything else I can help with today?
Customer: No, that's all. Have a good day.
Agent: You too!""",

    """Agent: Hello, thank you for holding. How can I help you?
Customer: My internet has been down for 2 hours. This is unacceptable.
Agent: I'm very sorry about the service interruption. Let me check what's happening in your area.
Customer: I work from home and this is costing me money.
Agent: I completely understand. I see there's a known outage affecting your neighborhood.
Customer: When will it be fixed? I need an exact time.
Agent: Our technicians estimate service will be restored within the next hour.
Customer: That's what they said an hour ago. This is terrible service.
Agent: I understand your frustration. As compensation, I can credit your account for today's outage.
Customer: Fine, but this better not happen again.
Agent: I'll make a note on your account about this issue. The credit will appear on your next bill.
Customer: Okay, thank you for that at least.""",

    """Agent: Good afternoon! How can I assist you today?
Customer: I love your new product features! The interface is so much better.
Agent: That's wonderful to hear! We've been working hard on improvements.
Customer: The mobile app especially is fantastic. Much faster than before.
Agent: I'm so glad you're enjoying it. Was there something specific you needed help with?
Customer: Just wanted to give feedback, but also wondering about the premium features.
Agent: I'd be happy to explain our premium options. What features are you most interested in?
Customer: The advanced analytics look really useful for my business.
Agent: Those are very popular. I can upgrade your account and give you a 30-day free trial.
Customer: That sounds perfect! How do we do that?
Agent: I'll process that upgrade now. You'll have access immediately.
Customer: Excellent! Thank you so much for the great service.
Agent: My pleasure! Let me know if you have any questions about the new features."""
]

class DataGenerator:
    def __init__(self):
        # Check if we should use real ML models
        use_real_ml = os.environ.get('USE_REAL_ML', 'false').lower() == 'true'
        self.ai_processor = AIInsightsProcessor(use_real_models=use_real_ml)
        
    async def create_database_tables(self):
        """Create all database tables"""
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created")
    
    def generate_call_record(self, call_number: int) -> CallRecord:
        """Generate a single realistic call record"""
        
        # Random timing (last 30 days)
        start_time = datetime.now() - timedelta(
            days=random.randint(0, 30),
            hours=random.randint(8, 18),  # Business hours
            minutes=random.randint(0, 59)
        )
        
        # Select random transcript and add variations
        base_transcript = random.choice(SAMPLE_TRANSCRIPTS)
        
        # Generate other realistic data
        duration = random.randint(120, 1800)  # 2-30 minutes
        agent_id = random.choice(AGENT_IDS)
        customer_id = random.choice(CUSTOMER_IDS)
        
        # Create call record
        call = CallRecord(
            call_id=f"CALL-{str(call_number).zfill(6)}",
            agent_id=agent_id,
            customer_id=customer_id,
            language="en",
            start_time=start_time,
            duration_seconds=duration,
            transcript=base_transcript
        )
        
        # Calculate AI insights
        call.agent_talk_ratio = self.ai_processor.calculate_talk_ratio(base_transcript)
        call.customer_sentiment_score = self.ai_processor.calculate_sentiment(base_transcript)
        
        # Generate embedding
        embedding = self.ai_processor.generate_embedding(base_transcript)
        if embedding:
            call.embedding = embedding
        
        return call
    
    async def generate_sample_data(self, num_records: int = 200):
        """Generate sample call records"""
        print(f"🔄 Generating {num_records} sample call records...")
        
        # Create records in batches for better performance
        batch_size = 50
        total_created = 0
        
        for batch_start in range(0, num_records, batch_size):
            batch_end = min(batch_start + batch_size, num_records)
            batch_records = []
            
            for i in range(batch_start, batch_end):
                call = self.generate_call_record(i + 1)
                batch_records.append(call)
            
            # Insert batch
            async with AsyncSessionLocal() as session:
                session.add_all(batch_records)
                await session.commit()
            
            total_created += len(batch_records)
            print(f"  ✅ Created {total_created}/{num_records} records")
        
        print(f"✅ Generated {total_created} call records successfully")

async def main():
    """Main data generation function"""
    print("📊 Sales Analytics Data Generator")
    print("=" * 40)
    
    generator = DataGenerator()
    
    # Create database tables
    await generator.create_database_tables()
    
    # Check if data already exists
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(func.count(CallRecord.id)))
        existing_records = result.scalar()
    
    if existing_records > 0:
        print(f"ℹ️  Database already contains {existing_records} records")
        if input("Regenerate data? This will delete existing records (y/n): ").lower() != 'y':
            print("✅ Keeping existing data")
            return
        
        # Clear existing data
        async with AsyncSessionLocal() as session:
            from sqlalchemy import delete
            await session.execute(delete(CallRecord))
            await session.commit()
        print("🗑️  Cleared existing data")
    
    # Generate new data
    await generator.generate_sample_data(200)
    
    # Verify data creation
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(func.count(CallRecord.id)))
        final_count = result.scalar()
    
    print(f"✅ Data generation complete! Created {final_count} call records")
    print("\n📋 Summary:")
    print(f"  • Total calls: {final_count}")
    print(f"  • Agents: {len(AGENT_IDS)}")
    print(f"  • Customers: {len(CUSTOMER_IDS)}")
    print(f"  • Time range: Last 30 days")
    print(f"  • AI Features: {'Real ML models' if generator.ai_processor.use_real_models else 'Fast fallback implementations'}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("\n🎉 Data generation completed successfully!")
    except Exception as e:
        print(f"\n❌ Data generation failed: {e}")
        sys.exit(1)
