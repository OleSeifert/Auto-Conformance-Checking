// import React, { useState } from 'react';
// import {
//   Box,
//   Button,
//   Card,
//   CardContent,
//   TextField,
//   Typography,
//   InputLabel,
//   FormHelperText,
// } from '@mui/material';
// import { useNavigate } from 'react-router-dom';
//
// const UploadPage = () => {
//   const [apiUrl, setApiUrl] = useState('');
//   const [token, setToken] = useState('');
//   const [dataPoolName, setDataPoolName] = useState('');
//   const [dataModelName, setDataModelName] = useState('');
//   const [dataTableName, setDataTableName] = useState('');
//   const [file, setFile] = useState(null);
//   const navigate = useNavigate();
//
//   const extractCSVHeaders = async (file) => {
//     const text = await file.text();
//     const firstLine = text.split(/\r?\n/)[0];
//     return firstLine.split(';').map((h) => h.trim());
//   };
//
//   const extractXESAttributes = async (file) => {
//     const text = await file.text();
//     const matches = text.match(/<string key=\"(.*?)\"/g) || [];
//     const uniqueAttrs = [...new Set(matches.map((m) => m.match(/key="(.*?)"/)?.[1]))];
//     return uniqueAttrs;
//   };
//
//   const handleUpload = async () => {
//     if (!apiUrl || !token || !dataPoolName || !dataModelName || !file) {
//       alert('Please fill in all required fields.');
//       return;
//     }
//
//     localStorage.setItem('apiUrl', apiUrl);
//     localStorage.setItem('token', token);
//     localStorage.setItem('dataPoolName', dataPoolName);
//     localStorage.setItem('dataModelName', dataModelName);
//     localStorage.setItem('dataTableName', dataTableName || 'ACTIVITIES');
//     localStorage.setItem('filename', file.name);
//
//     const fileExtension = file.name.split('.').pop().toLowerCase();
//
//     let headers = [];
//     if (fileExtension === 'csv') {
//       headers = await extractCSVHeaders(file);
//       navigate('/mapping', {
//         state: { headers, file } // pass file and headers
//       });
//     } else if (fileExtension === 'xes') {
//       headers = await extractXESAttributes(file);
//       navigate('/results', {
//         state: {
//           headers,
//           file,
//           analysis_type: 'xes'
//         }
//       });
//     } else {
//       alert('Unsupported file type. Please upload a .csv or .xes file.');
//     }
//   };
//
//   return (
//     <Card sx={{ maxWidth: 600, mx: 'auto', mt: 4, boxShadow: 3 }}>
//       <CardContent>
//         <Typography variant="h5" gutterBottom>
//           Upload Your Event Log
//         </Typography>
//
//         <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
//           <TextField
//             label="Celonis API URL"
//             fullWidth
//             value={apiUrl}
//             onChange={(e) => setApiUrl(e.target.value)}
//           />
//           <TextField
//             label="Celonis API Token"
//             fullWidth
//             type="password"
//             value={token}
//             onChange={(e) => setToken(e.target.value)}
//           />
//           <TextField
//             label="Data Pool Name"
//             fullWidth
//             value={dataPoolName}
//             onChange={(e) => setDataPoolName(e.target.value)}
//           />
//           <TextField
//             label="Data Model Name"
//             fullWidth
//             value={dataModelName}
//             onChange={(e) => setDataModelName(e.target.value)}
//           />
//           <Box>
//             <TextField
//               label="Data Table Name (optional)"
//               fullWidth
//               value={dataTableName}
//               onChange={(e) => setDataTableName(e.target.value)}
//             />
//             <FormHelperText>
//               Leave blank to use the default name: <strong>Activity Table</strong>
//             </FormHelperText>
//           </Box>
//           <InputLabel>Upload .csv or .xes File</InputLabel>
//           <input
//             type="file"
//             accept=".csv,.xes"
//             onChange={(e) => setFile(e.target.files[0])}
//           />
//           <Button variant="contained" onClick={handleUpload}>
//             Proceed
//           </Button>
//         </Box>
//       </CardContent>
//     </Card>
//   );
// };
//
// export default UploadPage;

import React, { useState } from 'react';
import {
  Box, Button, Card, CardContent, Typography, InputLabel
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const handleUpload = async () => {
    if (!file) return alert("Please select a file first.");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch('http://localhost:8000/analyse', {
        method: 'POST',
        body: formData
      });

      const result = await res.json();
      navigate('/mapping', { state: { headers: result.headers, file } });
    } catch (err) {
      alert('Failed to upload file: ' + err.message);
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