"""
Full Stack Developer Agent - AI-Powered Code Generation

This agent generates working software based on project requirements and architecture.
"""

from typing import Dict, Any, List
import json
from pathlib import Path

class FullStackDeveloperAgent:
    """
    AI Agent that generates working software based on project requirements and architecture.
    """
    
    @staticmethod
    async def generate_project(
        project_name: str,
        requirements: str,
        refined_requirements: str,
        system_architecture: str,
        ux_design: str,
        ai_provider: str,
        db_session,
        project_id: int
    ) -> Dict[str, Any]:
        """
        Generate a complete, working software project based on requirements and architecture.
        """
        try:
            # Step 1: Generate data model based on requirements and architecture
            data_model = await FullStackDeveloperAgent._generate_data_model(
                project_name, requirements, refined_requirements, system_architecture,
                ai_provider, db_session
            )
            
            # Step 2: Analyze requirements and determine optimal tech stack
            tech_stack_analysis = await FullStackDeveloperAgent._analyze_tech_stack(
                project_name, requirements, refined_requirements, data_model, system_architecture,
                ai_provider, db_session
            )
            
            # Step 2: Generate project structure and code
            project_path = await FullStackDeveloperAgent._generate_project_structure(
                project_id, project_name, tech_stack_analysis
            )
            
            # Step 3: Generate the actual code based on tech stack
            code_generation_result = await FullStackDeveloperAgent._generate_code(
                project_name, requirements, refined_requirements, data_model, 
                system_architecture, ux_design, tech_stack_analysis, project_path, ai_provider, db_session
            )
            
            # Step 4: Generate documentation and setup instructions
            docs_result = await FullStackDeveloperAgent._generate_documentation(
                project_name, tech_stack_analysis, project_path, ai_provider, db_session
            )
            
            return {
                "success": True,
                "project_path": str(project_path),
                "tech_stack": tech_stack_analysis,
                "code_generation": code_generation_result,
                "documentation": docs_result,
                "message": f"Project '{project_name}' generated successfully at {project_path}"
            }
            
        except Exception as e:
            print(f"Error in generate_project: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": f"Failed to generate project: {str(e)}",
                "project_path": None
            }
    
    @staticmethod
    async def _analyze_tech_stack(
        project_name: str,
        requirements: str,
        refined_requirements: str,
        data_model: str,
        system_architecture: str,
        ai_provider: str,
        db_session
    ) -> Dict[str, Any]:
        """
        Use AI to analyze requirements and determine the optimal tech stack.
        """
        try:
            # Use the same AI service pattern as other agents
            ai_response = await FullStackDeveloperAgent._call_ai_service(
                prompt=f"""
                You are a senior full stack developer. Analyze this project and determine the optimal tech stack.
                
                PROJECT: {project_name}
                REQUIREMENTS: {requirements}
                REFINED REQUIREMENTS: {refined_requirements}
                DATA MODEL: {data_model}
                SYSTEM ARCHITECTURE: {system_architecture}
                
                CRITICAL: You must return ONLY valid JSON. No explanations, no markdown, no additional text.
                
                TASK: Determine the optimal tech stack. Return ONLY a JSON response with this exact structure:
                {{
                    "project_type": "web_app",
                    "tech_stack_reasoning": "explanation",
                    "frontend": {{
                        "framework": "React.js",
                        "language": "JavaScript",
                        "styling": "CSS-in-JS"
                    }},
                    "backend": {{
                        "language": "Node.js",
                        "framework": "Express.js"
                    }},
                    "database": {{
                        "type": "PostgreSQL"
                    }},
                    "deployment": {{
                        "platform": "Cloud",
                        "containerization": "Docker"
                    }}
                }}
                
                Choose practical, production-ready technologies that match the project requirements.
                Remember: ONLY JSON, nothing else.
                """,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            if not ai_response:
                raise ValueError("AI response was empty")
            

            
            # Parse the JSON response with fallback logic
            try:
                # Try to parse the response directly
                tech_stack = json.loads(ai_response)
                return tech_stack
            except json.JSONDecodeError as e:
                print(f"JSON parsing failed: {e}")
                print(f"Full AI response: {ai_response}")
                
                # Try to extract JSON from the response if it contains extra text
                try:
                    # Look for JSON-like content between curly braces
                    start = ai_response.find('{')
                    end = ai_response.rfind('}') + 1
                    if start != -1 and end != 0:
                        json_content = ai_response[start:end]
                        tech_stack = json.loads(json_content)
                        print(f"Successfully extracted JSON from response")
                        return tech_stack
                except json.JSONDecodeError as extract_error:
                    print(f"JSON extraction also failed: {extract_error}")
                
                # If all parsing attempts fail, provide a fallback tech stack
                print("Using fallback tech stack due to JSON parsing failure")
                return {
                    "project_type": "web_app",
                    "tech_stack_reasoning": "Fallback due to AI response parsing failure",
                    "frontend": {
                        "framework": "HTML/CSS",
                        "language": "HTML",
                        "styling": "CSS"
                    },
                    "backend": {
                        "language": "None",
                        "framework": "None"
                    },
                    "database": {
                        "type": "None"
                    },
                    "deployment": {
                        "platform": "Static Hosting",
                        "containerization": "None"
                    }
                }
                
        except Exception as e:
            # If AI fails, raise an error - no fallback to hardcoded defaults
            raise RuntimeError(f"AI tech stack analysis failed: {str(e)}. Please retry or check your AI provider configuration.")
    
    @staticmethod
    async def _generate_data_model(
        project_name: str,
        requirements: str,
        refined_requirements: str,
        system_architecture: str,
        ai_provider: str,
        db_session
    ) -> str:
        """
        Generate a comprehensive data model based on requirements and system architecture.
        """
        try:
            ai_response = await FullStackDeveloperAgent._call_ai_service(
                prompt=f"""
                You are a senior database architect and data modeler. Create a comprehensive data model for this project.
                
                PROJECT: {project_name}
                REQUIREMENTS: {requirements}
                REFINED REQUIREMENTS: {refined_requirements}
                SYSTEM ARCHITECTURE: {system_architecture}
                
                TASK: Design a complete database schema that supports all the project requirements.
                
                Your data model should include:
                
                1. **Entity Analysis**
                   - Identify all major entities from the requirements
                   - Define relationships between entities
                   - Determine cardinality (one-to-one, one-to-many, many-to-many)
                
                2. **Database Schema**
                   - Table definitions with columns and data types
                   - Primary keys, foreign keys, and constraints
                   - Indexes for performance optimization
                   - Normalization considerations
                
                3. **Data Relationships**
                   - ERD (Entity Relationship Diagram) description
                   - Foreign key relationships
                   - Junction tables for many-to-many relationships
                
                4. **Data Validation**
                   - Field constraints and validation rules
                   - Business logic for data integrity
                   - Required vs optional fields
                
                5. **Performance Considerations**
                   - Partitioning strategies if needed
                   - Caching recommendations
                   - Query optimization suggestions
                
                6. **Implementation Notes**
                   - Database technology recommendations
                   - Migration strategy
                   - Backup and recovery considerations
                
                Return a comprehensive data model specification that developers can implement directly.
                Focus on creating a robust, scalable, and maintainable database design.
                """,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            if not ai_response:
                raise ValueError("AI response was empty")
            
            return ai_response
            
        except Exception as e:
            raise RuntimeError(f"Data model generation failed: {str(e)}. Please retry or check your AI provider configuration.")
    
    @staticmethod
    async def _generate_project_structure(
        project_id: int,
        project_name: str,
        tech_stack: Dict[str, Any]
    ) -> Path:
        """
        Create the project directory structure based on the tech stack.
        """
        # Sanitize project name for file system
        sanitized_name = "".join(c for c in project_name.lower() if c.isalnum() or c in (' ', '-', '_')).rstrip().replace(' ', '_')
        sanitized_name = sanitized_name.replace('-', '_')
        
        # Create project directory
        projects_dir = Path("projects")
        projects_dir.mkdir(exist_ok=True)
        
        project_dir = projects_dir / f"{project_id}_{sanitized_name}"
        project_dir.mkdir(exist_ok=True)
        
        # Create basic structure
        (project_dir / "docs").mkdir(exist_ok=True)
        (project_dir / "config").mkdir(exist_ok=True)
        (project_dir / "scripts").mkdir(exist_ok=True)
        
        # Create tech stack documentation
        tech_stack_file = project_dir / "tech-stack.md"
        tech_stack_file.write_text(f"""# Tech Stack for {project_name}

## AI Analysis Results

{json.dumps(tech_stack, indent=2)}

## Project Type
{tech_stack.get('project_type', 'Unknown')}

## Reasoning
{tech_stack.get('tech_stack_reasoning', 'No reasoning provided')}

## Frontend
- Framework: {tech_stack.get('frontend', {}).get('framework', 'Not specified')}
- Language: {tech_stack.get('frontend', {}).get('language', 'Not specified')}
- Styling: {tech_stack.get('frontend', {}).get('styling', 'Not specified')}

## Backend
- Language: {tech_stack.get('backend', {}).get('language', 'Not specified')}
- Framework: {tech_stack.get('backend', {}).get('framework', 'Not specified')}

## Database
- Type: {tech_stack.get('database', {}).get('type', 'Not specified')}

## Deployment
- Platform: {tech_stack.get('deployment', {}).get('platform', 'Not specified')}
- Containerization: {tech_stack.get('deployment', {}).get('containerization', 'Not specified')}
""")
        
        return project_dir
    
    @staticmethod
    async def _generate_code(
        project_name: str,
        requirements: str,
        refined_requirements: str,
        data_model: str,
        system_architecture: str,
        ux_design: str,
        tech_stack: Dict[str, Any],
        project_path: Path,
        ai_provider: str,
        db_session
    ) -> Dict[str, Any]:
        """
        Generate the actual code based on the tech stack analysis using AI.
        """
        try:
            print(f"Starting AI-driven code generation for project: {project_name}")
            print(f"Tech stack received: {tech_stack}")
            if not tech_stack:
                raise ValueError("Tech stack is None in _generate_code")
            print(f"Tech stack: {tech_stack.get('project_type', 'Unknown')}")
            
            # Use AI to generate the complete project structure and code
            files_created = await FullStackDeveloperAgent._generate_ai_driven_project(
                project_path, tech_stack, project_name, requirements, 
                refined_requirements, data_model, system_architecture, ux_design, ai_provider, db_session
            )
            
            return {
                "status": "AI-driven code generation completed successfully",
                "tech_stack_applied": tech_stack,
                "files_created": files_created,
                "instructions": f"Project generated with {len(files_created)} files using AI. Check the project directory for setup instructions.",
                "dependencies": tech_stack.get("dependencies", {}) if tech_stack else {}
            }
            
        except Exception as e:
            print(f"AI code generation error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "status": "Code generation failed",
                "error": str(e)
            }
    
    @staticmethod
    async def _generate_ai_driven_project(
        project_path: Path,
        tech_stack: Dict[str, Any],
        project_name: str,
        requirements: str,
        refined_requirements: str,
        data_model: str,
        system_architecture: str,
        ux_design: str,
        ai_provider: str,
        db_session
    ) -> List[str]:
        """
        Use AI to generate the complete project structure and code based on tech stack.
        """
        files_created = []
        
        try:
            
            # Step 1: Use AI to determine project structure
            structure_prompt = f"""
            You are a senior full stack developer. Based on the tech stack analysis, determine the optimal project structure.
            
            PROJECT: {project_name}
            REQUIREMENTS: {requirements}
            TECH STACK: {json.dumps(tech_stack, indent=2)}
            
            TASK: Return ONLY a JSON array of folder paths that should be created for this project type.
            Example: ["src", "src/components", "src/pages", "config", "docs"]
            
            Consider the project type ({tech_stack.get('project_type', 'web_app') if tech_stack else 'web_app'}) and tech stack when determining structure.
            """
            
            structure_response = await FullStackDeveloperAgent._call_ai_service(
                prompt=structure_prompt,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            # Create project structure
            try:
                folder_structure = json.loads(structure_response)
                for folder in folder_structure:
                    folder_path = project_path / folder
                    folder_path.mkdir(parents=True, exist_ok=True)
                    print(f"Created folder: {folder}")
            except json.JSONDecodeError:
                # Fallback to basic structure if AI fails
                basic_folders = ["src", "config", "docs"]
                for folder in basic_folders:
                    folder_path = project_path / folder
                    folder_path.mkdir(exist_ok=True)
                    print(f"Created fallback folder: {folder}")
            
            # Step 2: Use AI to generate configuration files
            config_files = await FullStackDeveloperAgent._generate_ai_config_files(
                project_path, tech_stack, project_name, ai_provider, db_session
            )
            files_created.extend(config_files)
            
            # Step 3: Use AI to generate source code files
            print(f"Starting source file generation for project: {project_name}")
            source_files = await FullStackDeveloperAgent._generate_ai_source_files(
                project_path, tech_stack, project_name, requirements, 
                refined_requirements, data_model, system_architecture, ux_design, ai_provider, db_session
            )
            print(f"Source files generated: {source_files}")
            files_created.extend(source_files)
            
            return files_created
            
        except Exception as e:
            print(f"Error in AI-driven project generation: {e}")
            raise RuntimeError(f"Failed to generate AI-driven project: {str(e)}")
    
    @staticmethod
    async def _generate_ai_config_files(
        project_path: Path,
        tech_stack: Dict[str, Any],
        project_name: str,
        ai_provider: str,
        db_session
    ) -> List[str]:
        """Use AI to generate configuration files based on tech stack."""
        files_created = []
        
        try:
            
            # Generate package.json or requirements.txt based on backend language
            backend_info = tech_stack.get("backend") or {}
            backend_lang = backend_info.get("language", "Node.js") if backend_info else "Node.js"
            
            if backend_lang == "Node.js":
                # Use AI to generate package.json
                package_prompt = f"""
                Generate a package.json file for this Node.js project.
                
                PROJECT: {project_name}
                TECH STACK: {json.dumps(tech_stack, indent=2)}
                
                Return ONLY the JSON content for package.json, no explanations.
                Include appropriate dependencies for the project type and requirements.
                """
                
                package_content = await FullStackDeveloperAgent._call_ai_service(
                    prompt=package_prompt,
                    ai_provider=ai_provider,
                    db_session=db_session
                )
                
                package_file = project_path / "package.json"
                package_file.write_text(package_content)
                files_created.append("package.json")
                
            elif backend_lang == "Python":
                # Use AI to generate requirements.txt
                requirements_prompt = f"""
                Generate a requirements.txt file for this Python project.
                
                PROJECT: {project_name}
                TECH STACK: {json.dumps(tech_stack, indent=2)}
                
                Return ONLY the requirements.txt content, one package per line with versions.
                Include appropriate dependencies for the project type and requirements.
                """
                
                requirements_content = await FullStackDeveloperAgent._call_ai_service(
                    prompt=requirements_prompt,
                    ai_provider=ai_provider,
                    db_session=db_session
                )
                
                requirements_file = project_path / "requirements.txt"
                requirements_file.write_text(requirements_content)
                files_created.append("requirements.txt")
            
            # Generate other config files based on tech stack
            deployment_info = tech_stack.get("deployment") or {}
            if deployment_info.get("containerization") == "Docker":
                docker_prompt = f"""
                Generate a Dockerfile for this project.
                
                PROJECT: {project_name}
                TECH STACK: {json.dumps(tech_stack, indent=2)}
                
                Return ONLY the Dockerfile content, no explanations.
                """
                
                docker_content = await FullStackDeveloperAgent._call_ai_service(
                    prompt=docker_prompt,
                    ai_provider=ai_provider,
                    db_session=db_session
                )
                
                dockerfile_path = project_path / "Dockerfile"
                dockerfile_path.write_text(docker_content)
                files_created.append("Dockerfile")
            
            # Generate .gitignore
            gitignore_prompt = f"""
                Generate a .gitignore file for this project.
                
                PROJECT: {project_name}
                TECH STACK: {json.dumps(tech_stack, indent=2)}
                
                Return ONLY the .gitignore content, no explanations.
                Include appropriate exclusions for the project type and tech stack.
                """
            
            gitignore_content = await FullStackDeveloperAgent._call_ai_service(
                prompt=gitignore_prompt,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            gitignore_path = project_path / ".gitignore"
            gitignore_path.write_text(gitignore_content)
            files_created.append(".gitignore")
            
            return files_created
            
        except Exception as e:
            print(f"Error generating AI config files: {e}")
            return []
    
    @staticmethod
    async def _generate_ai_source_files(
        project_path: Path,
        tech_stack: Dict[str, Any],
        project_name: str,
        requirements: str,
        refined_requirements: str,
        data_model: str,
        system_architecture: str,
        ux_design: str,
        ai_provider: str,
        db_session
    ) -> List[str]:
        """Use AI to generate source code files based on tech stack and requirements."""
        files_created = []
        
        try:
            
            project_type = tech_stack.get("project_type", "web_app")
            backend_info = tech_stack.get("backend") or {}
            backend_lang = backend_info.get("language", "Node.js") if backend_info else "None"
            frontend_info = tech_stack.get("frontend") or {}
            frontend_framework = frontend_info.get("framework", "React.js") if frontend_info else "HTML/CSS"
            print(f"Project type: {project_type}, Backend: {backend_lang}, Frontend: {frontend_framework}")
            
            # Generate backend code based on language
            if backend_lang == "Node.js":
                backend_files = await FullStackDeveloperAgent._generate_ai_nodejs_backend(
                    project_path, tech_stack, project_name, requirements, refined_requirements, 
                    data_model, system_architecture, ux_design, ai_provider, db_session
                )
                files_created.extend(backend_files)
            elif backend_lang == "Python":
                backend_files = await FullStackDeveloperAgent._generate_ai_python_backend(
                    project_path, tech_stack, project_name, requirements, refined_requirements,
                    data_model, system_architecture, ux_design, ai_provider, db_session
                )
                files_created.extend(backend_files)
            elif backend_lang in [None, "None", "null"]:
                # No backend needed (static sites, etc.)
                print(f"No backend required for project type '{project_type}'")
            else:
                # Handle unsupported backend languages
                print(f"Warning: Unsupported backend language '{backend_lang}' for project type '{project_type}'")
                print("Available backend languages: Node.js, Python, None (for static sites)")
                # Don't raise an error, just skip backend generation and continue
            
            # Generate frontend code based on framework
            print(f"Frontend framework: '{frontend_framework}', Project type: '{project_type}'")
            if frontend_framework == "React.js":
                frontend_files = await FullStackDeveloperAgent._generate_ai_react_frontend(
                    project_path, tech_stack, project_name, requirements, refined_requirements,
                    data_model, system_architecture, ux_design, ai_provider, db_session
                )
                files_created.extend(frontend_files)
            elif frontend_framework == "Vue.js":
                frontend_files = await FullStackDeveloperAgent._generate_ai_vue_frontend(
                    project_path, tech_stack, project_name, requirements, refined_requirements,
                    data_model, system_architecture, ux_design, ai_provider, db_session
                )
                files_created.extend(frontend_files)
            elif frontend_framework in ["Jekyll", "HTML/CSS", "HTML"] or project_type == "static_website":
                frontend_files = await FullStackDeveloperAgent._generate_ai_static_website(
                    project_path, tech_stack, project_name, requirements, refined_requirements,
                    data_model, system_architecture, ux_design, ai_provider, db_session
                )
                files_created.extend(frontend_files)
            else:
                # Handle unsupported tech stacks
                print(f"Warning: Unsupported frontend framework '{frontend_framework}' for project type '{project_type}'")
                print("Available frameworks: React.js, Vue.js, Jekyll, HTML/CSS")
                # Don't raise an error, just skip frontend generation and continue
            
            return files_created
            
        except Exception as e:
            print(f"Error generating AI source files: {e}")
            return []
    
    @staticmethod
    async def _generate_ai_nodejs_backend(
        project_path: Path,
        tech_stack: Dict[str, Any],
        project_name: str,
        requirements: str,
        refined_requirements: str,
        data_model: str,
        system_architecture: str,
        ux_design: str,
        ai_provider: str,
        db_session
    ) -> List[str]:
        """Use AI to generate Node.js backend code."""
        files_created = []
        
        try:
            # Generate main server file
            server_prompt = f"""
                Generate a Node.js/Express server file for this project.
                
                PROJECT: {project_name}
                REQUIREMENTS: {requirements}
                REFINED REQUIREMENTS: {refined_requirements}
                DATA MODEL: {data_model}
                SYSTEM ARCHITECTURE: {system_architecture}
                UX DESIGN: {ux_design}
                TECH STACK: {json.dumps(tech_stack, indent=2)}
                
                Return ONLY the JavaScript code, no explanations.
                Include proper error handling, middleware setup, and basic routes.
                Use the data model to create appropriate database models and routes.
                Follow the system architecture and UX design specifications.
                """
            
            server_content = await FullStackDeveloperAgent._call_ai_service(
                prompt=server_prompt,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            server_file = project_path / "server.js"
            server_file.write_text(server_content)
            files_created.append("server.js")
            
            # Generate .env template
            env_prompt = f"""
                Generate a .env.example file for this Node.js project.
                
                PROJECT: {project_name}
                TECH STACK: {json.dumps(tech_stack, indent=2)}
                
                Return ONLY the .env.example content, no explanations.
                Include appropriate environment variables for the project.
                """
            
            env_content = await FullStackDeveloperAgent._call_ai_service(
                prompt=env_prompt,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            env_file = project_path / ".env.example"
            env_file.write_text(env_content)
            files_created.append(".env.example")
            
            return files_created
            
        except Exception as e:
            print(f"Error generating Node.js backend: {e}")
            return []
    
    @staticmethod
    async def _generate_ai_python_backend(
        project_path: Path,
        tech_stack: Dict[str, Any],
        project_name: str,
        requirements: str,
        refined_requirements: str,
        data_model: str,
        system_architecture: str,
        ux_design: str,
        ai_provider: str,
        db_session
    ) -> List[str]:
        """Use AI to generate Python backend code."""
        files_created = []
        
        try:
            # Generate main app file
            app_prompt = f"""
                Generate a Python FastAPI application file for this project.
                
                PROJECT: {project_name}
                REQUIREMENTS: {requirements}
                REFINED REQUIREMENTS: {refined_requirements}
                DATA MODEL: {data_model}
                SYSTEM ARCHITECTURE: {system_architecture}
                UX DESIGN: {ux_design}
                TECH STACK: {json.dumps(tech_stack, indent=2)}
                
                Return ONLY the Python code, no explanations.
                Include proper error handling, route setup, and basic endpoints.
                Use the data model to create appropriate database models and routes.
                Follow the system architecture and UX design specifications.
                """
            
            app_content = await FullStackDeveloperAgent._call_ai_service(
                prompt=app_prompt,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            app_file = project_path / "main.py"
            app_file.write_text(app_content)
            files_created.append("main.py")
            
            return files_created
            
        except Exception as e:
            print(f"Error generating Python backend: {e}")
            return []
    
    @staticmethod
    async def _generate_ai_react_frontend(
        project_path: Path,
        tech_stack: Dict[str, Any],
        project_name: str,
        requirements: str,
        refined_requirements: str,
        data_model: str,
        system_architecture: str,
        ux_design: str,
        ai_provider: str,
        db_session
    ) -> List[str]:
        """Use AI to generate React frontend code."""
        files_created = []
        
        try:
            # Create frontend directory structure
            frontend_dir = project_path / "frontend"
            frontend_dir.mkdir(exist_ok=True)
            
            src_dir = frontend_dir / "src"
            src_dir.mkdir(exist_ok=True)
            
            # Generate main App component
            app_prompt = f"""
                Generate a React App.js component for this project.
                
                PROJECT: {project_name}
                REQUIREMENTS: {requirements}
                REFINED REQUIREMENTS: {refined_requirements}
                DATA MODEL: {data_model}
                SYSTEM ARCHITECTURE: {system_architecture}
                UX DESIGN: {ux_design}
                TECH STACK: {json.dumps(tech_stack, indent=2)}
                
                Return ONLY the React JavaScript code, no explanations.
                Create a component that matches the project requirements.
                Follow the UX design specifications for layout, components, and interactions.
                Use the data model to understand what data to display and manage.
                """
            
            app_content = await FullStackDeveloperAgent._call_ai_service(
                prompt=app_prompt,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            app_file = src_dir / "App.js"
            app_file.write_text(app_content)
            files_created.append("frontend/src/App.js")
            
            # Generate package.json for frontend
            package_prompt = f"""
                Generate a package.json file for this React frontend.
                
                PROJECT: {project_name}
                TECH STACK: {json.dumps(tech_stack, indent=2)}
                
                Return ONLY the JSON content for package.json, no explanations.
                Include appropriate React dependencies and scripts.
                """
            
            package_content = await FullStackDeveloperAgent._call_ai_service(
                prompt=package_prompt,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            package_file = frontend_dir / "package.json"
            package_file.write_text(package_content)
            files_created.append("frontend/package.json")
            
            return files_created
            
        except Exception as e:
            print(f"Error generating React frontend: {e}")
            return []
    
    @staticmethod
    async def _generate_ai_vue_frontend(
        project_path: Path,
        tech_stack: Dict[str, Any],
        project_name: str,
        requirements: str,
        refined_requirements: str,
        data_model: str,
        system_architecture: str,
        ux_design: str,
        ai_provider: str,
        db_session
    ) -> List[str]:
        """Use AI to generate Vue.js frontend code."""
        files_created = []
        
        try:
            # Create frontend directory structure
            frontend_dir = project_path / "frontend"
            frontend_dir.mkdir(exist_ok=True)
            
            # Generate Vue app files
            app_prompt = f"""
                Generate a Vue.js main.js file for this project.
                
                PROJECT: {project_name}
                REQUIREMENTS: {requirements}
                REFINED REQUIREMENTS: {refined_requirements}
                DATA MODEL: {data_model}
                SYSTEM ARCHITECTURE: {system_architecture}
                UX DESIGN: {ux_design}
                TECH STACK: {json.dumps(tech_stack, indent=2)}
                
                Return ONLY the Vue JavaScript code, no explanations.
                Follow the UX design specifications for layout, components, and interactions.
                Use the data model to understand what data to display and manage.
                """
            
            app_content = await FullStackDeveloperAgent._call_ai_service(
                prompt=app_prompt,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            app_file = frontend_dir / "main.js"
            app_file.write_text(app_content)
            files_created.append("frontend/main.js")
            
            return files_created
            
        except Exception as e:
            print(f"Error generating Vue frontend: {e}")
            return []
    
    @staticmethod
    async def _generate_ai_static_website(
        project_path: Path,
        tech_stack: Dict[str, Any],
        project_name: str,
        requirements: str,
        refined_requirements: str,
        data_model: str,
        system_architecture: str,
        ux_design: str,
        ai_provider: str,
        db_session
    ) -> List[str]:
        """Use AI to generate static HTML website code."""
        files_created = []
        
        try:
            
            frontend_info = tech_stack.get("frontend") or {}
            frontend_framework = frontend_info.get("framework", "HTML") if frontend_info else "HTML"
            
            if frontend_framework == "Jekyll":
                # Generate Jekyll static site
                files_created.extend(await FullStackDeveloperAgent._generate_jekyll_site(
                    project_path, tech_stack, project_name, requirements, refined_requirements,
                    data_model, system_architecture, ux_design, ai_provider, db_session
                ))
            else:
                # Generate pure HTML/CSS/JS static site
                files_created.extend(await FullStackDeveloperAgent._generate_html_site(
                    project_path, tech_stack, project_name, requirements, refined_requirements,
                    data_model, system_architecture, ux_design, ai_provider, db_session
                ))
            
            return files_created
            
        except Exception as e:
            print(f"Error generating static website: {e}")
            return []
    
    @staticmethod
    async def _generate_jekyll_site(
        project_path: Path,
        tech_stack: Dict[str, Any],
        project_name: str,
        requirements: str,
        refined_requirements: str,
        data_model: str,
        system_architecture: str,
        ux_design: str,
        ai_provider: str,
        db_session
    ) -> List[str]:
        """Generate Jekyll static site files."""
        files_created = []
        
        try:
            # Generate Jekyll config file
            config_prompt = f"""
            Generate a Jekyll _config.yml file for this project.
            
            PROJECT: {project_name}
            REQUIREMENTS: {requirements}
            TECH STACK: {json.dumps(tech_stack, indent=2)}
            
            Return ONLY the YAML content for _config.yml. Include:
            - Site title and description
            - Base URL and URL settings
            - Jekyll plugins and settings
            - Theme configuration if applicable
            """
            
            config_response = await FullStackDeveloperAgent._call_ai_service(
                prompt=config_prompt,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            config_file = project_path / "_config.yml"
            config_file.write_text(config_response.strip())
            files_created.append("_config.yml")
            
            # Generate main layout
            layout_prompt = f"""
            Generate a Jekyll default layout file (_layouts/default.html) for this project.
            
            PROJECT: {project_name}
            REQUIREMENTS: {requirements}
            UX DESIGN: {ux_design[:1000]}...
            
            Return ONLY the HTML content for the default layout. Include:
            - HTML5 structure
            - Responsive meta tags
            - Navigation based on the project requirements
            - Content area for pages
            - Footer
            """
            
            layout_response = await FullStackDeveloperAgent._call_ai_service(
                prompt=layout_prompt,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            layouts_dir = project_path / "_layouts"
            layouts_dir.mkdir(exist_ok=True)
            layout_file = layouts_dir / "default.html"
            layout_file.write_text(layout_response.strip())
            files_created.append("_layouts/default.html")
            
            # Generate main CSS
            css_prompt = f"""
            Generate a main CSS file (assets/css/main.css) for this project.
            
            PROJECT: {project_name}
            REQUIREMENTS: {requirements}
            UX DESIGN: {ux_design[:1000]}...
            
            Return ONLY the CSS content. Include:
            - Reset/normalize styles
            - Typography
            - Layout styles
            - Responsive design
            - Component styles based on the project requirements
            """
            
            css_response = await FullStackDeveloperAgent._call_ai_service(
                prompt=css_prompt,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            css_dir = project_path / "assets" / "css"
            css_dir.mkdir(parents=True, exist_ok=True)
            css_file = css_dir / "main.css"
            css_file.write_text(css_response.strip())
            files_created.append("assets/css/main.css")
            
            # Generate main pages based on requirements
            pages = await FullStackDeveloperAgent._generate_static_pages(
                project_path, project_name, requirements, refined_requirements,
                system_architecture, ux_design, ai_provider, db_session, is_jekyll=True
            )
            files_created.extend(pages)
            
            return files_created
            
        except Exception as e:
            print(f"Error generating Jekyll site: {e}")
            return []
    
    @staticmethod
    async def _generate_html_site(
        project_path: Path,
        tech_stack: Dict[str, Any],
        project_name: str,
        requirements: str,
        refined_requirements: str,
        data_model: str,
        system_architecture: str,
        ux_design: str,
        ai_provider: str,
        db_session
    ) -> List[str]:
        """Generate pure HTML/CSS/JS static site files."""
        files_created = []
        
        try:
            # Generate main CSS
            css_prompt = f"""
            Generate a main CSS file (css/style.css) for this project.
            
            PROJECT: {project_name}
            REQUIREMENTS: {requirements}
            UX DESIGN: {ux_design[:1000]}...
            
            Return ONLY the CSS content. Include:
            - Reset/normalize styles
            - Typography
            - Layout styles
            - Responsive design
            - Component styles based on the project requirements
            """
            
            css_response = await FullStackDeveloperAgent._call_ai_service(
                prompt=css_prompt,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            css_dir = project_path / "css"
            css_dir.mkdir(exist_ok=True)
            css_file = css_dir / "style.css"
            css_file.write_text(css_response.strip())
            files_created.append("css/style.css")
            
            # Generate main JavaScript if needed
            js_prompt = f"""
            Generate a main JavaScript file (js/main.js) for this project if interactive features are needed.
            
            PROJECT: {project_name}
            REQUIREMENTS: {requirements}
            
            Return ONLY the JavaScript content. Include:
            - DOM manipulation
            - Event handlers
            - Interactive features based on requirements
            - If no JavaScript is needed, return "// No JavaScript required for this project"
            """
            
            js_response = await FullStackDeveloperAgent._call_ai_service(
                prompt=js_prompt,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            if not js_response.strip().startswith("// No JavaScript required"):
                js_dir = project_path / "js"
                js_dir.mkdir(exist_ok=True)
                js_file = js_dir / "main.js"
                js_file.write_text(js_response.strip())
                files_created.append("js/main.js")
            
            # Generate main pages
            pages = await FullStackDeveloperAgent._generate_static_pages(
                project_path, project_name, requirements, refined_requirements,
                system_architecture, ux_design, ai_provider, db_session, is_jekyll=False
            )
            files_created.extend(pages)
            
            return files_created
            
        except Exception as e:
            print(f"Error generating HTML site: {e}")
            return []
    
    @staticmethod
    async def _generate_static_pages(
        project_path: Path,
        project_name: str,
        requirements: str,
        refined_requirements: str,
        system_architecture: str,
        ux_design: str,
        ai_provider: str,
        db_session,
        is_jekyll: bool = False
    ) -> List[str]:
        """Generate static HTML pages based on project requirements."""
        files_created = []
        
        try:
            # First, generate the index.html page
            index_prompt = f"""
            Generate the main index.html page for this project.
            
            PROJECT: {project_name}
            REQUIREMENTS: {requirements}
            UX DESIGN: {ux_design[:1000]}...
            
            Return ONLY the complete HTML content. Include:
            - HTML5 structure
            - Proper meta tags
            - Navigation menu with links to other pages (e.g., setup.html, email.html, security.html, about.html)
            - Main content based on the project requirements
            - Footer
            - Link to CSS file ({'assets/css/main.css' if is_jekyll else 'css/style.css'})
            - Link to JS file if needed ({'assets/js/main.js' if is_jekyll else 'js/main.js'})
            
            Make sure to include navigation links to pages that make sense for this project.
            """
            
            index_response = await FullStackDeveloperAgent._call_ai_service(
                prompt=index_prompt,
                ai_provider=ai_provider,
                db_session=db_session
            )
            
            # Write the index.html file
            index_file = project_path / "index.html"
            index_file.write_text(index_response.strip())
            files_created.append("index.html")
            
            # Extract navigation links from the generated index.html
            import re
            nav_links = re.findall(r'href=["\']([^"\']*\.html)["\']', index_response)
            nav_links = [link for link in nav_links if link != "index.html"]  # Remove self-reference
            
            # Extract the navigation HTML from index.html
            nav_match = re.search(r'<nav[^>]*>(.*?)</nav>', index_response, re.DOTALL)
            navigation_html = nav_match.group(1) if nav_match else ""
            
            # Create page configs for all navigation links
            pages_config = [{"filename": "index.html", "title": "Home", "description": "Main landing page"}]
            
            for link in nav_links:
                # Extract page name from filename
                page_name = link.replace('.html', '').replace('-', ' ').replace('_', ' ').title()
                pages_config.append({
                    "filename": link,
                    "title": page_name,
                    "description": f"Page about {page_name.lower()}"
                })
            
            # If no navigation links found, add some default pages
            if len(pages_config) == 1:
                pages_config.extend([
                    {"filename": "about.html", "title": "About", "description": "About page"},
                    {"filename": "contact.html", "title": "Contact", "description": "Contact page"}
                ])
            
            # Generate each page (skip index.html since we already generated it)
            for page_config in pages_config:
                filename = page_config["filename"]
                title = page_config["title"]
                description = page_config["description"]
                
                # Skip index.html since we already generated it
                if filename == "index.html":
                    continue
                
                page_prompt = f"""
                Generate an HTML page for this project.
                
                PROJECT: {project_name}
                PAGE: {title} ({filename})
                DESCRIPTION: {description}
                REQUIREMENTS: {requirements}
                UX DESIGN: {ux_design[:1000]}...
                
                IMPORTANT: Use this EXACT navigation menu from the index.html page:
                {navigation_html}
                
                Return ONLY the complete HTML content. Include:
                - HTML5 structure
                - Proper meta tags
                - Navigation menu with the EXACT HTML provided above
                - Main content based on the page description and project requirements
                - Footer
                - Link to CSS file ({'assets/css/main.css' if is_jekyll else 'css/style.css'})
                - Link to JS file if needed ({'assets/js/main.js' if is_jekyll else 'js/main.js'})
                
                Do NOT modify the navigation menu. Use the exact HTML provided above.
                """
                
                page_response = await FullStackDeveloperAgent._call_ai_service(
                    prompt=page_prompt,
                    ai_provider=ai_provider,
                    db_session=db_session
                )
                
                if is_jekyll:
                    pages_dir = project_path / "pages"
                    pages_dir.mkdir(exist_ok=True)
                    page_file = pages_dir / filename
                else:
                    page_file = project_path / filename
                
                page_file.write_text(page_response.strip())
                files_created.append(str(page_file.relative_to(project_path)))
            
            return files_created
            
        except Exception as e:
            print(f"Error generating static pages: {e}")
            return []
    
    @staticmethod
    async def _generate_documentation(
        project_name: str,
        tech_stack: Dict[str, Any],
        project_path: Path,
        ai_provider: str,
        db_session
    ) -> Dict[str, Any]:
        """
        Generate comprehensive documentation for the project.
        """
        try:
            # Generate README
            readme_content = f"""# {project_name}

## Overview
This project was generated by the BMAD AI system based on your requirements.

## Tech Stack
- **Project Type**: {tech_stack.get('project_type', 'Unknown') if tech_stack else 'Unknown'}
- **Frontend**: {(tech_stack.get('frontend') or {}).get('framework', 'Not specified') if tech_stack else 'Not specified'}
- **Backend**: {(tech_stack.get('backend') or {}).get('framework', 'Not specified') if tech_stack else 'Not specified'}
- **Database**: {(tech_stack.get('database') or {}).get('type', 'Not specified') if tech_stack else 'Not specified'}

## Quick Start
1. Review the tech stack analysis in `tech-stack.md`
2. Follow the setup instructions for your chosen technologies
3. Run the application according to the framework-specific instructions

## Project Structure
```
{project_path.name}/
├── src/            # Source code
├── config/         # Configuration files
├── docs/           # Documentation
└── tech-stack.md   # AI tech stack analysis
```

## Next Steps
- Customize the generated code to match your specific needs
- Add additional features and functionality
- Deploy to your preferred hosting platform

## Support
This project was generated by AI. Review and test all code before production use.
"""
            
            readme_file = project_path / "README.md"
            readme_file.write_text(readme_content)
            
            return {
                "status": "Documentation generated",
                "files_created": ["README.md", "tech-stack.md"]
            }
            
        except Exception as e:
            return {
                "status": "Documentation generation failed",
                "error": str(e)
            }
    
    @staticmethod
    async def _call_ai_service(prompt: str, ai_provider: str, db_session) -> str:
        """
        Unified method to call any AI service based on database configuration.
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
