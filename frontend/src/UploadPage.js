import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  TextField,
  Typography,
  InputLabel,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

const UploadPage = () => {
  const [apiUrl, setApiUrl] = useState('');
  const [token, setToken] = useState('');
  const [poolName, setPoolName] = useState('');
  const [logName, setLogName] = useState('');
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const extractCSVHeaders = async (file) => {
    const text = await file.text();
    const firstLine = text.split(/\r?\n/)[0];
    return firstLine.split(';').map((h) => h.trim()); //depends on the csv
  };

  const extractXESAttributes = async (file) => {
    const text = await file.text();
    const matches = text.match(/<string key=\"(.*?)\"/g) || [];
    const uniqueAttrs = [...new Set(matches.map((m) => m.match(/key="(.*?)"/)?.[1]))];
    return uniqueAttrs;
  };

  const handleUpload = async () => {
    if (!apiUrl || !token || !poolName || !logName || !file) {
      alert('All fields are required.');
      return;
    }

    const fileExtension = file.name.split('.').pop().toLowerCase();

    localStorage.setItem('apiUrl', apiUrl);
    localStorage.setItem('token', token);
    localStorage.setItem('poolName', poolName);
    localStorage.setItem('logName', logName);
    localStorage.setItem('filename', file.name);

    let headers = [];
    if (fileExtension === 'csv') {
      headers = await extractCSVHeaders(file);
      navigate('/mapping', { state: { headers } });
    } else if (fileExtension === 'xes') {
      headers = await extractXESAttributes(file);
      navigate('/results', { state: { headers } });
    } else {
      alert('Unsupported file type. Please upload a .csv or .xes file.');
    }
  };

  return (
    <Card sx={{ maxWidth: 600, mx: 'auto', mt: 4, boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Upload Your Event Log
        </Typography>

        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Celonis API URL"
            fullWidth
            value={apiUrl}
            onChange={(e) => setApiUrl(e.target.value)}
          />
          <TextField
            label="Celonis API Token"
            fullWidth
            type="password"
            value={token}
            onChange={(e) => setToken(e.target.value)}
          />
          <TextField
            label="Pool Name"
            fullWidth
            value={poolName}
            onChange={(e) => setPoolName(e.target.value)}
          />
          <TextField
            label="Log/Table Name"
            fullWidth
            value={logName}
            onChange={(e) => setLogName(e.target.value)}
          />
          <InputLabel>Upload .csv or .xes File</InputLabel>
          <input
            type="file"
            accept=".csv,.xes"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <Button variant="contained" onClick={handleUpload}>
            Proceed
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default UploadPage;