import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  TextField,
  Typography,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

const MappingPage = () => {
  const [caseIdCol, setCaseIdCol] = useState('');
  const [activityCol, setActivityCol] = useState('');
  const [timestampCol, setTimestampCol] = useState('');
  const navigate = useNavigate();

  const handleMappingSubmit = () => {
    localStorage.setItem('caseIdCol', caseIdCol);
    localStorage.setItem('activityCol', activityCol);
    localStorage.setItem('timestampCol', timestampCol);
    navigate('/results');
  };

  return (
    <Card sx={{ maxWidth: 600, mx: 'auto', mt: 4, boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Map Event Log Columns
        </Typography>

        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Case ID Column"
            fullWidth
            value={caseIdCol}
            onChange={(e) => setCaseIdCol(e.target.value)}
          />
          <TextField
            label="Activity Column"
            fullWidth
            value={activityCol}
            onChange={(e) => setActivityCol(e.target.value)}
          />
          <TextField
            label="Timestamp Column"
            fullWidth
            value={timestampCol}
            onChange={(e) => setTimestampCol(e.target.value)}
          />
          <Button variant="contained" onClick={handleMappingSubmit}>
            Confirm Mapping
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default MappingPage;