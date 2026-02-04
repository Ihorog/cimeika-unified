"""Initial schema with pgvector

Revision ID: 777d0bc4fdf7
Revises: 
Create Date: 2026-02-04 20:40:14.094115

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision = '777d0bc4fdf7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable extensions
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    
    # Create persona_type enum
    persona_type = postgresql.ENUM(
        'Ci', 'Kazkar', 'Nastrij', 'Podija', 'Malya', 'Gallery', 'Calendar',
        name='personaenum',
        create_type=False
    )
    persona_type.create(op.get_bind(), checkfirst=True)
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_username', 'users', ['username'])
    
    # Create personas table
    op.create_table(
        'personas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', persona_type, nullable=False),
        sa.Column('base_prompt', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('idx_personas_name', 'personas', ['name'])
    
    # Seed personas data
    op.execute("""
        INSERT INTO personas (name, base_prompt, description) VALUES
        ('Ci', 'Ти Ці — центральний координатор екосистеми Cimeika.', 'Central orchestration and coordination module'),
        ('Kazkar', 'Ти Казкар — хранитель спогадів і історій.', 'Memory and story keeper, guardian of legends'),
        ('Nastrij', 'Ти Настрій — емоційний аналітик.', 'Emotional state analyzer and mood tracker'),
        ('Podija', 'Ти Подія — майстер подій і майбутніх сценаріїв.', 'Event master and future scenario planner'),
        ('Malya', 'Ти Маля — двигун творчості та ідей.', 'Creativity engine and idea generator'),
        ('Gallery', 'Ти Галерея — візуальний архівіст.', 'Visual archivist and media manager'),
        ('Calendar', 'Ті Календар — контролер ритмів і часу.', 'Time rhythm controller and schedule manager')
    """)
    
    # Create memory_entries table with vector column
    op.create_table(
        'memory_entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('embedding', Vector(1536), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_memory_entries_user_id', 'memory_entries', ['user_id'])
    
    # Create vector similarity index
    op.execute('CREATE INDEX idx_memory_entries_embedding ON memory_entries USING ivfflat (embedding vector_cosine_ops)')
    
    # Create system_states table
    op.create_table(
        'system_states',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('persona_id', sa.Integer(), nullable=False),
        sa.Column('mood_score', sa.Integer(), nullable=False),
        sa.Column('energy_level', sa.Float(), nullable=False),
        sa.Column('context_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint('mood_score >= 1 AND mood_score <= 10', name='system_states_mood_score_check'),
        sa.ForeignKeyConstraint(['persona_id'], ['personas.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_system_states_persona_id', 'system_states', ['persona_id'])
    op.create_index('idx_system_states_user_id', 'system_states', ['user_id'])
    
    # Create triggers for updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql'
    """)
    
    op.execute('CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()')
    op.execute('CREATE TRIGGER update_personas_updated_at BEFORE UPDATE ON personas FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()')
    op.execute('CREATE TRIGGER update_memory_entries_updated_at BEFORE UPDATE ON memory_entries FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()')
    op.execute('CREATE TRIGGER update_system_states_updated_at BEFORE UPDATE ON system_states FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()')


def downgrade() -> None:
    # Drop triggers
    op.execute('DROP TRIGGER IF EXISTS update_system_states_updated_at ON system_states')
    op.execute('DROP TRIGGER IF EXISTS update_memory_entries_updated_at ON memory_entries')
    op.execute('DROP TRIGGER IF EXISTS update_personas_updated_at ON personas')
    op.execute('DROP TRIGGER IF EXISTS update_users_updated_at ON users')
    op.execute('DROP FUNCTION IF EXISTS update_updated_at_column()')
    
    # Drop tables
    op.drop_index('idx_system_states_user_id', table_name='system_states')
    op.drop_index('idx_system_states_persona_id', table_name='system_states')
    op.drop_table('system_states')
    
    op.execute('DROP INDEX IF EXISTS idx_memory_entries_embedding')
    op.drop_index('idx_memory_entries_user_id', table_name='memory_entries')
    op.drop_table('memory_entries')
    
    op.drop_index('idx_personas_name', table_name='personas')
    op.drop_table('personas')
    
    op.drop_index('idx_users_username', table_name='users')
    op.drop_index('idx_users_email', table_name='users')
    op.drop_table('users')
    
    # Drop enum type
    op.execute('DROP TYPE IF EXISTS personaenum')
    
    # Note: We don't drop extensions as they might be used by other databases

