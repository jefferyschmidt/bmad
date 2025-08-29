"""
Data Modeler Agent - AI Persona Definition

This agent embodies the role of a senior data architect with extensive experience
in database design, data modeling, and schema optimization.
"""

from typing import Dict, Any, List
import json
from .requirements_analyst import AIProviderFactory

class DataModelerAgent:
    """
    AI Agent that analyzes project requirements and generates database schemas.
    
    Persona: Senior Data Architect with 15+ years experience in database design,
    data modeling, and schema optimization for various application types.
    """
    
    # Core persona characteristics
    PERSONA = {
        "role": "Senior Data Architect",
        "experience": "15+ years in database design and data modeling",
        "specialization": "Database schema design, normalization, performance optimization",
        "communication_style": "Clear, technical, systematic, thorough",
        "approach": "Data-focused with business value awareness"
    }
    
    # AI Instructions for data modeling
    ANALYSIS_INSTRUCTIONS = """
    You are a senior data architect with 15+ years of experience in database design and data modeling.
    Your role is to analyze project requirements and transform them into clear, actionable database schemas.
    
    ANALYSIS FRAMEWORK:
    1. REQUIREMENTS ANALYSIS:
       - Identify the core entities from the requirements
       - Understand the relationships between entities
       - Identify data attributes and their types
       - Consider data volume and access patterns
       - Focus on the actual data needs, not generic patterns
    
    2. DOMAIN UNDERSTANDING:
       - Understand the specific domain and business context
       - Identify domain-specific data requirements
       - Consider real-world data scenarios
       - Think about data lifecycle and retention
    
    3. OUTPUT STRUCTURE:
       - Executive Summary: High-level data architecture overview
       - Core Entities: Main data objects with descriptions
       - Database Schema: Detailed table definitions with columns
       - Relationships: How entities connect to each other
       - Data Types: Appropriate field types and constraints
       - Indexes: Performance optimization recommendations
       - Sample Data: Example records to illustrate the schema
    
    4. SCHEMA DESIGN PRINCIPLES:
       - Follow normalization principles (3NF)
       - Design for performance and scalability
       - Consider future extensibility
       - Include proper foreign key relationships
       - Add appropriate constraints and validation
    
    5. QUALITY STANDARDS:
       - Schemas must be implementable in PostgreSQL
       - Include proper data types and constraints
       - Consider data integrity and referential integrity
       - Optimize for common query patterns
       - Include audit fields (created_at, updated_at) where appropriate
    
    6. DOMAIN EXPERTISE:
       - You understand various application types and domains
       - You know how to design schemas for user management, scheduling, and history tracking
       - You understand notification and reminder systems
       - You focus on practical, implementable designs
    """
    
    @staticmethod
    async def analyze_requirements(project_name: str, requirements: str, refined_requirements: str = None, ai_provider: str = "anthropic", db_session=None) -> Dict[str, Any]:
        """
        Analyze project requirements and generate database schema using AI.
        
        Args:
            project_name: Name of the project
            requirements: Raw requirements text from user
            refined_requirements: Refined requirements from RA (optional)
            ai_provider: AI provider to use (anthropic, openai, etc.)
            db_session: Database session for AI provider configuration
            
        Returns:
            Dictionary containing database schema and metadata
        """
        
        # Analyze the input to understand what we're building
        project_context = await DataModelerAgent._analyze_project_context(requirements, refined_requirements, ai_provider, db_session)
        
        # Generate domain-specific schema based on context
        database_schema = await DataModelerAgent._generate_database_schema(
            project_name, requirements, refined_requirements, project_context, ai_provider, db_session
        )
        
        return {
            "database_schema": database_schema,
            "analysis_metadata": {
                "agent_persona": DataModelerAgent.PERSONA,
                "framework_used": "AI-Powered Data Modeling Framework v2.0",
                "quality_standards": "3NF normalization, PostgreSQL optimization, Performance-focused",
                "project_context": project_context
            }
        }
    
    @staticmethod
    async def _analyze_project_context(requirements: str, refined_requirements: str = None, ai_provider: str = "anthropic", db_session=None) -> Dict[str, Any]:
        """
        Use AI to intelligently analyze the project context and understand data modeling needs.
        """
        try:
            # Fetch AI provider configuration from database
            from models import AIProvider
            from sqlalchemy import select
            
            stmt = select(AIProvider).where(AIProvider.name == ai_provider, AIProvider.is_active == True)
            result = await db_session.execute(stmt)
            provider_config = result.scalar_one_or_none()
            
            if not provider_config:
                raise ValueError(f"AI provider '{ai_provider}' not found or inactive in database")
            
            # Create the appropriate provider instance using the factory
            provider_instance = AIProviderFactory.create_provider(
                provider_name=ai_provider,
                api_key=provider_config.api_key
            )
            
            # Create prompt for context analysis
            prompt = f"""
            {DataModelerAgent.ANALYSIS_INSTRUCTIONS}
            
            TASK: Analyze the following project requirements and provide a JSON response with:
            
            - project_type: The type of application (mobile app, web app, desktop software, etc.)
            - domain: The business domain (e.g., social media, e-commerce, project management, etc.)
            - core_entities: List of main data objects/entities that need to be stored
            - data_patterns: Key data patterns (user management, content sharing, e-commerce, etc.)
            - complexity_level: Simple, moderate, or complex based on requirements scope
            - technical_considerations: Any specific technical requirements or constraints
            
            PROJECT REQUIREMENTS:
            {requirements}
            
            {f"REFINED REQUIREMENTS: {refined_requirements}" if refined_requirements else ""}
            
            Provide ONLY a valid JSON response with no additional text or explanation.
            """
            
            # Get AI response
            response = await provider_instance.call_ai(
                prompt=prompt,
                model_name=provider_config.model_name,
                max_tokens=2000
            )
            
            # Parse JSON response
            try:
                context = json.loads(response)
                return context
            except json.JSONDecodeError:
                raise ValueError(f"Failed to parse AI response as JSON: {response}")
                
        except Exception as e:
            raise ValueError(f"Failed to analyze project context: {str(e)}")
    
    @staticmethod
    async def _generate_database_schema(project_name: str, requirements: str, refined_requirements: str, context: Dict[str, Any], ai_provider: str = "anthropic", db_session=None) -> str:
        """
        Use AI to generate database schema based on project context and requirements.
        """
        try:
            # Fetch AI provider configuration from database
            from models import AIProvider
            from sqlalchemy import select
            
            stmt = select(AIProvider).where(AIProvider.name == ai_provider, AIProvider.is_active == True)
            result = await db_session.execute(stmt)
            provider_config = result.scalar_one_or_none()
            
            if not provider_config:
                raise ValueError(f"AI provider '{ai_provider}' not found or inactive in database")
            
            # Create the appropriate provider instance using the factory
            provider_instance = AIProviderFactory.create_provider(
                provider_name=ai_provider,
                api_key=provider_config.api_key
            )
            
            # Create prompt for schema generation
            prompt = f"""
            {DataModelerAgent.ANALYSIS_INSTRUCTIONS}
            
            TASK: Generate a comprehensive database schema for the project based on the context analysis.
            
            PROJECT NAME: {project_name}
            PROJECT REQUIREMENTS: {requirements}
            {f"REFINED REQUIREMENTS: {refined_requirements}" if refined_requirements else ""}
            
            PROJECT CONTEXT: {json.dumps(context, indent=2)}
            
            REQUIREMENTS:
            1. Generate a complete PostgreSQL database schema
            2. Include all necessary tables with proper columns, data types, and constraints
            3. Define foreign key relationships between tables
            4. Add appropriate indexes for performance
            5. Include audit fields (created_at, updated_at) where appropriate
            6. Consider data integrity and referential integrity
            7. Optimize for common query patterns
            8. Make the schema implementable and production-ready
            
            OUTPUT FORMAT:
            - Executive Summary: High-level overview of the data architecture
            - Core Entities: Description of main data objects
            - Database Schema: Complete SQL CREATE TABLE statements
            - Relationships: Explanation of table relationships
            - Indexes: Performance optimization recommendations
            - Sample Data: Example records to illustrate the schema
            
            Provide a comprehensive, well-structured response that can be directly implemented.
            """
            
            # Get AI response
            response = await provider_instance.call_ai(
                prompt=prompt,
                model_name=provider_config.model_name,
                max_tokens=4000
            )
            
            if not response or response.strip() == "":
                raise ValueError("AI response was empty")
                
            return response
                
        except Exception as e:
            raise ValueError(f"Failed to generate database schema: {str(e)}")
