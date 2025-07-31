"""Add comprehensive indexes for production performance

Revision ID: 002_add_production_indexes
Revises: 001_initial_migration
Create Date: 2025-08-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002_add_production_indexes'
down_revision = '001_initial_migration'
branch_labels = None
depends_on = None

def upgrade():
    """Add production-ready indexes"""
    
    # Individual column indexes (if not already existing)
    try:
        op.create_index('ix_call_records_call_id', 'call_records', ['call_id'])
    except:
        pass  # Index might already exist
        
    try:
        op.create_index('ix_call_records_agent_id', 'call_records', ['agent_id'])
    except:
        pass
        
    try:
        op.create_index('ix_call_records_start_time', 'call_records', ['start_time'])
    except:
        pass
        
    try:
        op.create_index('ix_call_records_agent_talk_ratio', 'call_records', ['agent_talk_ratio'])
    except:
        pass
        
    try:
        op.create_index('ix_call_records_customer_sentiment_score', 'call_records', ['customer_sentiment_score'])
    except:
        pass
        
    try:
        op.create_index('ix_call_records_created_at', 'call_records', ['created_at'])
    except:
        pass
    
    # Composite indexes for optimized queries
    try:
        op.create_index('idx_agent_start_time', 'call_records', ['agent_id', 'start_time'])
    except:
        pass
        
    try:
        op.create_index('idx_sentiment_time', 'call_records', ['customer_sentiment_score', 'start_time'])
    except:
        pass
        
    try:
        op.create_index('idx_agent_sentiment', 'call_records', ['agent_id', 'customer_sentiment_score'])
    except:
        pass

def downgrade():
    """Remove production indexes"""
    
    # Remove composite indexes
    try:
        op.drop_index('idx_agent_sentiment', table_name='call_records')
    except:
        pass
        
    try:
        op.drop_index('idx_sentiment_time', table_name='call_records')
    except:
        pass
        
    try:
        op.drop_index('idx_agent_start_time', table_name='call_records')
    except:
        pass
    
    # Remove individual indexes
    try:
        op.drop_index('ix_call_records_created_at', table_name='call_records')
    except:
        pass
        
    try:
        op.drop_index('ix_call_records_customer_sentiment_score', table_name='call_records')
    except:
        pass
        
    try:
        op.drop_index('ix_call_records_agent_talk_ratio', table_name='call_records')
    except:
        pass
        
    try:
        op.drop_index('ix_call_records_start_time', table_name='call_records')
    except:
        pass
        
    try:
        op.drop_index('ix_call_records_agent_id', table_name='call_records')
    except:
        pass
        
    try:
        op.drop_index('ix_call_records_call_id', table_name='call_records')
    except:
        pass
