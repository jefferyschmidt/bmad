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
  const [generatingDataModel, setGeneratingDataModel] = useState(false);
  const [generatingArchitecture, setGeneratingArchitecture] = useState(false);
  const [editForm, setEditForm] = useState({
    name: '',
    description: '',
    requirements: '',
    ai_provider: ''
  });
  const [activeStage, setActiveStage] = useState('requirements'); // 'requirements', 'data-model', 'architecture'

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
        ai_provider: data.ai_provider
      });
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

  const generateDataModel = async () => {
    if (!project) return;
    try {
      setGeneratingDataModel(true);
      setError(null); // Clear any previous errors
      setSuccess(null); // Clear any previous success messages
      
      const response = await fetch(`/api/v1/projects/${project.id}/generate-data-model`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Failed to generate data model');
      }

      const result = await response.json();
      
      if (result.success) {
        // Data model generation completed successfully
        await fetchProject();
        setSuccess('Data model generation completed successfully!');
      } else {
        // Data model generation failed - show the error message
        setError(result.error || 'Data model generation failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate data model');
    } finally {
      setGeneratingDataModel(false);
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
                    key: 'data-model',
                    label: 'Data Model',
                    icon: <span>🗄️</span>,
                    available: !!project.refined_requirements,
                    completed: !!project.data_model
                  },
                  {
                    key: 'architecture',
                    label: 'System Architecture',
                    icon: <span>🏗️</span>,
                    available: !!project.data_model,
                    completed: !!project.system_architecture
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

                  {/* Data Model Stage */}
                  {activeStage === 'data-model' && (
                    <Grow in={true} timeout={300}>
                      <Box>
                        <Typography variant="h5" gutterBottom>
                          Data Model
                        </Typography>
                        
                        {project.data_model ? (
                          <Box>
                            <Typography variant="h6" gutterBottom>
                              Database Schema
                            </Typography>
                            <Paper variant="outlined" sx={{ p: 2 }}>
                              <Typography variant="body1" component="pre" sx={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                                {project.data_model}
                              </Typography>
                            </Paper>
                          </Box>
                        ) : (
                          <Box>
                            <Alert severity="info" sx={{ mb: 2 }}>
                              No data model generated yet. Complete requirements analysis first, then click "Generate Data Model".
                            </Alert>
                          </Box>
                        )}
                        
                        {/* Data Model Button - Always visible if requirements exist */}
                        {project.refined_requirements && (
                          <Box sx={{ mt: 2 }}>
                            <Button
                              variant="contained"
                              color="secondary"
                              startIcon={<span>🗄️</span>}
                              onClick={generateDataModel}
                              disabled={generatingDataModel}
                            >
                              {generatingDataModel ? 'Generating Data Model...' : project.data_model ? 'Regenerate Data Model' : 'Generate Data Model'}
                            </Button>
                          </Box>
                        )}
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
                        
                        {/* Architecture Button - Always visible if data model exists */}
                        {project.data_model && (
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
