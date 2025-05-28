import React, { useState } from 'react';
import { CELONIS_LOG_UPLOAD, GET_COLUMN_NAMES } from './config';
import {
  Box, Button, Card, CardContent, Typography, InputLabel
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const navigate = useNavigate();
  const handleUpload = async () => {
  if (!file) {
    alert("Please select a file.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${CELONIS_LOG_UPLOAD}`, {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const error = await res.text();
      throw new Error(error);
    }

    const colRes = await fetch(`${GET_COLUMN_NAMES}`);
      if (!colRes.ok) {
        throw new Error("Failed to fetch column names");
      }

      const result = await colRes.json(); 
    console.log("Extracted columns from backend:", result.columns);
    alert("File uploaded and processed!");

    // Check if the file is .xes or .csv
    const fileType = file.name.endsWith(".xes") ? "xes" : "csv";

      navigate("/mapping", {
        state: {
          columns: result.columns,
          fileType: fileType,
        }
      });
  } catch (err) {
    alert("Error uploading file: " + err.message);
  }
};

  return (
    <Card sx={{ maxWidth: 600, mx: 'auto', mt: 4, boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Upload Event Log
        </Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <InputLabel>Upload .csv or .xes File</InputLabel>
          <input type="file" accept=".csv,.xes" onChange={e => setFile(e.target.files[0])} />
          <Button variant="contained" onClick={handleUpload}>Submit</Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default UploadPage;