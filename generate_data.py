import asyncio
import json
from faker import Faker
from datetime import datetime, timedelta
from sqlalchemy import insert
from app.models import CallRecord, Base
from app.database import engine, AsyncSessionLocal
from app.ai_insights import AIInsightsProcessor
import random
import os

fake = Faker()

# Diverse transcript templates for realistic data
TRANSCRIPT_TEMPLATES = [
    # Order inquiry
    """Agent: Thank you for calling {company}, how can I help you today?
Customer: Hi, I have a question about my recent order.
Agent: I'd be happy to help you with that. Can you provide your order number?
Customer: Sure, it's ORDER-{order_num}.
Agent: Let me look that up for you. I can see your order here.
Customer: Great, when will it be delivered?
Agent: It should arrive within 2-3 business days.
Customer: Perfect, thank you for your help!
Agent: You're welcome! Is there anything else I can help you with?
Customer: No, that's all. Have a great day!
Agent: You too, goodbye!""",

    # Billing issue
    """Agent: Good morning, this is {agent_name} from customer service. How may I assist you?
Customer: I'm calling about a charge on my account that I don't recognize.
Agent: I understand your concern. Can you please provide me with your account number?
Customer: Yes, it's {account_num}.
Agent: Thank you. I can see the charge you're referring to. This appears to be for our premium service upgrade.
Customer: I never signed up for that! This is frustrating.
Agent: I apologize for the confusion. Let me remove this charge immediately and ensure it doesn't happen again.
Customer: Thank you, I appreciate you resolving this quickly.
Agent: Of course! The refund will appear in 3-5 business days. Is there anything else I can help you with?
Customer: No, that covers everything. Thanks again.
Agent: You're very welcome. Have a wonderful day!""",

    # Product support
    """Agent: Hi there! Thanks for calling {company} support. What can I help you with today?
Customer: I'm having trouble setting up my new device.
Agent: I'd be glad to walk you through the setup process. What type of device are you working with?
Customer: It's the {product_name} model.
Agent: Excellent choice! Let's start with the initial setup. Do you have the device powered on?
Customer: Yes, it's on but I'm stuck on the configuration screen.
Agent: No problem at all. Let me guide you step by step through the configuration.
Customer: This is great, it's working now! You explained it so clearly.
Agent: Wonderful! I'm so glad we got that sorted out for you.
Customer: You've been incredibly helpful. Thank you so much!
Agent: It was my pleasure! Feel free to call back if you need any other assistance.""",

    # Complaint resolution
    """Agent: Thank you for calling. My name is {agent_name}. How can I make your day better?
Customer: I need to complain about terrible service I received at your store yesterday.
Agent: I'm very sorry to hear about your poor experience. Can you tell me more about what happened?
Customer: The staff was rude and unhelpful. I waited 30 minutes just to get basic information.
Agent: That's completely unacceptable, and I sincerely apologize. Which location was this?
Customer: The downtown branch on Main Street.
Agent: I'm going to escalate this to the store manager immediately and follow up personally.
Customer: I appreciate that, but I'm really considering taking my business elsewhere.
Agent: I completely understand your frustration. Let me see what I can do to make this right.
Customer: Well, I suppose I'll give you one more chance to fix this.
Agent: Thank you for that opportunity. I promise we'll do better moving forward."""
]

async def generate_data():
    """Generate realistic call data with proper AI insights"""
    print("Starting data generation...")
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Check if we should use real ML models
    use_real_ml = os.getenv('USE_REAL_ML', 'false').lower() == 'true'
    
    # Initialize AI processor
    ai_processor = AIInsightsProcessor(use_real_models=use_real_ml)
    
    if use_real_ml:
        print("🧠 Using production ML models for high-quality AI insights")
    else:
        print("🚀 Using fast fallback implementations for development")
    
    # Generate agent IDs and other data
    agents = [f"agent_{i:03d}" for i in range(1, 21)]  # 20 agents
    companies = ["TechCorp", "ServicePlus", "CustomerFirst", "SolutionsPro"]
    products = ["SmartDevice Pro", "UltraConnect", "PowerSync", "CloudLink"]
    
    sample_calls = []
    print(f"Generating 200 realistic call transcripts...")
    
    for i in range(200):  # Generate 200 calls as required
        if i % 50 == 0:
            print(f"   Progress: {i}/200 calls generated...")
            
        # Create diverse, realistic transcript
        template = random.choice(TRANSCRIPT_TEMPLATES)
        transcript = template.format(
            company=random.choice(companies),
            agent_name=fake.first_name(),
            order_num=fake.random_number(digits=6),
            account_num=fake.random_number(digits=8),
            product_name=random.choice(products)
        )
        
        call_data = {
            'call_id': f'call_{fake.uuid4()}',
            'agent_id': random.choice(agents),
            'customer_id': f'customer_{fake.uuid4()}',
            'language': random.choice(['en', 'en-US', 'en-GB']),
            'start_time': fake.date_time_between(start_date='-30d', end_date='now'),
            'duration_seconds': random.randint(120, 900),  # 2-15 minutes
            'transcript': transcript
        }
        
        # Process with real AI models
        insights = await ai_processor.process_call_insights(call_data)
        
        # Handle embedding separately since it's a property
        embedding_data = insights.pop('embedding', None)
        call_data.update(insights)
        
        # Convert embedding to JSON string for database storage
        if embedding_data:
            call_data['embedding_json'] = json.dumps(embedding_data)
        
        sample_calls.append(call_data)
    
    print("Storing calls in database...")
    async with AsyncSessionLocal() as session:
        # Insert in batches for better performance
        batch_size = 50
        for i in range(0, len(sample_calls), batch_size):
            batch = sample_calls[i:i + batch_size]
            await session.execute(insert(CallRecord).values(batch))
            await session.commit()
            print(f"   Stored batch {i//batch_size + 1}/{(len(sample_calls) + batch_size - 1)//batch_size}")
    
    print(f"Generated {len(sample_calls)} sample calls with real AI insights")

if __name__ == "__main__":
    asyncio.run(generate_data())
