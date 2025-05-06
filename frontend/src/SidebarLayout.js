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

const drawerWidth = 220;

const SidebarLayout = ({ children }) => {
  const navigate = useNavigate();

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position="fixed"
        sx={{
          zIndex: 1201,
          background: 'linear-gradient(to right, #6a11cb, #2575fc)',
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
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
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