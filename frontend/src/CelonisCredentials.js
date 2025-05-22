import React, { useState } from 'react';
import { API_BASE} from "./config";
import {
  Box, Button, Card, CardContent, TextField, Typography, FormHelperText
} from '@mui/material';

const CelonisCredentials = () => {
  const [apiUrl, setApiUrl] = useState('');
  const [token, setToken] = useState('');
  const [dataPoolName, setDataPoolName] = useState('');
  const [dataModelName, setDataModelName] = useState('');
  const [dataTableName, setDataTableName] = useState('');

  const handleSubmit = async () => {
    const payload = {
      api_url: apiUrl,
      api_token: token,
      data_pool_name: dataPoolName,
      data_model_name: dataModelName,
      data_table_name: dataTableName || 'ACTIVITIES'
    };

    try {
      const res = await fetch(`${API_BASE}/celonis-connection`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('Connection failed');
      alert('Celonis connection saved!');
    } catch (err) {
      alert('Error connecting to backend: ' + err.message);
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
          <Box>
            <TextField label="Data Table Name (optional)" fullWidth value={dataTableName} onChange={e => setDataTableName(e.target.value)} />
            <FormHelperText>Defaults to <strong>ACTIVITIES</strong></FormHelperText>
          </Box>
          <Button variant="contained" onClick={handleSubmit}>Submit</Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default CelonisCredentials;