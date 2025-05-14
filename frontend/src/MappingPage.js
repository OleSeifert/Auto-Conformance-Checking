import React, { useState } from 'react';
import {
  Box, Button, Card, CardContent, Typography,
  FormControl, InputLabel, MenuItem, Select, FormHelperText
} from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';

const MappingPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const headers = location.state?.headers || [];
  const uploadedFile = location.state?.file || null;

  const [caseIdCol, setCaseIdCol] = useState('');
  const [activityCol, setActivityCol] = useState('');
  const [timestampCol, setTimestampCol] = useState('');
  const [resourceCol1, setResourceCol1] = useState('');
  const [resourceCol2, setResourceCol2] = useState('');

  const isValid = caseIdCol && activityCol && timestampCol;

  const handleSubmit = async () => {
    if (!isValid) {
      alert('Please fill in all required fields');
      return;
    }

    if (!uploadedFile) {
      alert('No uploaded file found. Please re-upload.');
      return;
    }

    const formData = new FormData();
    formData.append("file", uploadedFile);

    const metadata = {
      api_url: localStorage.getItem("apiUrl"),
      api_token: localStorage.getItem("token"),
      data_pool_name: localStorage.getItem("dataPoolName"),
      data_model_name: localStorage.getItem("dataModelName"),
      data_table_name: localStorage.getItem("dataTableName") || "Activity Table",
      case_id_col: caseIdCol,
      activity_col: activityCol,
      timestamp_col: timestampCol,
      resource_col1: resourceCol1,
      resource_col2: resourceCol2
    };

    formData.append("metadata", JSON.stringify(metadata));

    const res = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      body: formData
    });

    const result = await res.json();
    navigate('/results', { state: result });
  };

  const renderDropdown = (label, value, setter, required = true) => (
    <FormControl fullWidth required={required} error={required && !value}>
      <InputLabel>{label}</InputLabel>
      <Select value={value} onChange={(e) => setter(e.target.value)} label={label}>
        {headers.map((h, i) => <MenuItem key={i} value={h}>{h}</MenuItem>)}
      </Select>
      {required && !value && <FormHelperText>Required</FormHelperText>}
    </FormControl>
  );

  return (
    <Card sx={{ maxWidth: 600, mx: 'auto', mt: 4 }}>
      <CardContent>
        <Typography variant="h5">Map Columns</Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
          {renderDropdown("Case ID Column", caseIdCol, setCaseIdCol)}
          {renderDropdown("Activity Column", activityCol, setActivityCol)}
          {renderDropdown("Timestamp Column", timestampCol, setTimestampCol)}
          {renderDropdown("Resource Column (optional)", resourceCol1, setResourceCol1, false)}
          {renderDropdown("Resource 2 Column (optional)", resourceCol2, setResourceCol2, false)}
          <Button variant="contained" onClick={handleSubmit} disabled={!isValid}>
            Confirm Mapping
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default MappingPage;