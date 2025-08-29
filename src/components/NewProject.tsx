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
  Typography
} from '@mui/material';
import { Project, AIProvider } from '../types/project';

interface NewProjectProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (project: Omit<Project, 'id' | 'created_at' | 'updated_at' | 'status' | 'archived' | 'refined_requirements' | 'user_stories' | 'data_model' | 'system_architecture'>) => void;
  aiProviders: AIProvider[];
}

const NewProject: React.FC<NewProjectProps> = ({ open, onClose, onSubmit, aiProviders }) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [requirements, setRequirements] = useState('');
  const [aiProvider, setAiProvider] = useState('anthropic');

  const handleSubmit = () => {
    if (!name.trim() || !requirements.trim()) {
      return;
    }

    onSubmit({
      name: name.trim(),
      description: description.trim(),
      requirements: requirements.trim(),
      ai_provider: aiProvider
    });

    // Reset form
    setName('');
    setDescription('');
    setRequirements('');
    setAiProvider('anthropic');
    onClose();
  };

  const handleClose = () => {
    // Reset form
    setName('');
    setDescription('');
    setRequirements('');
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
          disabled={!name.trim() || !requirements.trim()}
        >
          Create Project
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default NewProject;
