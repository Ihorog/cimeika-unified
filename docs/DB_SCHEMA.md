# DB_SCHEMA — Cimeika PostgreSQL Schema

## Extensions

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;  -- pgvector for embeddings
```

## Core Tables

### users
| Column     | Type      | Notes                  |
|------------|-----------|------------------------|
| id         | UUID PK   | uuid_generate_v4()     |
| username   | VARCHAR   | UNIQUE NOT NULL        |
| email      | VARCHAR   | UNIQUE NOT NULL        |
| created_at | TIMESTAMPTZ | default NOW()        |
| updated_at | TIMESTAMPTZ | auto-updated trigger |

### personas
| Column      | Type          | Notes                         |
|-------------|---------------|-------------------------------|
| id          | SERIAL PK     |                               |
| name        | persona_type  | UNIQUE (enum: Ci..Calendar)   |
| base_prompt | TEXT          | System prompt for this persona|
| description | TEXT          |                               |

### memory_entries
| Column    | Type          | Notes                         |
|-----------|---------------|-------------------------------|
| id        | SERIAL PK     |                               |
| user_id   | UUID FK→users |                               |
| content   | TEXT          |                               |
| embedding | vector(1536)  | OpenAI ada-002, ivfflat index |
| metadata  | JSONB         |                               |

### system_states
| Column       | Type            | Notes                 |
|--------------|-----------------|-----------------------|
| id           | SERIAL PK       |                       |
| user_id      | UUID FK→users   |                       |
| persona_id   | INT FK→personas |                       |
| mood_score   | INT             | 1–10                  |
| energy_level | FLOAT           |                       |
| context_data | JSONB           |                       |

## Module Tables (managed by SQLAlchemy ORM)

### podija_events
| Column          | Type       | Notes                          |
|-----------------|------------|--------------------------------|
| id              | SERIAL PK  |                                |
| module          | VARCHAR    | default 'podija'               |
| time            | TIMESTAMP  | record creation time           |
| title           | VARCHAR    | NOT NULL                       |
| description     | TEXT       |                                |
| event_date      | TIMESTAMP  | scheduled time                 |
| event_type      | VARCHAR    | past/future/planned/scenario   |
| status          | VARCHAR    | planned / done / cancelled     |
| is_completed    | BOOLEAN    |                                |
| participants    | JSONB      |                                |
| location        | VARCHAR    |                                |
| tags            | JSONB      |                                |
| source_trace    | VARCHAR    |                                |
| canon_bundle_id | VARCHAR    | 'cimeika-v1'                   |

Indexes: `event_date`, `status`

### calendar_entries
| Column             | Type       | Notes                                    |
|--------------------|------------|------------------------------------------|
| id                 | SERIAL PK  |                                          |
| module             | VARCHAR    | default 'calendar'                       |
| time               | TIMESTAMP  |                                          |
| title              | VARCHAR    | NOT NULL                                 |
| scheduled_at       | TIMESTAMP  | NOT NULL                                 |
| end_time           | TIMESTAMP  |                                          |
| entry_type         | VARCHAR    | event/reminder/routine/rhythm            |
| is_recurring       | BOOLEAN    |                                          |
| recurrence_pattern | JSONB      |                                          |
| location           | VARCHAR    |                                          |
| participants       | JSONB      |                                          |
| reminder_settings  | JSONB      |                                          |
| **external_id**    | VARCHAR    | **google_event_id stored ONLY here**     |
| tags               | JSONB      |                                          |
| canon_bundle_id    | VARCHAR    |                                          |

Indexes: `scheduled_at`, UNIQUE `external_id` (where not null)

### gallery_items
| Column          | Type      | Notes                   |
|-----------------|-----------|-------------------------|
| id              | SERIAL PK |                         |
| module          | VARCHAR   | default 'gallery'       |
| title           | VARCHAR   | NOT NULL                |
| media_type      | VARCHAR   | image/video/audio/doc   |
| url             | TEXT      | NOT NULL                |
| thumbnail_url   | TEXT      |                         |
| file_size       | INTEGER   | bytes                   |
| mime_type       | VARCHAR   |                         |
| media_metadata  | JSONB     |                         |
| tags            | JSONB     |                         |
| canon_bundle_id | VARCHAR   |                         |

### ci_signals
| Column        | Type      | Notes                                  |
|---------------|-----------|----------------------------------------|
| id            | SERIAL PK |                                        |
| signal_type   | VARCHAR   | reminder_due/event_created/sync_request|
| source_module | VARCHAR   | emitting module                        |
| target_module | VARCHAR   | receiving module (nullable=broadcast)  |
| payload       | JSONB     |                                        |
| status        | VARCHAR   | pending / processed / failed           |
| processed_at  | TIMESTAMP |                                        |
| created_at    | TIMESTAMP |                                        |

Indexes: `signal_type`, `status`, `created_at`

### reminder_jobs
| Column         | Type      | Notes                              |
|----------------|-----------|------------------------------------|
| id             | SERIAL PK |                                    |
| entity_type    | VARCHAR   | podija_event / calendar_entry      |
| entity_id      | INTEGER   |                                    |
| remind_at      | TIMESTAMP | exact UTC fire time (event_date−N) |
| offset_minutes | INTEGER   | default 10 (T-10m)                 |
| channel        | VARCHAR   | telegram / web / both              |
| status         | VARCHAR   | pending / sent / failed / cancelled|
| sent_at        | TIMESTAMP |                                    |
| payload        | JSONB     |                                    |
| created_at     | TIMESTAMP |                                    |

Indexes: `remind_at`, `status`, `(entity_type, entity_id)`

## Other Module Tables

Each remaining module (ci_entities, kazkar_stories, nastrij_emotions, malya_ideas) follows the same pattern: `id, module, time, <module-fields>, tags, source_trace, canon_bundle_id`.

See `backend/app/modules/<module>/model.py` for the authoritative ORM definition.
