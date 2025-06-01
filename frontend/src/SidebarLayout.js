import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Drawer,
  List,
  ListItem,
  ListItemText,
  Box,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { keyframes } from '@emotion/react';

// Drawer width
const drawerWidth = 220;

// Animate background-position to simulate flowing gradient
const flowingGradient = keyframes`
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
`;

// Shared gradient with flowing effect
const sharedGradientStyle = {
  background: 'linear-gradient(270deg, #6a11cb, #2575fc, #3a0e80, #2575fc)',
  backgroundSize: '600% 600%',
  animation: `${flowingGradient} 20s ease-in-out infinite`,
  color: '#fff',
};

const SidebarLayout = ({ children }) => {
  const navigate = useNavigate();

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position="fixed"
        sx={{
          zIndex: 1201,
          ...sharedGradientStyle,
        }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap>
            🚀 ConfInsights
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: 'border-box',
            ...sharedGradientStyle,
          },
        }}
      >
        <Toolbar />
        <List>
          <ListItem button onClick={() => navigate('/')}>
            <ListItemText primary="Upload Log" />
          </ListItem>
          <ListItem button onClick={() => navigate('/mapping')}>
            <ListItemText primary="Map Columns" />
          </ListItem>
          <ListItem button onClick={() => navigate('/results')}>
            <ListItemText primary="Conformance Insights" />
          </ListItem>
        </List>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, p: 3, ml: `${drawerWidth}px` }}>
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};

export default SidebarLayout;