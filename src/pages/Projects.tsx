import React, { useState, useEffect, useCallback } from 'react';
import {
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  Box,
  Chip,
  IconButton,
  Switch,
  FormControlLabel,
  Alert
} from '@mui/material';
import { Add, Visibility } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import NewProject from '../components/NewProject';
import { Project, AIProvider } from '../types/project';

const Projects: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [aiProviders, setAiProviders] = useState<AIProvider[]>([]);
  const [showNewProject, setShowNewProject] = useState(false);
  const [showArchived, setShowArchived] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const fetchProjects = useCallback(async () => {
    try {
      const response = await fetch('/api/v1/projects');
      if (!response.ok) {
        throw new Error('Failed to fetch projects');
      }
      const data = await response.json();
      setProjects(data.projects);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch projects');
    } finally {
      setLoading(false);
    }
  }, []);

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
    fetchProjects();
    fetchAIProviders();
  }, [fetchProjects, fetchAIProviders]);

  const handleCreateProject = async (projectData: Omit<Project, 'id' | 'created_at' | 'updated_at' | 'status' | 'archived' | 'refined_requirements' | 'user_stories' | 'data_model' | 'system_architecture'>) => {
    try {
      const response = await fetch('/api/v1/projects', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(projectData),
      });

      if (!response.ok) {
        throw new Error('Failed to create project');
      }

      await fetchProjects();
      setShowNewProject(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create project');
    }
  };



  const filteredProjects = projects.filter(project => 
    showArchived ? project.archived : !project.archived
  );

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
        <Typography>Loading projects...</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Projects
        </Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => setShowNewProject(true)}
          disabled={aiProviders.length === 0}
        >
          New Project
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Box sx={{ mb: 3 }}>
        <FormControlLabel
          control={
            <Switch
              checked={showArchived}
              onChange={(e) => setShowArchived(e.target.checked)}
            />
          }
          label="Show Archived Projects"
        />
      </Box>

      <Grid container spacing={3}>
        {filteredProjects.map((project) => (
          <Grid item xs={12} sm={6} md={4} key={project.id}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ flex: 1, pb: 1 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1.5 }}>
                  <Typography variant="h6" component="h2" sx={{ flex: 1, lineHeight: 1.2 }}>
                    {project.name}
                  </Typography>
                  <Chip
                    label={project.status}
                    color={getStatusColor(project.status) as any}
                    size="small"
                    icon={<span>{getStatusIcon(project.status)}</span>}
                  />
                </Box>
                
                {project.description && (
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1.5, lineHeight: 1.4 }}>
                    {project.description}
                  </Typography>
                )}
                
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1.5 }}>
                  <Typography variant="caption" color="text.secondary">
                    Created: {new Date(project.created_at).toLocaleDateString()}
                  </Typography>
                  <Chip
                    label={project.ai_provider === 'anthropic' ? 'Claude' : 'ChatGPT'}
                    size="small"
                    variant="outlined"
                    sx={{ fontSize: '0.7rem' }}
                  />
                </Box>
              </CardContent>
              
              <CardActions>
                <Button
                  variant="contained"
                  size="small"
                  onClick={() => navigate(`/projects/${project.id}`)}
                  startIcon={<Visibility />}
                  sx={{ flex: 1 }}
                >
                  View Details
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {filteredProjects.length === 0 && (
        <Box sx={{ textAlign: 'center', mt: 4 }}>
          <Typography variant="h6" color="text.secondary">
            {showArchived ? 'No archived projects' : 'No projects yet'}
          </Typography>
          {!showArchived && (
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={() => setShowNewProject(true)}
              sx={{ mt: 2 }}
            >
              Create Your First Project
            </Button>
          )}
        </Box>
      )}

      <NewProject
        open={showNewProject}
        onClose={() => setShowNewProject(false)}
        onSubmit={handleCreateProject}
        aiProviders={aiProviders}
      />
    </Container>
  );
};

export default Projects;
