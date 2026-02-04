-- CIMEIKA Database Schema
-- PostgreSQL with pgvector extension for vector embeddings
-- Implements 7 personas architecture

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- Create persona type enum
CREATE TYPE persona_type AS ENUM (
    'Ci',
    'Kazkar',
    'Nastrij',
    'Podija',
    'Malya',
    'Gallery',
    'Calendar'
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- Personas table
CREATE TABLE IF NOT EXISTS personas (
    id SERIAL PRIMARY KEY,
    name persona_type UNIQUE NOT NULL,
    base_prompt TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_personas_name ON personas(name);

-- Memory entries table with vector embeddings
CREATE TABLE IF NOT EXISTS memory_entries (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI ada-002 embedding dimension
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_memory_entries_user_id ON memory_entries(user_id);
-- Create vector similarity index for fast nearest neighbor search
CREATE INDEX idx_memory_entries_embedding ON memory_entries USING ivfflat (embedding vector_cosine_ops);

-- System states table
CREATE TABLE IF NOT EXISTS system_states (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    persona_id INTEGER NOT NULL REFERENCES personas(id) ON DELETE CASCADE,
    mood_score INTEGER NOT NULL CHECK (mood_score >= 1 AND mood_score <= 10),
    energy_level FLOAT NOT NULL,
    context_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_system_states_user_id ON system_states(user_id);
CREATE INDEX idx_system_states_persona_id ON system_states(persona_id);

-- Seed data for 7 personas
INSERT INTO personas (name, base_prompt, description) VALUES
    ('Ci', 'Ти Ці — центральний координатор екосистеми Cimeika.', 'Central orchestration and coordination module'),
    ('Kazkar', 'Ти Казкар — хранитель спогадів і історій.', 'Memory and story keeper, guardian of legends'),
    ('Nastrij', 'Ти Настрій — емоційний аналітик.', 'Emotional state analyzer and mood tracker'),
    ('Podija', 'Ти Подія — майстер подій і майбутніх сценаріїв.', 'Event master and future scenario planner'),
    ('Malya', 'Ти Маля — двигун творчості та ідей.', 'Creativity engine and idea generator'),
    ('Gallery', 'Ти Галерея — візуальний архівіст.', 'Visual archivist and media manager'),
    ('Calendar', 'Ті Календар — контролер ритмів і часу.', 'Time rhythm controller and schedule manager')
ON CONFLICT (name) DO NOTHING;

-- Create function for automatic updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_personas_updated_at BEFORE UPDATE ON personas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_memory_entries_updated_at BEFORE UPDATE ON memory_entries
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_system_states_updated_at BEFORE UPDATE ON system_states
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
