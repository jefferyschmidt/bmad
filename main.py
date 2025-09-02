"""
BMAD Pipeline MVP - Database-integrated version
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List
import json

from database import get_db, init_db
from models import Project, AIProvider
from services import ProjectService
from agents.requirements_analyst import RequirementsAnalystAgent
from agents.ux_designer import UXDesignerAgent
from agents.software_architect import SoftwareArchitectAgent
from schemas import (
    ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse,
    RequirementsAnalysisResponse, UXDesignResponse, SystemArchitectureResponse,
    ArchiveProjectRequest, AIProviderResponse, ProjectGenerationResponse
)

app = FastAPI(title="BMAD API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {"message": "BMAD API is running"}

@app.get("/api/v1/ai-providers", response_model=List[AIProviderResponse])
async def get_ai_providers(db: AsyncSession = Depends(get_db)):
    """Get all active AI providers"""
    try:
        result = await db.execute(
            text("SELECT * FROM bmad_ai_providers WHERE is_active = true ORDER BY name")
        )
        providers = result.fetchall()
        
        # Convert to AIProviderResponse objects
        ai_providers = []
        for row in providers:
            ai_providers.append(AIProviderResponse(
                id=row[0],
                name=row[1],
                display_name=row[2],
                api_key=row[3],
                model_name=row[4],
                max_tokens=row[5],
                is_active=row[6],
                created_at=row[7],
                updated_at=row[8]
            ))
        
        return ai_providers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch AI providers: {str(e)}")

@app.get("/api/v1/projects", response_model=ProjectListResponse)
async def get_projects(db: AsyncSession = Depends(get_db)):
    """Get all projects"""
    try:
        result = await db.execute(
            text("SELECT * FROM bmad_projects ORDER BY created_at DESC")
        )
        projects = result.fetchall()
        
        # Convert to ProjectResponse objects
        project_list = []
        for row in projects:
            project_list.append(ProjectResponse(
                id=row[0],
                name=row[1],
                description=row[2],
                requirements=row[3],
                refined_requirements=row[4],
                user_stories=row[5],
                status=row[6],
                created_at=row[7],
                updated_at=row[8],
                archived=row[9],
                system_architecture=row[11],  # Skip data_model at index 10
                ai_provider=row[12],
                ux_design=row[13],
                tech_stack=row[14] if len(row) > 14 else None
            ))
        
        return ProjectListResponse(projects=project_list, total=len(project_list))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch projects: {str(e)}")

@app.post("/api/v1/projects", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    """Create a new project"""
    try:
        result = await db.execute(
            text("""
                INSERT INTO bmad_projects (name, description, requirements, ai_provider, status, archived, created_at, updated_at)
                VALUES (:name, :description, :requirements, :ai_provider, 'draft', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                RETURNING *
            """),
            {
                "name": project.name,
                "description": project.description,
                "requirements": project.requirements,
                "ai_provider": project.ai_provider
            }
        )
        
        new_project = result.fetchone()
        await db.commit()
        
        return ProjectResponse(
            id=new_project[0],
            name=new_project[1],
            description=new_project[2],
            requirements=new_project[3],
            refined_requirements=new_project[4],
            user_stories=new_project[5],
            status=new_project[6],
            created_at=new_project[7],
            updated_at=new_project[8],
            archived=new_project[9],
            system_architecture=new_project[11],  # Skip data_model at index 10
            ai_provider=new_project[12],
            ux_design=new_project[13],
            tech_stack=new_project[14] if len(new_project) > 14 else None
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")

@app.get("/api/v1/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific project by ID"""
    try:
        result = await db.execute(
            text("SELECT * FROM bmad_projects WHERE id = :id"),
            {"id": project_id}
        )
        project = result.fetchone()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return ProjectResponse(
            id=project[0],
            name=project[1],
            description=project[2],
            requirements=project[3],
            refined_requirements=project[4],
            user_stories=project[5],
            status=project[6],
            created_at=project[7],
            updated_at=project[8],
            archived=project[9],
            system_architecture=project[11],  # Skip data_model at index 10
            ai_provider=project[12],
            ux_design=project[13],
            tech_stack=project[14] if len(project) > 14 else None
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch project: {str(e)}")

@app.patch("/api/v1/projects/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project_update: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    """Update a project"""
    try:
        # Build dynamic update query
        update_fields = []
        params = {"id": project_id}
        
        if project_update.name is not None:
            update_fields.append("name = :name")
            params["name"] = project_update.name
        if project_update.description is not None:
            update_fields.append("description = :description")
            params["description"] = project_update.description
        if project_update.requirements is not None:
            update_fields.append("requirements = :requirements")
            params["requirements"] = project_update.requirements
        if project_update.ai_provider is not None:
            update_fields.append("ai_provider = :ai_provider")
            params["ai_provider"] = project_update.ai_provider


        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        
        query = f"""
            UPDATE bmad_projects 
            SET {', '.join(update_fields)}
            WHERE id = :id
            RETURNING *
        """
        
        result = await db.execute(text(query), params)
        updated_project = result.fetchone()
        
        if not updated_project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        await db.commit()
        
        return ProjectResponse(
            id=updated_project[0],
            name=updated_project[1],
            description=updated_project[2],
            requirements=updated_project[3],
            refined_requirements=updated_project[4],
            user_stories=updated_project[5],
            status=updated_project[6],
            created_at=updated_project[7],
            updated_at=updated_project[8],
            archived=updated_project[9],
            system_architecture=updated_project[11],  # Skip data_model at index 10
            ai_provider=updated_project[12],
            ux_design=updated_project[13],
            tech_stack=updated_project[14] if len(updated_project) > 14 else None
        )
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update project: {str(e)}")

@app.patch("/api/v1/projects/{project_id}/archive")
async def archive_project(project_id: int, archive_request: ArchiveProjectRequest, db: AsyncSession = Depends(get_db)):
    """Archive or unarchive a project"""
    try:
        result = await db.execute(
            text("""
                UPDATE bmad_projects 
                SET archived = :archived, updated_at = CURRENT_TIMESTAMP
                WHERE id = :id
                RETURNING *
            """),
            {"id": project_id, "archived": archive_request.archived}
        )
        
        updated_project = result.fetchone()
        if not updated_project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        await db.commit()
        
        return {
            "success": True,
            "message": f"Project {'archived' if archive_request.archived else 'unarchived'} successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update project: {str(e)}")

@app.post("/api/v1/projects/{project_id}/analyze-requirements", response_model=RequirementsAnalysisResponse)
async def analyze_requirements(project_id: int, db: AsyncSession = Depends(get_db)):
    """Analyze project requirements using the Requirements Analyst agent"""
    try:
        result = await ProjectService.analyze_requirements(db, project_id)
        return RequirementsAnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Requirements analysis failed: {str(e)}")

@app.post("/api/v1/projects/{project_id}/generate-ux-design", response_model=UXDesignResponse)
async def generate_ux_design(project_id: int, db: AsyncSession = Depends(get_db)):
    """Generate UX/UI design using the UX Designer agent"""
    try:
        result = await ProjectService.generate_ux_design(db, project_id)
        return UXDesignResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"UX design generation failed: {str(e)}")

@app.post("/api/v1/projects/{project_id}/generate-system-architecture", response_model=SystemArchitectureResponse)
async def generate_system_architecture(project_id: int, db: AsyncSession = Depends(get_db)):
    """Generate system architecture using the Software Architect agent"""
    try:
        result = await ProjectService.generate_system_architecture(db, project_id)
        return SystemArchitectureResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System architecture generation failed: {str(e)}")

@app.post("/api/v1/projects/{project_id}/generate-project", response_model=ProjectGenerationResponse)
async def generate_project(project_id: int, db: AsyncSession = Depends(get_db)):
    """Generate complete working software project using the Full Stack Developer agent"""
    try:
        result = await ProjectService.generate_project(db, project_id)
        return ProjectGenerationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Project generation failed: {str(e)}")
