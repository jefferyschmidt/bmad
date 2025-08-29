"""
Requirements Analyst Agent - AI Persona Definition

This agent embodies the role of a senior business analyst with extensive experience
in software requirements engineering, user story creation, and acceptance criteria definition.
"""

from typing import Dict, Any, List, Protocol
import json
import asyncio
from abc import ABC, abstractmethod

# AI Provider Interface - defines the contract all providers must implement
class AIProviderInterface(Protocol):
    """Protocol defining the interface all AI providers must implement"""
    
    async def call_ai(self, prompt: str, model_name: str, max_tokens: int) -> str:
        """Call the AI service and return the response"""
        ...

# Base class for AI providers
class BaseAIProvider(ABC):
    """Base class for AI providers with common functionality"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    @abstractmethod
    async def call_ai(self, prompt: str, model_name: str, max_tokens: int) -> str:
        """Abstract method that each provider must implement"""
        pass

# Anthropic Provider Implementation
class AnthropicProvider(BaseAIProvider):
    """Anthropic Claude AI provider"""
    
    async def call_ai(self, prompt: str, model_name: str, max_tokens: int) -> str:
        try:
            # Import here to avoid dependency issues if not installed
            from anthropic import Anthropic
            
            client = Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model=model_name,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except ImportError:
            raise RuntimeError("Anthropic client not installed. Run: pip install anthropic")
        except Exception as e:
            raise RuntimeError(f"Anthropic API call failed: {str(e)}")

# OpenAI Provider Implementation
class OpenAIProvider(BaseAIProvider):
    """OpenAI ChatGPT AI provider"""
    
    async def call_ai(self, prompt: str, model_name: str, max_tokens: int) -> str:
        try:
            # Import here to avoid dependency issues if not installed
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=model_name,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except ImportError:
            raise RuntimeError("OpenAI client not installed. Run: pip install openai")
        except Exception as e:
            raise RuntimeError(f"OpenAI API call failed: {str(e)}")

# Provider Factory - dynamically creates provider instances
class AIProviderFactory:
    """Factory for creating AI provider instances based on provider name"""
    
    _providers = {
        'anthropic': AnthropicProvider,
        'openai': OpenAIProvider,
        # Add new providers here - they will be automatically available
        # 'cohere': CohereProvider,
        # 'mistral': MistralProvider,
        # 'gemini': GeminiProvider,
    }
    
    @classmethod
    def create_provider(cls, provider_name: str, api_key: str) -> BaseAIProvider:
        """Create an AI provider instance by name"""
        if provider_name not in cls._providers:
            raise ValueError(f"Unsupported AI provider: {provider_name}. Supported providers: {list(cls._providers.keys())}")
        
        provider_class = cls._providers[provider_name]
        return provider_class(api_key)
    
    @classmethod
    def register_provider(cls, name: str, provider_class: type):
        """Register a new AI provider class"""
        if not issubclass(provider_class, BaseAIProvider):
            raise ValueError(f"Provider class must inherit from BaseAIProvider")
        cls._providers[name] = provider_class

class RequirementsAnalystAgent:
    """
    AI Agent that analyzes project requirements and generates refined specifications.
    
    Persona: Senior Business Analyst with 15+ years experience in software requirements
    engineering, specializing in agile methodologies and user story creation.
    """
    
    # Core persona characteristics
    PERSONA = {
        "role": "Senior Business Analyst",
        "experience": "15+ years in software requirements engineering",
        "specialization": "Agile methodologies, user story creation, acceptance criteria",
        "communication_style": "Clear, professional, systematic, thorough",
        "approach": "Business-value focused with technical awareness"
    }
    
    # AI Instructions for requirements analysis
    ANALYSIS_INSTRUCTIONS = """
    You are a senior business analyst with 15+ years of experience in software requirements engineering.
    Your role is to analyze project requirements and transform them into clear, actionable specifications.
    
    CRITICAL: You must ONLY analyze the requirements provided. Do NOT make assumptions about the domain
    or project type unless explicitly stated in the requirements. If the requirements are vague or insufficient,
    you should ask for clarification rather than inventing details.
    
    ANALYSIS FRAMEWORK:
    1. REQUIREMENTS VALIDATION:
       - First, assess if the provided requirements contain enough information to analyze
       - If requirements are too vague (e.g., "asdf", "test", single words), request clarification
       - Only proceed with analysis if requirements contain meaningful content
    
    2. REQUIREMENTS BREAKDOWN:
       - Identify the CORE PROBLEM being solved based ONLY on the provided requirements
       - Break down vague requirements into specific, actionable features
       - Identify implicit requirements that users don't think to mention
       - Focus on USER VALUE, not technical implementation
       - Consider the actual user's daily workflow and pain points
       - Ask yourself: "What is the intent of what we're building?" based on the actual requirements
    
    3. CLARIFYING QUESTIONS (ASK THESE FIRST):
       - Who is the target user? (age, tech proficiency, lifestyle)
       - What is their current process? (how do they solve this problem now?)
       - What triggers the need? (what pain point are they experiencing?)
       - What would success look like? (what outcome do they want?)
       - What devices do they use? (phone, tablet, desktop, etc.)
       - What's their environment? (home, office, mobile, etc.)
    
    4. OUTPUT STRUCTURE:
       - Executive Summary: Clear problem statement and solution overview based on actual requirements
       - Core Problem: What pain point are we solving (from the requirements)?
       - Functional Requirements: SPECIFIC features based on the requirements, not generic ones
       - User Stories: Detailed user scenarios with acceptance criteria
       - Non-Functional Requirements: Realistic for the actual project scope
       - Assumptions: What we're assuming about the user and project
       - Success Metrics: How we'll know it's working
    
    5. USER STORY CREATION:
       - Focus on the USER'S GOAL, not technical features
       - Make stories specific to the actual domain mentioned in requirements
       - Include realistic acceptance criteria
       - Consider the user's actual needs and constraints
       - Think about edge cases relevant to the specific project
    
    6. QUALITY STANDARDS:
       - Requirements must be SPECIFIC to the user's actual needs
       - Avoid generic business jargon - use domain-appropriate language
       - Focus on solving the actual problem stated, not building generic software
       - Consider the user's technical comfort level
       - Prioritize features that directly solve the stated problem
    
    7. DOMAIN EXPERTISE:
       - You are a generalist business analyst, not a domain expert
       - You analyze requirements objectively without domain bias
       - You ask clarifying questions when requirements are unclear
       - You focus on the business value and user needs
       - You don't assume project type or domain unless specified
    
    8. CUSTOMER EXPERIENCE:
       - You are an expert in customer experience and user interface design. 
       - You find personal pleasure in making every user absolutely delighted with the experience.
       - You understand that simple, focused solutions are better than complex, feature-rich ones.
    
    9. INPUT VALIDATION:
       - Use AI intelligence to determine if requirements are sufficient for analysis
       - If requirements are insufficient, ask for clarification with specific guidance
       - Only proceed with analysis if requirements contain enough information to understand the project
    """
    
    @staticmethod
    async def analyze_requirements(project_name: str, requirements: str, ai_provider: str = "anthropic", db_session=None) -> Dict[str, Any]:
        """
        Analyze project requirements using the AI persona and framework.
        
        Args:
            project_name: Name of the project
            requirements: Raw requirements text from user
            ai_provider: Which AI service to use (from database)
            db_session: Database session to fetch API keys
            
        Returns:
            Dictionary containing refined requirements and user stories
        """
        
        # First, analyze the input to understand what we're building
        project_context = await RequirementsAnalystAgent._analyze_project_context(requirements, ai_provider, db_session)
        
        # Apply the analysis framework to the requirements
        refined_requirements = await RequirementsAnalystAgent._generate_refined_requirements(
            project_name, requirements, project_context, ai_provider, db_session
        )
        
        user_stories = await RequirementsAnalystAgent._generate_user_stories(
            project_name, requirements, project_context, ai_provider, db_session
        )
        
        return {
            "refined_requirements": refined_requirements,
            "user_stories": user_stories,
            "analysis_metadata": {
                "agent_persona": RequirementsAnalystAgent.PERSONA,
                "framework_used": "Requirements Analysis Framework v2.0",
                "quality_standards": "Domain-specific, User-focused, Practical implementation",
                "project_context": project_context,
                "ai_provider_used": ai_provider
            }
        }

    @staticmethod
    async def _analyze_project_context(requirements: str, ai_provider: str, db_session) -> Dict[str, Any]:
        """
        Use AI persona to intelligently analyze the project context.
        The AI should determine project type, domain, and characteristics based on the requirements.
        """
        # First, validate that requirements are sufficient for analysis using AI
        is_sufficient, guidance_questions = await RequirementsAnalystAgent._validate_requirements_ai(requirements, ai_provider, db_session)
        
        if not is_sufficient:
            raise ValueError(
                f"Requirements are insufficient for analysis. Please provide detailed requirements including:\n"
                f"{guidance_questions}\n"
                "You can provide a more detailed response to these questions in the next step."
            )
        
        prompt = f"""
        {RequirementsAnalystAgent.ANALYSIS_INSTRUCTIONS}
        
        Analyze the following project requirements and provide a JSON response with:
        - project_type: What type of project this is (web app, mobile app, desktop software, automation tool, API service, etc.)
        - domain: The business domain or industry this project serves
        - complexity: Simple, moderate, or complex based on the requirements
        - user_type: Who the target users are
        - core_intent: What problem this project is trying to solve
        - key_features: The main features that would be needed (no arbitrary limit - analyze the actual requirements)
        
        Requirements: {requirements}
        
        Respond with only valid JSON, no other text.
        """
        
        response = await RequirementsAnalystAgent._call_ai_service(prompt, ai_provider, db_session)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            raise ValueError(f"AI context analysis did not return valid JSON. Raw response: {response}")
    
    @staticmethod
    async def _validate_requirements_ai(requirements: str, ai_provider: str, db_session) -> tuple[bool, str]:
        """
        Use AI to intelligently validate whether requirements contain sufficient information for analysis.
        Returns a tuple of (is_sufficient, guidance_questions).
        """
        if not requirements or not requirements.strip():
            return False, "Please provide requirements to analyze."
        
        # Use AI to determine if requirements are sufficient
        prompt = f"""
        You are a senior business analyst evaluating whether project requirements are sufficient for analysis.
        
        TASK: Determine if the following requirements contain enough information to begin requirements analysis.
        
        EVALUATION CRITERIA:
        - Requirements should describe a specific problem or need (even if simple)
        - Requirements should indicate who the users are OR allow reasonable inference from context
        - Requirements should suggest what functionality is needed (even if basic)
        - Requirements should have enough detail to understand the project scope (even if it's a simple project)
        
        IMPORTANT: Be reasonable and practical. Simple projects like "a website with pictures" or "a basic calculator app" 
        are perfectly valid and sufficient for analysis. Don't require enterprise-level detail for simple projects.
        
        REQUIREMENTS TO EVALUATE:
        {requirements}
        
        Respond with ONLY a JSON object in this exact format:
        {{
            "sufficient": true/false,
            "reason": "Brief explanation of why requirements are sufficient or insufficient",
            "guidance": "If insufficient, provide 3-5 specific questions to help the user provide better requirements. If sufficient, this can be empty or a brief confirmation."
        }}
        
        For guidance questions, be specific and relevant to what's missing. For example:
        - If missing user context: "Who will be using this system? What is their role or background?"
        - If missing problem context: "What specific problem are you trying to solve? What is the current pain point?"
        - If missing scope: "What is the scope of this project? Is this a small tool or a large system?"
        
        Respond with only valid JSON, no other text.
        """
        
        try:
            response = await RequirementsAnalystAgent._call_ai_service(prompt, ai_provider, db_session)
            validation_result = json.loads(response)
            
            if "sufficient" in validation_result:
                guidance = validation_result.get("guidance", "")
                return validation_result["sufficient"], guidance
            else:
                # If AI response is malformed, default to allowing analysis
                return True, ""
                
        except (json.JSONDecodeError, Exception):
            # If AI validation fails, default to allowing analysis to proceed
            # This prevents blocking legitimate requirements due to AI service issues
            return True, ""
    
    @staticmethod
    def _validate_requirements(requirements: str) -> bool:
        """
        Legacy validation method - kept for backward compatibility but no longer used.
        The AI-based validation in _validate_requirements_ai is now the primary method.
        """
        # This method is deprecated in favor of AI-based validation
        # Keeping it for backward compatibility but it always returns True
        return True

    @staticmethod
    async def _generate_refined_requirements(project_name: str, requirements: str, context: Dict[str, Any], ai_provider: str, db_session) -> str:
        """
        Generate refined requirements using the AI persona and intelligent analysis.
        """
        prompt = f"""
        {RequirementsAnalystAgent.ANALYSIS_INSTRUCTIONS}
        
        Generate refined requirements for the project "{project_name}" based on these requirements:
        {requirements}
        
        Context: {json.dumps(context)}
        
        Generate comprehensive, professional requirements that follow the framework in the instructions.
        Focus on what the user actually needs, not generic boilerplate.
        """
        
        response = await RequirementsAnalystAgent._call_ai_service(prompt, ai_provider, db_session)
        if not response or not response.strip():
            raise ValueError("AI service returned empty response for refined requirements")
        return response

    @staticmethod
    async def _generate_user_stories(project_name: str, requirements: str, context: Dict[str, Any], ai_provider: str, db_session) -> List[Dict[str, Any]]:
        """
        Generate intelligent user stories using the AI persona framework.
        """
        prompt = f"""
        {RequirementsAnalystAgent.ANALYSIS_INSTRUCTIONS}
        
        Generate user stories for the project "{project_name}" based on these requirements:
        {requirements}
        
        Context: {json.dumps(context)}
        
        Generate user stories in JSON format with this structure:
        [
            {{
                "id": "US-001",
                "title": "Story title",
                "description": "As a user, I want... so that...",
                "acceptance_criteria": ["criteria 1", "criteria 2", "criteria 3"],
                "priority": "High/Medium/Low",
                "business_value": "What value this provides",
                "story_points": 1-8
            }}
        ]
        
        Focus on the user's goals and the actual problem being solved.
        Generate as many user stories as needed to cover the requirements - don't limit yourself to an arbitrary number.
        Respond with only valid JSON, no other text.
        """
        
        response = await RequirementsAnalystAgent._call_ai_service(prompt, ai_provider, db_session)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            raise ValueError(f"AI response was not valid JSON: {response}")

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

# Example of how to add a new provider (no code changes needed in the main agent):
# Just add a new row to the ai_providers table and implement the provider class below

"""
# Example: Adding Cohere as a new provider
class CohereProvider(BaseAIProvider):
    async def call_ai(self, prompt: str, model_name: str, max_tokens: int) -> str:
        try:
            import cohere
            co = cohere.Client(self.api_key)
            response = co.generate(
                model=model_name,
                prompt=prompt,
                max_tokens=max_tokens
            )
            return response.generations[0].text
        except ImportError:
            raise RuntimeError("Cohere client not installed. Run: pip install cohere")
        except Exception as e:
            raise RuntimeError(f"Cohere API call failed: {str(e)}")

# Register the new provider
AIProviderFactory.register_provider('cohere', CohereProvider)
"""
