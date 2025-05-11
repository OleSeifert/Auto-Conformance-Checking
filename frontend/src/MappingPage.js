import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  FormHelperText
} from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';

const MappingPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const [headers, setHeaders] = useState([]); 
  const [caseIdCol, setCaseIdCol] = useState('');
  const [activityCol, setActivityCol] = useState('');
  const [timestampCol, setTimestampCol] = useState('');
  const [resourceCol1, setResourceCol1] = useState('');
  const [resourceCol2, setResourceCol2] = useState('');

  useEffect(() => {
    if (location.state?.headers) {
      setHeaders(location.state.headers);
    } else {
      alert('No column headers found. Please upload a file again.');
      navigate('/');
    }
  }, [location.state, navigate]);

  const isValid = caseIdCol && activityCol && timestampCol;

  const handleMappingSubmit = () => {
    if (!isValid) {
      alert('Please fill in all required fields.');
      return;
    }

    localStorage.setItem('caseIdCol', caseIdCol);
    localStorage.setItem('activityCol', activityCol);
    localStorage.setItem('timestampCol', timestampCol);
    localStorage.setItem('resourceCol1', resourceCol1);
    localStorage.setItem('resourceCol2', resourceCol2);

    navigate('/results');
  };

  const renderDropdown = (label, value, setValue, required = true) => (
    <FormControl fullWidth required={required} error={required && !value}>
      <InputLabel>{label}</InputLabel>
      <Select value={value} onChange={(e) => setValue(e.target.value)} label={label}>
        {headers.map((col, idx) => (
          <MenuItem key={idx} value={col}>
            {col}
          </MenuItem>
        ))}
      </Select>
      {required && !value && <FormHelperText>Required</FormHelperText>}
    </FormControl>
  );

  return (
    <Card sx={{ maxWidth: 600, mx: 'auto', mt: 4, boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Map Event Log Columns
        </Typography>

        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {renderDropdown('Case ID Column', caseIdCol, setCaseIdCol)}
          {renderDropdown('Activity Column', activityCol, setActivityCol)}
          {renderDropdown('Timestamp Column', timestampCol, setTimestampCol)}
          {renderDropdown('Resource Column (optional)', resourceCol1, setResourceCol1, false)}
          {renderDropdown('Resource Column (optional)', resourceCol2, setResourceCol2, false)}

          <Button
            variant="contained"
            onClick={handleMappingSubmit}
            disabled={!isValid}
          >
            Confirm Mapping
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default MappingPage;