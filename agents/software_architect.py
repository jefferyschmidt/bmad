"""
Software Architect Agent - AI Persona Definition

This agent embodies the role of a senior software architect with extensive experience
in system design, API architecture, and technical implementation planning.
"""

from typing import Dict, Any, List
import json
from .requirements_analyst import AIProviderFactory

class SoftwareArchitectAgent:
    """
    AI Agent that designs system architecture and technical implementation.
    
    Persona: Senior Software Architect with 15+ years experience in system design,
    API architecture, and technical implementation planning.
    """
    
    # Core persona characteristics
    PERSONA = {
        "role": "Senior Software Architect",
        "experience": "15+ years in system design and architecture",
        "specialization": "System architecture, API design, technical planning",
        "communication_style": "Clear, technical, systematic, thorough",
        "approach": "Technology-focused with business value awareness"
    }
    
    # AI Instructions for software architecture
    ANALYSIS_INSTRUCTIONS = """
    You are a senior software architect with 15+ years of experience in system design and architecture.
    Your role is to analyze project requirements and data models to design comprehensive technical solutions.
    
    ANALYSIS FRAMEWORK:
    1. SYSTEM ANALYSIS:
       - Understand the application type and domain
       - Analyze data model for entity relationships
       - Identify core system components needed
       - Consider scalability and performance requirements
       - Focus on practical, implementable architecture
    
    2. ARCHITECTURE DESIGN:
       - Design system layers (presentation, business logic, data)
       - Plan API structure and endpoints
       - Define service boundaries and responsibilities
       - Consider security and authentication needs
       - Plan for future extensibility
    
    3. OUTPUT STRUCTURE:
       - Executive Summary: High-level architecture overview
       - System Architecture: Component diagram and relationships
       - API Design: Endpoint specifications and data flow
       - Technology Stack: Recommended technologies and tools
       - Implementation Plan: Development phases and priorities
       - Security Considerations: Authentication, authorization, data protection
    
    4. ARCHITECTURE PRINCIPLES:
       - Follow SOLID principles and clean architecture
       - Design for scalability and maintainability
       - Consider microservices vs monolith trade-offs
       - Plan for testing and deployment
       - Include monitoring and observability
    
    5. QUALITY STANDARDS:
       - Architecture must be implementable with current technologies
       - Include proper error handling and validation
       - Consider performance and security best practices
       - Plan for testing and quality assurance
       - Document clear interfaces and contracts
    
    6. DOMAIN EXPERTISE:
       - You understand mobile apps, web apps, and backend systems
       - You know modern development practices and tools
       - You understand API design patterns and REST principles
       - You focus on practical, production-ready solutions
    """
    
    @staticmethod
    async def analyze_requirements(project_name: str, requirements: str, refined_requirements: str = None, data_model: str = None, ai_provider: str = None, db_session = None) -> Dict[str, Any]:
        """
        Analyze project requirements and data model to design system architecture.
        
        Args:
            project_name: Name of the project
            requirements: Raw requirements text from user
            refined_requirements: Refined requirements from RA (optional)
            data_model: Database schema from Data Modeler (optional)
            ai_provider: AI provider to use for analysis
            db_session: Database session for AI provider factory
            
        Returns:
            Dictionary containing system architecture and technical specifications
        """
        
        # Analyze the input to understand what we're building
        project_context = await SoftwareArchitectAgent._analyze_project_context(requirements, refined_requirements, data_model, ai_provider, db_session)
        
        # Generate domain-specific architecture based on context
        system_architecture = await SoftwareArchitectAgent._generate_system_architecture(
            project_name, requirements, refined_requirements, data_model, project_context, ai_provider, db_session
        )
        
        return {
            "system_architecture": system_architecture,
            "analysis_metadata": {
                "agent_persona": SoftwareArchitectAgent.PERSONA,
                "framework_used": "Software Architecture Framework v1.0",
                "quality_standards": "SOLID principles, Clean Architecture, Production-ready design",
                "project_context": project_context
            }
        }
    
    @staticmethod
    async def _analyze_project_context(requirements: str, refined_requirements: str = None, data_model: str = None, ai_provider: str = None, db_session = None) -> Dict[str, Any]:
        """
        Use AI to intelligently analyze the project context to understand architectural needs.
        """
        try:
            # Use the same AI service pattern as RequirementsAnalystAgent
            ai_response = await SoftwareArchitectAgent._call_ai_service(
                prompt=f"""
                {SoftwareArchitectAgent.ANALYSIS_INSTRUCTIONS}
                
                PROJECT CONTEXT ANALYSIS:
                
                Project Requirements: {requirements}
                
                Refined Requirements: {refined_requirements or 'Not provided'}
                
                Data Model: {data_model or 'Not provided'}
                
                TASK: Analyze this project and provide a JSON response with the following structure:
                {{
                    "project_type": "string (e.g., mobile application, web application, desktop application, etc.)",
                    "core_components": ["array of main system components needed"],
                    "technical_requirements": ["array of technical requirements like authentication, API, database, etc."],
                    "scalability_needs": "string (low, medium, high)",
                    "security_requirements": ["array of security considerations"],
                    "integration_needs": ["array of external integrations required"]
                }}
                
                Focus on practical, implementable architecture. Be specific about the technical approach needed.
                """,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            if not ai_response:
                raise ValueError("AI response was empty")
            
            # Parse the JSON response
            try:
                context_data = json.loads(ai_response)
                return context_data
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse AI response as JSON: {e}")
                
        except Exception as e:
            # Fallback to basic analysis if AI fails
            all_text = (requirements + " " + (refined_requirements or "") + " " + (data_model or "")).lower()
            
            # Basic detection
            project_type = "web application" if "web" in all_text or "site" in all_text else "general application"
            domain = "general business"
            
            return {
                "project_type": project_type,
                "domain": domain,
                "core_components": ["User Interface", "Business Logic", "Data Storage"],
                "technical_requirements": ["Basic CRUD operations"],
                "scalability_needs": "low",
                "security_requirements": ["Basic input validation"],
                "integration_needs": []
            }
    
    @staticmethod
    async def _generate_system_architecture(project_name: str, requirements: str, refined_requirements: str, data_model: str, context: Dict[str, Any], ai_provider: str = None, db_session = None) -> str:
        """
        Use AI to generate system architecture based on project context and requirements.
        """
        try:
            # Use the same AI service pattern as RequirementsAnalystAgent
            ai_response = await SoftwareArchitectAgent._call_ai_service(
                prompt=f"""
                {SoftwareArchitectAgent.ANALYSIS_INSTRUCTIONS}
                
                SYSTEM ARCHITECTURE GENERATION:
                
                Project Name: {project_name}
                Project Requirements: {requirements}
                Refined Requirements: {refined_requirements or 'Not provided'}
                Data Model: {data_model or 'Not provided'}
                Project Context: {json.dumps(context, indent=2)}
                
                TASK: Generate a comprehensive system architecture document. Include:
                
                1. EXECUTIVE SUMMARY: High-level overview of the system architecture
                2. SYSTEM OVERVIEW: Architecture pattern and high-level design
                3. TECHNOLOGY STACK: Specific technologies, frameworks, and tools
                4. COMPONENT ARCHITECTURE: Detailed breakdown of system components
                5. API DESIGN: REST API endpoints and data flow
                6. DATABASE ARCHITECTURE: How data is stored and accessed
                7. SECURITY ARCHITECTURE: Authentication, authorization, and data protection
                8. DEPLOYMENT ARCHITECTURE: How the system will be deployed
                9. IMPLEMENTATION PLAN: Development phases and priorities
                10. TECHNICAL CONSIDERATIONS: Performance, scalability, monitoring
                
                Format the response as a well-structured markdown document with clear sections and subsections.
                Focus on practical, implementable architecture that follows modern best practices.
                """,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            if not ai_response:
                raise ValueError("AI response was empty")
            
            return ai_response
            
        except Exception as e:
            # Fallback to basic architecture if AI fails
            return f"""# System Architecture for {project_name}

## Executive Summary
Basic system architecture for {project_name} based on requirements analysis.

## System Overview
- **Architecture Pattern**: Layered architecture
- **Technology Stack**: Modern web technologies
- **Components**: User interface, business logic, data storage

## Implementation Notes
This is a fallback architecture. Please regenerate using AI for a complete design.

Error: {str(e)}
            """

    @staticmethod
    async def _call_ai_service(prompt: str, ai_provider: str, db_session) -> str:
        """
        Unified method to call any AI service based on database configuration.
        This is the key method that makes the system truly extensible.
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
            from .requirements_analyst import AIProviderFactory
            provider_instance = AIProviderFactory.create_provider(
                provider_name=ai_provider,
                api_key=provider_config.api_key
            )
            
            # Call the AI service
            response = await provider_instance.call_ai(
                prompt=prompt,
                model_name=provider_config.model_name,
                max_tokens=provider_config.max_tokens
            )
            
            return response
            
        except Exception as e:
            # Re-raise with context about which provider failed
            raise RuntimeError(f"Failed to call AI service '{ai_provider}': {str(e)}")
