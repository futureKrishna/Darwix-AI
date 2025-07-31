"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create extension for pg_trgm
    op.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm;')
    
    # Create call_records table
    op.create_table('call_records',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('call_id', sa.String(length=100), nullable=False),
    sa.Column('agent_id', sa.String(length=100), nullable=False),
    sa.Column('customer_id', sa.String(length=100), nullable=False),
    sa.Column('language', sa.String(length=10), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('duration_seconds', sa.Integer(), nullable=False),
    sa.Column('transcript', sa.Text(), nullable=False),
    sa.Column('agent_talk_ratio', sa.Float(), nullable=True),
    sa.Column('customer_sentiment_score', sa.Float(), nullable=True),
    sa.Column('embedding', postgresql.ARRAY(sa.Float()), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_call_records_agent_id'), 'call_records', ['agent_id'], unique=False)
    op.create_index(op.f('ix_call_records_call_id'), 'call_records', ['call_id'], unique=True)
    op.create_index(op.f('ix_call_records_start_time'), 'call_records', ['start_time'], unique=False)
    
    # Create GIN index for full-text search using pg_trgm
    op.create_index(
        'idx_transcript_gin_trgm', 
        'call_records', 
        ['transcript'], 
        unique=False,
        postgresql_using='gin',
        postgresql_ops={'transcript': 'gin_trgm_ops'}
    )

def downgrade() -> None:
    op.drop_index('idx_transcript_gin_trgm', table_name='call_records')
    op.drop_index(op.f('ix_call_records_start_time'), table_name='call_records')
    op.drop_index(op.f('ix_call_records_call_id'), table_name='call_records')
    op.drop_index(op.f('ix_call_records_agent_id'), table_name='call_records')
    op.drop_table('call_records')
    op.execute('DROP EXTENSION IF EXISTS pg_trgm;')