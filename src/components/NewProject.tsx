import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Typography,
  FormHelperText
} from '@mui/material';
import { Project, AIProvider } from '../types/project';
import { APPLICATION_TYPES, ApplicationType, TechStack } from '../constants/applicationTypes';

interface NewProjectProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (project: Omit<Project, 'id' | 'created_at' | 'updated_at' | 'status' | 'archived' | 'refined_requirements' | 'user_stories' | 'data_model' | 'system_architecture' | 'tech_stack_id'>) => void;
  aiProviders: AIProvider[];
}

const NewProject: React.FC<NewProjectProps> = ({ open, onClose, onSubmit, aiProviders }) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [requirements, setRequirements] = useState('');
  const [applicationType, setApplicationType] = useState('');
  const [aiProvider, setAiProvider] = useState('anthropic');

  // Helper functions
  const getSelectedApplicationType = (): ApplicationType | undefined => {
    return APPLICATION_TYPES.find(type => type.id === applicationType);
  };

  const handleSubmit = () => {
    if (!name.trim() || !requirements.trim() || !applicationType) {
      return;
    }

    onSubmit({
      name: name.trim(),
      description: description.trim(),
      requirements: requirements.trim(),
      application_type: applicationType,
      ai_provider: aiProvider
    });

    // Reset form
    setName('');
    setDescription('');
    setRequirements('');
    setApplicationType('');
    setAiProvider('anthropic');
    onClose();
  };

  const handleClose = () => {
    // Reset form
    setName('');
    setDescription('');
    setRequirements('');
    setApplicationType('');
    setAiProvider('anthropic');
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle>Create New Project</DialogTitle>
      <DialogContent>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
          <TextField
            label="Project Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            fullWidth
            required
            placeholder="Enter project name"
          />
          
          <TextField
            label="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            fullWidth
            multiline
            rows={2}
            placeholder="Brief description of the project"
          />
          
          <TextField
            label="Requirements"
            value={requirements}
            onChange={(e) => setRequirements(e.target.value)}
            fullWidth
            multiline
            rows={6}
            required
            placeholder="Describe what you want to build. Be as detailed as possible about the problem you're trying to solve, the users, and the desired functionality."
            helperText="The AI Requirements Analyst will analyze these requirements and generate refined specifications and user stories."
          />
          
          <FormControl fullWidth required>
            <InputLabel>Application Type</InputLabel>
            <Select
              value={applicationType}
              label="Application Type"
              onChange={(e) => setApplicationType(e.target.value)}
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
            <FormHelperText>
              Choose the type of application you want to build. The AI will select the best technology stack for your requirements.
            </FormHelperText>
          </FormControl>
          
          <FormControl fullWidth>
            <InputLabel>AI Provider</InputLabel>
            <Select
              value={aiProvider}
              label="AI Provider"
              onChange={(e) => setAiProvider(e.target.value)}
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
          
          <Typography variant="body2" color="text.secondary">
            Choose which AI service will analyze your requirements. Each provider has different strengths and may produce slightly different results.
          </Typography>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Cancel</Button>
        <Button 
          onClick={handleSubmit} 
          variant="contained" 
          disabled={!name.trim() || !requirements.trim() || !applicationType}
        >
          Create Project
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default NewProject;
