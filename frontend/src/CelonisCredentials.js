import React, { useState } from 'react';
import { CELONIS_CONNECTION } from "./config";
import { useNavigate } from 'react-router-dom';
import {
  Box, Button, Card, CardContent, TextField, Typography, FormHelperText
} from '@mui/material';

const CelonisCredentials = () => {
  const [apiUrl, setApiUrl] = useState('');
  const [token, setToken] = useState('');
  const [dataPoolName, setDataPoolName] = useState('');
  const [dataModelName, setDataModelName] = useState('');
  // const [dataTableName, setDataTableName] = useState('');
  const navigate = useNavigate();
  const handleSubmit = async () => {
  const payload = {
    celonis_base_url: apiUrl,
    celonis_data_pool_name: dataPoolName,
    celonis_data_model_name: dataModelName,
    api_token: token,
    // data_table_name: dataTableName.trim() === "" ? "ACTIVITIES" : dataTableName
  };

  try {
    const res = await fetch(`${CELONIS_CONNECTION}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      let backendMessage = "Unknown error";
      try {
        const errorData = await res.json();
        backendMessage = errorData.message || JSON.stringify(errorData);
      } catch (e) {
        backendMessage = await res.text(); // fallback
      }

      throw new Error(backendMessage);
    }

    alert('Celonis connection saved!');
    navigate('/upload');
  } catch (err) {
    alert('Error connecting to backend: ' + err.message);
    console.error("Full error:", err);
  }
};
  return (
    <Card sx={{ maxWidth: 600, mx: 'auto', mt: 4, boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Celonis Credentials
        </Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField label="Celonis API URL" fullWidth value={apiUrl} onChange={e => setApiUrl(e.target.value)} />
          <TextField label="Celonis API Token" fullWidth type="password" value={token} onChange={e => setToken(e.target.value)} />
          <TextField label="Data Pool Name" fullWidth value={dataPoolName} onChange={e => setDataPoolName(e.target.value)} />
          <TextField label="Data Model Name" fullWidth value={dataModelName} onChange={e => setDataModelName(e.target.value)} />
          {/* <Box>
            <TextField label="Data Table Name (optional)" fullWidth value={dataTableName} onChange={e => setDataTableName(e.target.value)} />
            <FormHelperText>Defaults to <strong>ACTIVITIES</strong></FormHelperText>
          </Box> */}
          <Button variant="contained" onClick={handleSubmit} disabled={
              !apiUrl.trim() ||
              !token.trim() ||
              !dataPoolName.trim() ||
              !dataModelName.trim()
              }>Submit</Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default CelonisCredentials;