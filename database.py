"""
Database configuration and connection for BMAD Pipeline
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, text

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://musiclive:npg_wopeP92YbXft@ep-curly-hat-ad4vut3o-pooler.c-2.us-east-1.aws.neon.tech/musiclive"
)

# Convert to async URL for asyncpg
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    pool_size=10,
    max_overflow=20,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Metadata with table naming convention
metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)

# Dependency to get database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Initialize database tables
async def init_db():
    # First create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Then check and add archived column in a separate transaction
    async with engine.begin() as conn:
        try:
            # Check if archived column exists
            result = await conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'bmad_projects' AND column_name = 'archived'"))
            if not result.fetchone():
                # Column doesn't exist, add it
                await conn.execute(text("ALTER TABLE bmad_projects ADD COLUMN archived BOOLEAN DEFAULT FALSE"))
                await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_bmad_projects_archived ON bmad_projects(archived)"))
                print("Added archived column to bmad_projects table")
            else:
                print("Archived column already exists")
        except Exception as e:
            print(f"Error checking/adding archived column: {e}")
            # Continue anyway, the column might already exist
    
    # Check and add ux_design column in a separate transaction
    async with engine.begin() as conn:
        try:
            # Check if ux_design column exists
            result = await conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'bmad_projects' AND column_name = 'ux_design'"))
            if not result.fetchone():
                # Column doesn't exist, add it
                await conn.execute(text("ALTER TABLE bmad_projects ADD COLUMN ux_design TEXT"))
                print("Added ux_design column to bmad_projects table")
            else:
                print("UX design column already exists")
        except Exception as e:
            print(f"Error checking/adding ux_design column: {e}")
            # Continue anyway, the column might already exist
    
    # Check and add system_architecture column in a separate transaction
    async with engine.begin() as conn:
        try:
            # Check if system_architecture column exists
            result = await conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'bmad_projects' AND column_name = 'system_architecture'"))
            if not result.fetchone():
                # Column doesn't exist, add it
                await conn.execute(text("ALTER TABLE bmad_projects ADD COLUMN system_architecture TEXT"))
                print("Added system_architecture column to bmad_projects table")
            else:
                print("System architecture column already exists")
        except Exception as e:
            print(f"Error checking/adding system_architecture column: {e}")
            # Continue anyway, the column might already exist
    
    # Check and add ai_provider column in a separate transaction
    async with engine.begin() as conn:
        try:
            # Check if ai_provider column exists
            result = await conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'bmad_projects' AND column_name = 'ai_provider'"))
            if not result.fetchone():
                # Column doesn't exist, add it
                await conn.execute(text("ALTER TABLE bmad_projects ADD COLUMN ai_provider VARCHAR(50) DEFAULT 'anthropic'"))
                print("Added ai_provider column to bmad_projects table")
            else:
                print("AI provider column already exists")
        except Exception as e:
            print(f"Error checking/adding ai_provider column: {e}")
            # Continue anyway, the column might already exist
    
    # Check and add tech_stack column in a separate transaction
    async with engine.begin() as conn:
        try:
            # Check if tech_stack column exists
            result = await conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'bmad_projects' AND column_name = 'tech_stack'"))
            if not result.fetchone():
                # Column doesn't exist, add it
                await conn.execute(text("ALTER TABLE bmad_projects ADD COLUMN tech_stack TEXT"))
                print("Added tech_stack column to bmad_projects table")
            else:
                print("Tech stack column already exists")
        except Exception as e:
            print(f"Error checking/adding tech_stack column: {e}")
            # Continue anyway, the column might already exist
    
    # Create ai_providers table if it doesn't exist
    async with engine.begin() as conn:
        try:
            # Check if ai_providers table exists
            result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_name = 'bmad_ai_providers'"))
            if not result.fetchone():
                # Table doesn't exist, create it
                await conn.execute(text("""
                    CREATE TABLE bmad_ai_providers (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) UNIQUE NOT NULL,
                        display_name VARCHAR(100) NOT NULL,
                        api_key TEXT NOT NULL,
                        model_name VARCHAR(100) NOT NULL,
                        max_tokens INTEGER DEFAULT 4000,
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                print("Created bmad_ai_providers table")
                
                # Insert default AI providers with placeholder API keys
                await conn.execute(text("""
                    INSERT INTO bmad_ai_providers (name, display_name, api_key, model_name, max_tokens, is_active)
                    VALUES 
                    ('anthropic', 'Anthropic Claude', 'YOUR_ANTHROPIC_API_KEY_HERE', 'claude-3-haiku-20240307', 4000, TRUE),
                    ('openai', 'OpenAI ChatGPT', 'YOUR_OPENAI_API_KEY_HERE', 'gpt-4o', 4000, TRUE)
                """))
                print("Inserted default AI providers")
            else:
                print("AI providers table already exists")
        except Exception as e:
            print(f"Error creating ai_providers table: {e}")
            # Continue anyway, the table might already exist
