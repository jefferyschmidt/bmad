import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  Box,
  Chip,
  Paper,
  Alert,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Fade,
  Grow
} from '@mui/material';
import { ArrowBack, Edit, Psychology, Archive, Unarchive, Refresh } from '@mui/icons-material';
import { Project, AIProvider } from '../types/project';
import { APPLICATION_TYPES, ApplicationType, TechStack } from '../constants/applicationTypes';

const ProjectWorkspace: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [project, setProject] = useState<Project | null>(null);
  const [aiProviders, setAiProviders] = useState<AIProvider[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [editing, setEditing] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [generatingArchitecture, setGeneratingArchitecture] = useState(false);
  const [generatingUXDesign, setGeneratingUXDesign] = useState(false);
  const [generatingProject, setGeneratingProject] = useState(false);
  const [generationResult, setGenerationResult] = useState<any>(null);
  const [editForm, setEditForm] = useState({
    name: '',
    description: '',
    requirements: '',
    application_type: '',
    ai_provider: ''
  });
  const [activeStage, setActiveStage] = useState('requirements'); // 'requirements', 'data-model', 'architecture', 'project'

  // Helper functions for application type
  const getSelectedApplicationType = (): ApplicationType | undefined => {
    return APPLICATION_TYPES.find(type => type.id === editForm.application_type);
  };

  const fetchProject = useCallback(async () => {
    if (!id) return;
    try {
      const response = await fetch(`/api/v1/projects/${id}`);
      if (!response.ok) {
        throw new Error('Failed to fetch project');
      }
      const data = await response.json();
      setProject(data);
      setEditForm({
        name: data.name,
        description: data.description || '',
        requirements: data.requirements,
        application_type: data.application_type || '',
        ai_provider: data.ai_provider
      });
      // Clear generation result when fetching project to avoid stale data
      setGenerationResult(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch project');
    } finally {
      setLoading(false);
    }
  }, [id]);

  const fetchAIProviders = useCallback(async () => {
    try {
      const response = await fetch('/api/v1/ai-providers');
      if (!response.ok) {
        throw new Error('Failed to fetch AI providers');
      }
      const data = await response.json();
      setAiProviders(data);
    } catch (err) {
      console.error('Failed to fetch AI providers:', err);
      // Set default providers if API call fails
      setAiProviders([
        { id: 1, name: 'anthropic', display_name: 'Anthropic Claude', model_name: 'claude-3-haiku-20240307', max_tokens: 4000, is_active: true, created_at: '' },
        { id: 2, name: 'openai', display_name: 'OpenAI ChatGPT', model_name: 'gpt-4o', max_tokens: 4000, is_active: true, created_at: '' }
      ]);
    }
  }, []);

  useEffect(() => {
    fetchProject();
    fetchAIProviders();
  }, [fetchProject, fetchAIProviders]);

  const handleUpdateProject = async () => {
    if (!project) return;
    try {
      const response = await fetch(`/api/v1/projects/${project.id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(editForm),
      });

      if (!response.ok) {
        throw new Error('Failed to update project');
      }

      await fetchProject();
      setEditing(false);
      setSuccess('Project updated successfully!');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update project');
    }
  };

  const analyzeRequirements = async () => {
    if (!project) return;
    try {
      setAnalyzing(true);
      setError(null); // Clear any previous errors
      setSuccess(null); // Clear any previous success messages
      
      const response = await fetch(`/api/v1/projects/${project.id}/analyze-requirements`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Failed to analyze requirements');
      }

      const result = await response.json();
      
      if (result.success) {
        // Analysis completed successfully
        await fetchProject();
        setSuccess('Requirements analysis completed successfully!');
      } else {
        // Analysis failed - show the error message with AI guidance
        setError(result.error || 'Requirements analysis failed');
        // Don't refresh the project since analysis didn't complete
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze requirements');
    } finally {
      setAnalyzing(false);
    }
  };

  const generateUXDesign = async () => {
    if (!project) return;
    try {
      setGeneratingUXDesign(true);
      setError(null); // Clear any previous errors
      setSuccess(null); // Clear any previous success messages
      
      const response = await fetch(`/api/v1/projects/${project.id}/generate-ux-design`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Failed to generate UX/UI design');
      }

      const result = await response.json();
      
      if (result.success) {
        // UX/UI design generation completed successfully
        await fetchProject();
        setSuccess('UX/UI design generated successfully!');
      } else {
        // UX/UI design generation failed - show the error message
        setError(result.error || 'UX/UI design generation failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate UX/UI design');
    } finally {
      setGeneratingUXDesign(false);
    }
  };

  const generateSystemArchitecture = async () => {
    if (!project) return;
    try {
      setGeneratingArchitecture(true);
      setError(null); // Clear any previous errors
      setSuccess(null); // Clear any previous success messages
      
      const response = await fetch(`/api/v1/projects/${project.id}/generate-system-architecture`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Failed to generate system architecture');
      }

      const result = await response.json();
      
      if (result.success) {
        // System architecture generation completed successfully
        await fetchProject();
        setSuccess('System architecture generation completed successfully!');
      } else {
        // System architecture generation failed - show the error message
        setError(result.error || 'System architecture generation failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate system architecture');
    } finally {
      setGeneratingArchitecture(false);
    }
  };

  const generateProject = async () => {
    if (!project) return;
    try {
      setGeneratingProject(true);
      setError(null); // Clear any previous errors
      setSuccess(null); // Clear any previous success messages
      
      const response = await fetch(`/api/v1/projects/${project.id}/generate-project`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Failed to generate project');
      }

      const result = await response.json();
      
      if (result.success) {
        // Project generation completed successfully
        setGenerationResult(result);
        setSuccess('Project generated successfully! Check the projects folder for your generated code.');
      } else {
        // Project generation failed - show the error message
        setError(result.error || 'Project generation failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate project');
    } finally {
      setGeneratingProject(false);
    }
  };

  const handleArchiveProject = async (archived: boolean) => {
    if (!project) return;
    try {
      const response = await fetch(`/api/v1/projects/${project.id}/archive`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ archived }),
      });

      if (!response.ok) {
        throw new Error('Failed to update project');
      }

      await fetchProject();
      setSuccess(`Project ${archived ? 'archived' : 'unarchived'} successfully!`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update project');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft':
        return 'default';
      case 'Requirements Complete':
        return 'success';
      case 'Data Model Complete':
        return 'info';
      case 'System Architecture Complete':
        return 'warning';
      case 'Project Generated':
        return 'success';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'Requirements Complete':
        return '✅';
      case 'Data Model Complete':
        return '🗄️';
      case 'System Architecture Complete':
        return '🏗️';
      case 'Project Generated':
        return '🚀';
      default:
        return '📝';
    }
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Typography>Loading project...</Typography>
      </Container>
    );
  }

  if (!project) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Typography color="error">Project not found</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <IconButton onClick={() => navigate('/projects')} sx={{ mr: 2 }}>
          <ArrowBack />
        </IconButton>
        <Box sx={{ flex: 1 }}>
          <Typography variant="h4" component="h1">
            {project.name}
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
            <Chip
              label={project.status}
              color={getStatusColor(project.status) as any}
              icon={<span>{getStatusIcon(project.status)}</span>}
            />
            <Chip
              label={project.ai_provider === 'anthropic' ? 'Claude' : 'ChatGPT'}
              size="small"
              variant="outlined"
            />
          </Box>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={project.archived ? <Unarchive /> : <Archive />}
            onClick={() => handleArchiveProject(!project.archived)}
          >
            {project.archived ? 'UNARCHIVE' : 'ARCHIVE'}
          </Button>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={fetchProject}
          >
            REFRESH
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      {/* Original Requirements Section */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h5" gutterBottom>
            Original Requirements
          </Typography>
          <Button
            size="small"
            startIcon={<Edit />}
            onClick={() => setEditing(true)}
            disabled={aiProviders.length === 0}
          >
            Edit Requirements
          </Button>
        </Box>
        <Paper variant="outlined" sx={{ p: 2, backgroundColor: 'grey.50' }}>
          <Typography variant="body1" component="pre" sx={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
            {project.requirements}
          </Typography>
        </Paper>
      </Paper>

      {/* Three-Panel Layout */}
          <Box sx={{ display: 'flex', gap: 3 }}>
            {/* Left Navigation Panel - 250px */}
            <Paper sx={{ width: 250, flexShrink: 0 }}>
              <List>
                {[
                  {
                    key: 'requirements',
                    label: 'Requirements',
                    icon: <Psychology />,
                    available: true,
                    completed: !!project.refined_requirements
                  },
                  {
                    key: 'architecture',
                    label: 'System Architecture',
                    icon: <span>🏗️</span>,
                    available: !!project.refined_requirements,
                    completed: !!project.system_architecture
                  },
                  {
                    key: 'ux-design',
                    label: 'UX/UI Design',
                    icon: <span>🎨</span>,
                    available: !!project.system_architecture,
                    completed: !!project.ux_design
                  },
                  {
                    key: 'project',
                    label: 'Generate Project',
                    icon: <span>🚀</span>,
                    available: !!project.ux_design,
                    completed: project.status === 'Project Generated'
                  }
                ].map((stage, index) => (
                  <React.Fragment key={stage.key}>
                    <ListItem disablePadding>
                      <ListItemButton
                        onClick={() => setActiveStage(stage.key as any)}
                        disabled={!stage.available}
                        selected={activeStage === stage.key}
                        sx={{
                          '&.Mui-selected': {
                            backgroundColor: 'primary.main',
                            color: 'primary.contrastText',
                            '&:hover': {
                              backgroundColor: 'primary.dark',
                            },
                          },
                        }}
                      >
                        <ListItemIcon sx={{ color: 'inherit' }}>
                          {stage.completed ? (
                            <span style={{ color: 'green' }}>✅</span>
                          ) : (
                            stage.icon
                          )}
                        </ListItemIcon>
                        <ListItemText 
                          primary={stage.label}
                          secondary={stage.completed ? 'Completed' : stage.available ? 'Available' : 'Pending'}
                        />
                      </ListItemButton>
                    </ListItem>
                    {index < 2 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </Paper>

            {/* Right Content Panel */}
            <Box sx={{ flex: 1 }}>
              <Fade in={true} timeout={300}>
                <Paper sx={{ p: 3, minHeight: 400 }}>
                  {/* Requirements Stage */}
                  {activeStage === 'requirements' && (
                    <Grow in={true} timeout={300}>
                      <Box>
                        <Typography variant="h5" gutterBottom>
                          Requirements Analysis
                        </Typography>

                        {/* Refined Requirements */}
                        {project.refined_requirements ? (
                          <Box sx={{ mb: 3 }}>
                            <Typography variant="h6" gutterBottom>
                              Refined Requirements
                            </Typography>
                            <Paper variant="outlined" sx={{ p: 2 }}>
                              <Typography variant="body1" component="pre" sx={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                                {project.refined_requirements}
                              </Typography>
                            </Paper>
                          </Box>
                        ) : (
                          <Alert severity="info" sx={{ mb: 2 }}>
                            No refined requirements yet. Click "Analyze Requirements" to get started.
                          </Alert>
                        )}

                        {/* Action Buttons - Always visible */}
                        <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                          <Button
                            variant="contained"
                            startIcon={<Psychology />}
                            onClick={analyzeRequirements}
                            disabled={analyzing}
                          >
                            {analyzing ? 'Analyzing...' : project.refined_requirements ? 'Re-analyze Requirements' : 'Analyze Requirements'}
                          </Button>
                        </Box>
                      </Box>
                    </Grow>
                  )}



                  {/* Architecture Stage */}
                  {activeStage === 'architecture' && (
                    <Grow in={true} timeout={300}>
                      <Box>
                        <Typography variant="h5" gutterBottom>
                          System Architecture
                        </Typography>
                        
                        {project.system_architecture ? (
                          <Box>
                            <Typography variant="h6" gutterBottom>
                              Architecture Design
                            </Typography>
                            <Paper variant="outlined" sx={{ p: 2 }}>
                              <Typography variant="body1" component="pre" sx={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                                {project.system_architecture}
                              </Typography>
                            </Paper>
                          </Box>
                        ) : (
                          <Box>
                            <Alert severity="info" sx={{ mb: 2 }}>
                              No system architecture generated yet. Complete data modeling first, then generate the system architecture.
                            </Alert>
                          </Box>
                        )}
                        
                        {/* Architecture Button - Always visible if requirements exist */}
                        {project.refined_requirements && (
                          <Box sx={{ mt: 2 }}>
                            <Button
                              variant="contained"
                              color="secondary"
                              startIcon={<span>🏗️</span>}
                              onClick={generateSystemArchitecture}
                              disabled={generatingArchitecture}
                            >
                              {generatingArchitecture ? 'Generating System Architecture...' : project.system_architecture ? 'Regenerate System Architecture' : 'Generate System Architecture'}
                            </Button>
                          </Box>
                        )}
                      </Box>
                    </Grow>
                  )}

                  {/* UX/UI Design Stage */}
                  {activeStage === 'ux-design' && (
                    <Grow in={true} timeout={300}>
                      <Box>
                        <Typography variant="h5" gutterBottom>
                          UX/UI Design
                        </Typography>
                        
                        {project.ux_design ? (
                          <Box>
                            <Alert severity="success" sx={{ mb: 2 }}>
                              🎨 UX/UI Design completed! Your application design is ready.
                            </Alert>
                            <Typography variant="h6" gutterBottom>
                              Design Specifications
                            </Typography>
                            <Paper variant="outlined" sx={{ p: 2 }}>
                              <Typography variant="body1" component="pre" sx={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                                {project.ux_design}
                              </Typography>
                            </Paper>
                          </Box>
                        ) : (
                          <Box>
                            <Alert severity="info" sx={{ mb: 2 }}>
                              Ready to design the user experience and interface! This will create design specifications for your application.
                            </Alert>
                          </Box>
                        )}
                        
                        {/* UX/UI Design Button - Always visible if system architecture exists */}
                        {project.system_architecture && (
                          <Box sx={{ mt: 2 }}>
                            <Button
                              variant="contained"
                              color="primary"
                              startIcon={<span>🎨</span>}
                              onClick={generateUXDesign}
                              disabled={generatingUXDesign}
                            >
                              {generatingUXDesign ? 'Generating Design...' : project.ux_design ? 'Regenerate Design' : 'Generate UX/UI Design'}
                            </Button>
                          </Box>
                        )}
                      </Box>
                    </Grow>
                  )}

                  {/* Project Generation Stage */}
                  {activeStage === 'project' && (
                    <Grow in={true} timeout={300}>
                      <Box>
                        <Typography variant="h5" gutterBottom>
                          Generate Project
                        </Typography>
                        
                        {project.status === 'Project Generated' ? (
                          <Box>
                            {/* Show warnings if any */}
                            {generationResult?.code_generation?.warnings && generationResult.code_generation.warnings.length > 0 && (
                              <Alert severity="warning" sx={{ mb: 2 }}>
                                <Typography variant="subtitle2" gutterBottom>
                                  ⚠️ Generation completed with warnings:
                                </Typography>
                                {generationResult.code_generation.warnings.map((warning: string, index: number) => (
                                  <Typography key={index} variant="body2" component="div">
                                    • {warning}
                                  </Typography>
                                ))}
                              </Alert>
                            )}
                            
                            {/* Show success or warning based on status */}
                            {generationResult?.code_generation?.status === 'Code generation completed with warnings' ? (
                              <Alert severity="warning" sx={{ mb: 2 }}>
                                ⚠️ Project structure created but some components may be missing. Check warnings above.
                              </Alert>
                            ) : generationResult ? (
                              <Alert severity="success" sx={{ mb: 2 }}>
                                🎉 Project generated successfully! Your complete working software is ready.
                              </Alert>
                            ) : (
                              <Alert severity="info" sx={{ mb: 2 }}>
                                ℹ️ Project was previously generated. Click "REGENERATE PROJECT" to see current generation details.
                              </Alert>
                            )}
                            
                            {/* Project Structure Display */}
                            <Typography variant="h6" gutterBottom>
                              📁 Generated Project Structure
                            </Typography>
                            <Paper variant="outlined" sx={{ p: 2, mb: 3 }}>
                              {generationResult?.project_path ? (
                                <Box sx={{ fontFamily: 'monospace', fontSize: '0.9rem' }}>
                                  <Box sx={{ color: 'primary.main', fontWeight: 'bold' }}>
                                    {generationResult.project_path}/
                                  </Box>
                                  <Box sx={{ ml: 2, mt: 1 }}>
                                    {generationResult?.code_generation?.files_created && generationResult.code_generation.files_created.length > 0 ? (
                                      generationResult.code_generation.files_created.map((file: string, index: number) => (
                                        <Box key={index} sx={{ color: 'text.secondary' }}>
                                          {index === generationResult.code_generation.files_created.length - 1 ? '└──' : '├──'} 📄 {file}
                                        </Box>
                                      ))
                                    ) : (
                                      <Box sx={{ color: 'warning.main', fontStyle: 'italic' }}>
                                        ⚠️ No source files were generated. Check warnings above.
                                      </Box>
                                    )}
                                  </Box>
                                </Box>
                              ) : (
                                <Alert severity="error">
                                  ❌ No project path available. Click "REGENERATE PROJECT" to see the actual project structure.
                                </Alert>
                              )}
                            </Paper>

                            {/* Quick Start Instructions */}
                            <Typography variant="h6" gutterBottom>
                              🚀 Quick Start
                            </Typography>
                            <Paper variant="outlined" sx={{ p: 2, mb: 3 }}>
                              {generationResult?.tech_stack?.frontend?.framework === 'Next.js' ? (
                                <>
                                  <Typography variant="body2" component="div" sx={{ mb: 2 }}>
                                    <strong>Next.js Full-Stack Application:</strong>
                                  </Typography>
                                  <Box sx={{ fontFamily: 'monospace', fontSize: '0.85rem', bgcolor: 'grey.50', p: 1, borderRadius: 1, mb: 2 }}>
                                    cd {generationResult.project_path}<br/>
                                    npm install<br/>
                                    npx prisma generate<br/>
                                    npx prisma db push<br/>
                                    npm run dev
                                  </Box>
                                  <Typography variant="body2" color="text.secondary">
                                    This will start the Next.js development server at http://localhost:3000
                                  </Typography>
                                </>
                              ) : generationResult?.tech_stack?.frontend?.framework ? (
                                <>
                                  <Typography variant="body2" component="div" sx={{ mb: 2 }}>
                                    <strong>Backend ({generationResult.tech_stack.backend?.name || 'Unknown'}):</strong>
                                  </Typography>
                                  <Box sx={{ fontFamily: 'monospace', fontSize: '0.85rem', bgcolor: 'grey.50', p: 1, borderRadius: 1, mb: 2 }}>
                                    cd {generationResult.project_path}/backend<br/>
                                    npm install<br/>
                                    cp .env.example .env<br/>
                                    npm run dev
                                  </Box>
                                  
                                  <Typography variant="body2" component="div" sx={{ mb: 2 }}>
                                    <strong>Frontend ({generationResult.tech_stack.frontend.name}):</strong>
                                  </Typography>
                                  <Box sx={{ fontFamily: 'monospace', fontSize: '0.85rem', bgcolor: 'grey.50', p: 1, borderRadius: 1 }}>
                                    cd {generationResult.project_path}/frontend<br/>
                                    npm install<br/>
                                    npm start
                                  </Box>
                                </>
                              ) : (
                                <Alert severity="error">
                                  ❌ No generation data available. Click "REGENERATE PROJECT" to generate the project and see setup instructions.
                                </Alert>
                              )}
                            </Paper>

                            {/* Tech Stack Summary */}
                            <Typography variant="h6" gutterBottom>
                              🛠️ Tech Stack Used
                            </Typography>
                            <Paper variant="outlined" sx={{ p: 2 }}>
                              {generationResult?.tech_stack ? (
                                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                                  {generationResult.tech_stack.frontend?.name && (
                                    <Chip label={generationResult.tech_stack.frontend.name} color="primary" variant="outlined" />
                                  )}
                                  {generationResult.tech_stack.backend?.name && generationResult.tech_stack.backend.name !== "None" && (
                                    <Chip label={generationResult.tech_stack.backend.name} color="primary" variant="outlined" />
                                  )}
                                  {generationResult.tech_stack.database?.name && generationResult.tech_stack.database.name !== "None" && (
                                    <Chip label={generationResult.tech_stack.database.name} color="primary" variant="outlined" />
                                  )}
                                  {generationResult.tech_stack.deployment?.name && (
                                    <Chip label={generationResult.tech_stack.deployment.name} color="primary" variant="outlined" />
                                  )}
                                </Box>
                              ) : (
                                <Alert severity="error">
                                  ❌ No tech stack data available. Click "REGENERATE PROJECT" to see the actual tech stack used.
                                </Alert>
                              )}
                            </Paper>
                          </Box>
                        ) : (
                          <Box>
                            <Alert severity="info" sx={{ mb: 2 }}>
                              Ready to generate your complete working software project! This will create a full application based on your requirements, data model, and system architecture.
                            </Alert>
                          </Box>
                        )}
                        
                        {/* Project Generation Button - Always visible if system architecture exists */}
                        {project.system_architecture && (
                          <Box sx={{ mt: 2 }}>
                            <Button
                              variant="contained"
                              color="primary"
                              startIcon={<span>🚀</span>}
                              onClick={generateProject}
                              disabled={generatingProject}
                            >
                              {generatingProject ? 'Generating Project...' : project.status === 'Project Generated' ? 'Regenerate Project' : 'Generate Project'}
                            </Button>
                          </Box>
                        )}
                      </Box>
                    </Grow>
                  )}
                </Paper>
              </Fade>
            </Box>
         </Box>

          {/* Edit Dialog */}
          {editing && (
            <Dialog open={editing} onClose={() => setEditing(false)} maxWidth="md" fullWidth>
              <DialogTitle>Edit Project</DialogTitle>
              <DialogContent>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 1 }}>
                  <TextField
                    label="Project Name"
                    value={editForm.name}
                    onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                    fullWidth
                  />
                  <TextField
                    label="Description"
                    value={editForm.description}
                    onChange={(e) => setEditForm({ ...editForm, description: e.target.value })}
                    fullWidth
                    multiline
                    rows={2}
                  />
                  <TextField
                    label="Requirements"
                    value={editForm.requirements}
                    onChange={(e) => setEditForm({ ...editForm, requirements: e.target.value })}
                    fullWidth
                    multiline
                    rows={6}
                  />
                  <FormControl fullWidth>
                    <InputLabel>Application Type</InputLabel>
                    <Select
                      value={editForm.application_type}
                      label="Application Type"
                      onChange={(e) => setEditForm({ ...editForm, application_type: e.target.value })}
                    >
                      {APPLICATION_TYPES.map((type) => (
                        <MenuItem key={type.id} value={type.id}>
                          <Box>
                            <Typography variant="body1">{type.name}</Typography>
                            <Typography variant="body2" color="text.secondary">
                              {type.description}
                            </Typography>
                          </Box>
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                  <FormControl fullWidth>
                    <InputLabel>AI Provider</InputLabel>
                    <Select
                      value={editForm.ai_provider}
                      label="AI Provider"
                      onChange={(e) => setEditForm({ ...editForm, ai_provider: e.target.value })}
                    >
                      {aiProviders && aiProviders.length > 0 ? (
                        aiProviders.map((provider) => (
                          <MenuItem key={provider.name} value={provider.name}>
                            {provider.display_name}
                          </MenuItem>
                        ))
                      ) : (
                        <MenuItem value="anthropic">Anthropic Claude</MenuItem>
                      )}
                    </Select>
                  </FormControl>
                </Box>
              </DialogContent>
              <DialogActions>
                <Button onClick={() => setEditing(false)}>Cancel</Button>
                <Button variant="contained" onClick={handleUpdateProject}>
                  Save Changes
                </Button>
              </DialogActions>
            </Dialog>
          )}

          {/* Project Metadata */}
          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Project Information
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Created: {new Date(project.created_at).toLocaleString()}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Last Updated: {new Date(project.updated_at).toLocaleString()}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Status: {project.status}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Archived: {project.archived ? 'Yes' : 'No'}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
    </Container>
  );
};

export default ProjectWorkspace;
