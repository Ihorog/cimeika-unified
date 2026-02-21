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

-- ============================================================
-- Core module tables (SQLAlchemy manages these via ORM)
-- ============================================================

-- podija_events: PoDiya MVP — events, scenarios
CREATE TABLE IF NOT EXISTS podija_events (
    id SERIAL PRIMARY KEY,
    module VARCHAR(64) NOT NULL DEFAULT 'podija',
    time TIMESTAMP NOT NULL DEFAULT NOW(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    event_date TIMESTAMP,
    event_type VARCHAR(64),
    status VARCHAR(32) NOT NULL DEFAULT 'planned',  -- planned, done, cancelled
    is_completed BOOLEAN DEFAULT FALSE,
    participants JSONB,
    location VARCHAR(255),
    tags JSONB DEFAULT '[]',
    source_trace VARCHAR(255),
    canon_bundle_id VARCHAR(128) NOT NULL DEFAULT 'cimeika-v1'
);

CREATE INDEX IF NOT EXISTS idx_podija_events_event_date ON podija_events(event_date);
CREATE INDEX IF NOT EXISTS idx_podija_events_status ON podija_events(status);

-- calendar_entries: Calendar library with external sync support
CREATE TABLE IF NOT EXISTS calendar_entries (
    id SERIAL PRIMARY KEY,
    module VARCHAR(64) NOT NULL DEFAULT 'calendar',
    time TIMESTAMP NOT NULL DEFAULT NOW(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    scheduled_at TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    entry_type VARCHAR(64),
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_pattern JSONB,
    location VARCHAR(255),
    participants JSONB,
    reminder_settings JSONB,
    external_id VARCHAR(255),  -- google_event_id stored ONLY here
    tags JSONB DEFAULT '[]',
    source_trace VARCHAR(255),
    canon_bundle_id VARCHAR(128) NOT NULL DEFAULT 'cimeika-v1'
);

CREATE INDEX IF NOT EXISTS idx_calendar_entries_scheduled_at ON calendar_entries(scheduled_at);
CREATE UNIQUE INDEX IF NOT EXISTS idx_calendar_entries_external_id ON calendar_entries(external_id)
    WHERE external_id IS NOT NULL;

-- gallery_items: Gallery library
CREATE TABLE IF NOT EXISTS gallery_items (
    id SERIAL PRIMARY KEY,
    module VARCHAR(64) NOT NULL DEFAULT 'gallery',
    time TIMESTAMP NOT NULL DEFAULT NOW(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    media_type VARCHAR(64) NOT NULL,
    url TEXT NOT NULL,
    thumbnail_url TEXT,
    file_size INTEGER,
    mime_type VARCHAR(128),
    media_metadata JSONB,
    tags JSONB DEFAULT '[]',
    source_trace VARCHAR(255),
    canon_bundle_id VARCHAR(128) NOT NULL DEFAULT 'cimeika-v1'
);

-- ci_signals: Ci orchestration bus signals
CREATE TABLE IF NOT EXISTS ci_signals (
    id SERIAL PRIMARY KEY,
    signal_type VARCHAR(64) NOT NULL,   -- e.g. reminder_due, event_created, sync_request
    source_module VARCHAR(64) NOT NULL,
    target_module VARCHAR(64),
    payload JSONB DEFAULT '{}',
    status VARCHAR(32) NOT NULL DEFAULT 'pending',  -- pending, processed, failed
    processed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ci_signals_signal_type ON ci_signals(signal_type);
CREATE INDEX IF NOT EXISTS idx_ci_signals_status ON ci_signals(status);
CREATE INDEX IF NOT EXISTS idx_ci_signals_created_at ON ci_signals(created_at);

-- reminder_jobs: Scheduled reminder delivery (T-10m and custom offsets)
CREATE TABLE IF NOT EXISTS reminder_jobs (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(64) NOT NULL,   -- podija_event, calendar_entry
    entity_id INTEGER NOT NULL,
    remind_at TIMESTAMP NOT NULL,       -- exact UTC time to fire
    offset_minutes INTEGER NOT NULL DEFAULT 10,
    channel VARCHAR(32) NOT NULL DEFAULT 'telegram',  -- telegram, web, both
    status VARCHAR(32) NOT NULL DEFAULT 'pending',    -- pending, sent, failed, cancelled
    sent_at TIMESTAMP,
    payload JSONB DEFAULT '{}',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reminder_jobs_remind_at ON reminder_jobs(remind_at);
CREATE INDEX IF NOT EXISTS idx_reminder_jobs_status ON reminder_jobs(status);
CREATE INDEX IF NOT EXISTS idx_reminder_jobs_entity ON reminder_jobs(entity_type, entity_id);
