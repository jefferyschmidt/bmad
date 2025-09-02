"""
UX/UI Designer Agent for BMAD Pipeline
"""

import json
from typing import Dict, Any
from .requirements_analyst import AIProviderFactory


class UXDesignerAgent:
    """Agent responsible for generating UX/UI design specifications"""
    
    PERSONA = """
    You are a senior UX/UI Designer with 15+ years of experience creating intuitive, 
    accessible, and beautiful user interfaces. You specialize in:
    
    - User Experience (UX) design principles and best practices
    - User Interface (UI) design patterns and components
    - Accessibility standards (WCAG 2.1 AA compliance)
    - Responsive design for multiple device types
    - User research and persona development
    - Information architecture and navigation design
    - Visual design systems and design tokens
    - Prototyping and user testing methodologies
    
    You create comprehensive design specifications that developers can implement directly.
    You focus on user-centered design that solves real problems and creates delightful experiences.
    """
    
    DESIGN_INSTRUCTIONS = """
    Analyze the project requirements and system architecture to create comprehensive UX/UI design specifications.
    
    Your design should include:
    
    1. **User Personas & Journey Maps**
       - Primary and secondary user personas
       - Key user journeys and workflows
       - Pain points and opportunities
    
    2. **Information Architecture**
       - Site/app structure and navigation
       - Content organization and hierarchy
       - User flow diagrams
    
    3. **UI Design System**
       - Color palette and typography
       - Component library (buttons, forms, cards, etc.)
       - Layout grids and spacing
       - Responsive breakpoints
    
    4. **Key Screens/Pages**
       - Wireframes for main user flows
       - Detailed mockups for critical interfaces
       - Mobile and desktop considerations
    
    5. **Interaction Design**
       - Micro-interactions and animations
       - Form validation and feedback
       - Loading states and error handling
    
    6. **Accessibility Guidelines**
       - Keyboard navigation
       - Screen reader support
       - Color contrast requirements
       - Focus management
    
    7. **Implementation Notes**
       - Design tokens and CSS variables
       - Component specifications
       - Animation timing and easing
       - Responsive behavior rules
    
    Focus on creating a design that is:
    - Intuitive and easy to use
    - Accessible to all users
    - Scalable and maintainable
    - Aligned with modern design trends
    - Optimized for the target platform(s)
    """
    
    @staticmethod
    async def analyze_requirements(
        project_name: str,
        requirements: str,
        refined_requirements: str,
        system_architecture: str,
        application_type: str,
        ai_provider: str,
        db_session
    ) -> Dict[str, Any]:
        """
        Generate comprehensive UX/UI design specifications
        
        Args:
            project_name: Name of the project
            requirements: Original user requirements
            refined_requirements: Analyzed and refined requirements
            system_architecture: System architecture specifications
            application_type: Type of application (static_website, web_application, mobile_app, etc.)
            ai_provider: AI provider to use (anthropic, openai)
            db_session: Database session for AI provider config
            
        Returns:
            Dict containing ux_design and analysis_metadata
        """
        try:
            print(f"Starting UX/UI design generation for project: {project_name}")
            
            # Get AI provider configuration
            ai_service = await UXDesignerAgent._call_ai_service(
                prompt=f"""
                {UXDesignerAgent.PERSONA}
                
                {UXDesignerAgent.DESIGN_INSTRUCTIONS}
                
                PROJECT: {project_name}
                ORIGINAL REQUIREMENTS: {requirements}
                REFINED REQUIREMENTS: {refined_requirements}
                SYSTEM ARCHITECTURE: {system_architecture}
                APPLICATION TYPE: {application_type or 'Not specified'}
                
                TASK: Create comprehensive UX/UI design specifications for this project.
                
                Return your response as a structured design document that covers all the key areas:
                - User personas and journey maps
                - Information architecture
                - UI design system
                - Key screens/pages
                - Interaction design
                - Accessibility guidelines
                - Implementation notes
                
                IMPORTANT: Consider the application type when creating the design:
                - Static Website: Focus on content presentation, navigation, and visual hierarchy
                - Web Application: Emphasize user workflows, data visualization, and interactive elements
                - Mobile App: Consider touch interactions, mobile navigation patterns, and device-specific features
                - Automation Script: Focus on command-line interfaces, progress indicators, and error handling
                - Desktop Application: Consider desktop UI patterns, window management, and platform integration
                
                Be specific and actionable. Developers should be able to implement your design directly.
                Focus on creating an excellent user experience that aligns with the project requirements.
                """,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            if not ai_service["success"]:
                raise Exception(f"AI service call failed: {ai_service['error']}")
            
            design_spec = ai_service["response"]
            
            return {
                "success": True,
                "ux_design": design_spec,
                "analysis_metadata": {
                    "agent": "UXDesignerAgent",
                    "ai_provider": ai_provider,
                    "design_scope": "comprehensive_ux_ui",
                    "generation_timestamp": "2024-01-01T00:00:00Z"
                }
            }
            
        except Exception as e:
            print(f"UX/UI design generation error: {e}")
            return {
                "success": False,
                "error": f"UX/UI design generation failed: {str(e)}"
            }
    
    @staticmethod
    async def _call_ai_service(
        prompt: str,
        ai_provider: str,
        db_session
    ) -> Dict[str, Any]:
        """
        Call the appropriate AI service based on provider configuration
        
        Args:
            prompt: The prompt to send to the AI
            ai_provider: AI provider name (anthropic, openai)
            db_session: Database session for configuration
            
        Returns:
            Dict containing success status and response or error
        """
        try:
            # Get AI provider configuration from database
            from sqlalchemy import text
            result = await db_session.execute(
                text("SELECT api_key, model_name, max_tokens FROM bmad_ai_providers WHERE name = :name AND is_active = true"),
                {"name": ai_provider}
            )
            provider_config = result.fetchone()
            
            if not provider_config:
                raise Exception(f"AI provider '{ai_provider}' not found or inactive")
            
            api_key = provider_config[0]
            model_name = provider_config[1]
            max_tokens = provider_config[2]
            
            # Create AI provider instance
            provider = AIProviderFactory.create_provider(
                provider_name=ai_provider,
                api_key=api_key
            )
            
            # Call AI service
            response = await provider.call_ai(prompt, model_name, max_tokens)
            
            return {
                "success": True,
                "response": response
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"AI service call failed: {str(e)}"
            }
