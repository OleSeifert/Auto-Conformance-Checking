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
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const handleUpload = () => {
    if (!apiUrl || !token || !file) {
      alert('All fields are required.');
      return;
    }
    localStorage.setItem('apiUrl', apiUrl);
    localStorage.setItem('token', token);
    localStorage.setItem('filename', file.name);
    navigate('/mapping');
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
          <InputLabel>Upload .csv or .xes File</InputLabel>
          <input
            type="file"
            accept=".csv,.xes"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <Button variant="contained" onClick={handleUpload}>
            Proceed to Mapping
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default UploadPage;