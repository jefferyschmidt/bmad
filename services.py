"""
Service layer for BMAD Pipeline database operations
"""

import json
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models import Project
from schemas import ProjectCreate, ProjectUpdate
from agents import RequirementsAnalystAgent, UXDesignerAgent, SoftwareArchitectAgent, FullStackDeveloperAgent

class ProjectService:
    """Service for project operations"""
    
    @staticmethod
    async def create_project(db: AsyncSession, project_data: ProjectCreate) -> Project:
        """Create a new project"""
        db_project = Project(
            name=project_data.name,
            description=project_data.description,
            requirements=project_data.requirements,
            status="draft"
        )
        db.add(db_project)
        await db.commit()
        await db.refresh(db_project)
        return db_project
    
    @staticmethod
    async def get_project(db: AsyncSession, project_id: int) -> Optional[Project]:
        """Get a project by ID"""
        result = await db.execute(select(Project).where(Project.id == project_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all_projects(db: AsyncSession, skip: int = 0, limit: int = 100, include_archived: bool = False) -> tuple[List[Project], int]:
        """Get all projects with pagination and archive filtering"""
        # Build query with archive filter
        query = select(Project)
        if not include_archived:
            query = query.where(Project.archived == False)
        
        # Get total count
        count_query = select(func.count(Project.id))
        if not include_archived:
            count_query = count_query.where(Project.archived == False)
        count_result = await db.execute(count_query)
        total = count_result.scalar()
        
        # Get projects
        result = await db.execute(
            query
            .order_by(Project.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        projects = result.scalars().all()
        
        return projects, total
    
    @staticmethod
    async def update_project(db: AsyncSession, project_id: int, project_data: ProjectUpdate) -> Optional[Project]:
        """Update a project"""
        project = await ProjectService.get_project(db, project_id)
        if not project:
            return None
        
        update_data = project_data.model_dump(exclude_unset=True)
        
        # Check if requirements were updated
        requirements_updated = 'requirements' in update_data and update_data['requirements'] != project.requirements
        
        for field, value in update_data.items():
            setattr(project, field, value)
        
        # If requirements were updated, reset analysis and status
        if requirements_updated:
            project.status = "draft"
            project.refined_requirements = None
            project.user_stories = None
        
        await db.commit()
        await db.refresh(project)
        return project
    
    @staticmethod
    async def delete_project(db: AsyncSession, project_id: int) -> bool:
        """Delete a project"""
        project = await ProjectService.get_project(db, project_id)
        if not project:
            return False
        
        await db.delete(project)
        await db.commit()
        return True
    
    @staticmethod
    async def archive_project(db: AsyncSession, project_id: int, archived: bool) -> Optional[Project]:
        """Archive or unarchive a project"""
        project = await ProjectService.get_project(db, project_id)
        if not project:
            return None
        
        project.archived = archived
        await db.commit()
        await db.refresh(project)
        return project
    
    @staticmethod
    async def analyze_requirements(db: AsyncSession, project_id: int) -> Dict[str, Any]:
        """Analyze project requirements using the Requirements Analyst agent."""
        project = await ProjectService.get_project(db, project_id)
        if not project:
            return {"success": False, "error": "Project not found"}
        
        try:
            # Call the Requirements Analyst agent with the project's AI provider choice
            result = await RequirementsAnalystAgent.analyze_requirements(
                project_name=project.name,
                requirements=project.requirements,
                ai_provider=project.ai_provider,
                db_session=db
            )
            
            # Update project with analysis results
            project.refined_requirements = result["refined_requirements"]
            project.user_stories = json.dumps(result["user_stories"])
            project.status = "Requirements Complete"
            
            # Clear downstream artifacts since requirements have changed
            project.system_architecture = None
            project.ux_design = None
            
            await db.commit()
            await db.refresh(project)
            
            return {
                "success": True,
                "refined_requirements": result["refined_requirements"],
                "user_stories": result["user_stories"],
                "analysis_metadata": result["analysis_metadata"]
            }
            
        except Exception as e:
            await db.rollback()
            return {"success": False, "error": f"Analysis failed: {str(e)}"}

    @staticmethod
    async def generate_ux_design(db: AsyncSession, project_id: int) -> Dict[str, Any]:
        """Generate UX/UI design using the UXDesignerAgent"""
        project = await ProjectService.get_project(db, project_id)
        if not project:
            return {"success": False, "error": "Project not found"}
        
        try:
            # Use the UXDesignerAgent to generate UX/UI design
            design_result = await UXDesignerAgent.analyze_requirements(
                project_name=project.name,
                requirements=project.requirements,
                refined_requirements=project.refined_requirements,
                system_architecture=project.system_architecture,
                ai_provider=project.ai_provider,
                db_session=db
            )
            
            # Check if the design generation was successful
            if not design_result.get("success", False):
                return {"success": False, "error": design_result.get("error", "UX design generation failed")}
            
            # Update project with UX design results
            project.ux_design = design_result["ux_design"]
            project.status = "UX Design Complete"
            
            await db.commit()
            await db.refresh(project)
            
            return {
                "success": True,
                "ux_design": design_result["ux_design"],
                "analysis_metadata": design_result.get("analysis_metadata", {})
            }
            
        except Exception as e:
            await db.rollback()
            return {"success": False, "error": f"Error generating UX design: {str(e)}"}

    @staticmethod
    async def generate_system_architecture(db: AsyncSession, project_id: int) -> Dict[str, Any]:
        """Generate system architecture using the SoftwareArchitectAgent"""
        project = await ProjectService.get_project(db, project_id)
        if not project:
            return {"success": False, "error": "Project not found"}
        
        try:
            # Use the SoftwareArchitectAgent to generate system architecture
            architecture_result = await SoftwareArchitectAgent.analyze_requirements(
                project_name=project.name,
                requirements=project.requirements,
                refined_requirements=project.refined_requirements,
                ai_provider=project.ai_provider,
                db_session=db
            )
            
            # Update project with system architecture results
            project.system_architecture = architecture_result["system_architecture"]
            project.status = "System Architecture Complete"
            
            # Clear UX design since architecture has changed
            project.ux_design = None
            
            await db.commit()
            await db.refresh(project)
            
            return {
                "success": True,
                "system_architecture": architecture_result["system_architecture"],
                "analysis_metadata": architecture_result.get("analysis_metadata", {})
            }
            
        except Exception as e:
            await db.rollback()
            return {"success": False, "error": f"Error generating system architecture: {str(e)}"}

    @staticmethod
    async def generate_project(db: AsyncSession, project_id: int) -> Dict[str, Any]:
        """Generate complete working software project using the FullStackDeveloperAgent"""
        project = await ProjectService.get_project(db, project_id)
        if not project:
            return {"success": False, "error": "Project not found"}
        
        # Check if all prerequisites are complete
        if not project.refined_requirements:
            return {"success": False, "error": "Requirements analysis must be completed first"}
        if not project.system_architecture:
            return {"success": False, "error": "System architecture must be completed first"}
        if not project.ux_design:
            return {"success": False, "error": "UX/UI design must be completed first"}
        
        try:
            # Use the FullStackDeveloperAgent to generate the complete project
            project_result = await FullStackDeveloperAgent.generate_project(
                project_name=project.name,
                requirements=project.requirements,
                refined_requirements=project.refined_requirements,
                system_architecture=project.system_architecture,
                ux_design=project.ux_design,
                ai_provider=project.ai_provider,
                db_session=db,
                project_id=project.id
            )
            
            if project_result["success"]:
                # Update project status
                project.status = "Project Generated"
                await db.commit()
                await db.refresh(project)
            
            return project_result
            
        except Exception as e:
            await db.rollback()
            return {"success": False, "error": f"Error generating project: {str(e)}"}
