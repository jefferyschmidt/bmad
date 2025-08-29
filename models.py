"""
Database models for BMAD Pipeline
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

class AIProvider(Base):
    __tablename__ = "bmad_ai_providers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)  # anthropic, openai, etc.
    display_name = Column(String(100), nullable=False)  # Anthropic Claude, OpenAI ChatGPT, etc.
    api_key = Column(Text, nullable=False)
    model_name = Column(String(100), nullable=False)  # claude-3-5-sonnet-20241022, gpt-4o, etc.
    max_tokens = Column(Integer, default=4000)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<AIProvider(name='{self.name}', display_name='{self.display_name}')>"

class Project(Base):
    __tablename__ = "bmad_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    requirements = Column(Text, nullable=False)
    refined_requirements = Column(Text, nullable=True)
    user_stories = Column(Text, nullable=True)
    data_model = Column(Text, nullable=True)
    system_architecture = Column(Text, nullable=True)
    status = Column(String(50), default="draft", index=True)
    archived = Column(Boolean, default=False, index=True)
    ai_provider = Column(String(50), default="anthropic", nullable=False)  # anthropic, openai
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Project(name='{self.name}', status='{self.status}')>"
