import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';

const Header: React.FC = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Box display="flex" alignItems="center">
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            BMAD Pipeline MVP
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
