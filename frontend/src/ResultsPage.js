import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  Divider,
} from '@mui/material';

const ResultsPage = () => {
  const [view, setView] = useState('temporal');

  const renderInsight = () => {
    switch (view) {
      case 'temporal':
        return <Typography>⏱ Temporal Insights Placeholder</Typography>;
      case 'declarative':
        return <Typography>⚖ Declarative Constraints Placeholder</Typography>;
      case 'resource':
        return <Typography>👥 Resource-based Insights Placeholder</Typography>;
      default:
        return null;
    }
  };

  return (
    <Card sx={{ mx: 'auto', mt: 4, maxWidth: 900, boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Conformance Insights
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, my: 2 }}>
          <Button
            variant={view === 'temporal' ? 'contained' : 'outlined'}
            onClick={() => setView('temporal')}
          >
            Temporal
          </Button>
          <Button
            variant={view === 'declarative' ? 'contained' : 'outlined'}
            onClick={() => setView('declarative')}
          >
            Declarative
          </Button>
          <Button
            variant={view === 'resource' ? 'contained' : 'outlined'}
            onClick={() => setView('resource')}
          >
            Resource
          </Button>
        </Box>
        <Divider />
        <Box sx={{ mt: 3 }}>{renderInsight()}</Box>
      </CardContent>
    </Card>
  );
};

export default ResultsPage;