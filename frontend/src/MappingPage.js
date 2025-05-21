// import React, { useState } from 'react';
// import { API_BASE} from "./config";
// import {
//   Box, Button, Card, CardContent, Typography,
//   FormControl, InputLabel, MenuItem, Select, FormHelperText
// } from '@mui/material';
// import { useLocation, useNavigate } from 'react-router-dom';
//
// const MappingPage = () => {
//   const location = useLocation();
//   const navigate = useNavigate();
//
//   const headers = location.state?.headers || [];
//   const uploadedFile = location.state?.file || null;
//
//   const [caseIdCol, setCaseIdCol] = useState('');
//   const [activityCol, setActivityCol] = useState('');
//   const [timestampCol, setTimestampCol] = useState('');
//   const [resourceCol1, setResourceCol1] = useState('');
//   const [resourceCol2, setResourceCol2] = useState('');
//
//   const isValid = caseIdCol && activityCol && timestampCol;
//
//   const handleSubmit = async () => {
//     if (!isValid) {
//       alert('Please fill in all required fields');
//       return;
//     }
//
//     if (!uploadedFile) {
//       alert('No uploaded file found. Please re-upload.');
//       return;
//     }
//
//     const formData = new FormData();
//     formData.append("file", uploadedFile);
//
//     const metadata = {
//       api_url: localStorage.getItem("apiUrl"),
//       api_token: localStorage.getItem("token"),
//       data_pool_name: localStorage.getItem("dataPoolName"),
//       data_model_name: localStorage.getItem("dataModelName"),
//       data_table_name: localStorage.getItem("dataTableName") || "Activity Table",
//       case_id_col: caseIdCol,
//       activity_col: activityCol,
//       timestamp_col: timestampCol,
//       resource_col1: resourceCol1,
//       resource_col2: resourceCol2
//     };
//
//     formData.append("metadata", JSON.stringify(metadata));
//
//     const res = await fetch(`${API_BASE}/analyze`, {
//       method: "POST",
//       body: formData
//     });
//
//     const result = await res.json();
//     navigate('/results', { state: result });
//   };
//
//   const renderDropdown = (label, value, setter, required = true) => (
//     <FormControl fullWidth required={required} error={required && !value}>
//       <InputLabel>{label}</InputLabel>
//       <Select value={value} onChange={(e) => setter(e.target.value)} label={label}>
//         {headers.map((h, i) => <MenuItem key={i} value={h}>{h}</MenuItem>)}
//       </Select>
//       {required && !value && <FormHelperText>Required</FormHelperText>}
//     </FormControl>
//   );
//
//   return (
//     <Card sx={{ maxWidth: 600, mx: 'auto', mt: 4 }}>
//       <CardContent>
//         <Typography variant="h5">Map Columns</Typography>
//         <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
//           {renderDropdown("Case ID Column", caseIdCol, setCaseIdCol)}
//           {renderDropdown("Activity Column", activityCol, setActivityCol)}
//           {renderDropdown("Timestamp Column", timestampCol, setTimestampCol)}
//           {renderDropdown("Resource Column (optional)", resourceCol1, setResourceCol1, false)}
//           {renderDropdown("Resource 2 Column (optional)", resourceCol2, setResourceCol2, false)}
//           <Button variant="contained" onClick={handleSubmit} disabled={!isValid}>
//             Confirm Mapping
//           </Button>
//         </Box>
//       </CardContent>
//     </Card>
//   );
// };
//
// export default MappingPage;

import React, { useState, useEffect } from 'react';
import {
  Box, Button, Card, CardContent, Typography,
  FormControl, InputLabel, MenuItem, Select, FormHelperText
} from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';
import { API_BASE } from './config';

const MappingPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const file = location.state?.file || null;
  const fileType = location.state?.fileType || 'csv'; // 'csv' or 'xes'
  const [columns, setColumns] = useState([]);

  // Mapping values
  const [caseIdCol, setCaseIdCol] = useState('');
  const [activityCol, setActivityCol] = useState('');
  const [timestampCol, setTimestampCol] = useState('');
  const [resourceCol1, setResourceCol1] = useState('');
  const [resourceCol2, setResourceCol2] = useState('');

  const isXES = fileType === 'xes';

  useEffect(() => {
    const fetchColumns = async () => {
      try {
        const res = await fetch(`${API_BASE}/get-columns`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ fileType })  // optional payload
        });
        const result = await res.json();
        setColumns(result.columns || []);

        // Pre-fill and disable case/activity/timestamp for XES
        if (isXES) {
          setCaseIdCol(result.default_case_id);
          setActivityCol(result.default_activity);
          setTimestampCol(result.default_timestamp);
        }
      } catch (err) {
        alert('Failed to fetch column names');
      }
    };

    fetchColumns();
  }, [fileType]);

  const handleSubmit = async () => {
    const payload = {
      case_id_col: caseIdCol,
      activity_col: activityCol,
      timestamp_col: timestampCol,
      resource_col1: resourceCol1,
      resource_col2: resourceCol2,
      file_type: fileType
    };

    try {
      const res = await fetch(`${API_BASE}/mapping-columns`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const result = await res.json();
      navigate('/results', { state: result });
    } catch (err) {
      alert('Failed to send mappings: ' + err.message);
    }
  };

  const renderDropdown = (label, value, setter, disabled = false, required = true) => (
    <FormControl fullWidth required={required} error={required && !value} disabled={disabled}>
      <InputLabel>{label}</InputLabel>
      <Select value={value} onChange={(e) => setter(e.target.value)} label={label}>
        {columns.map((col, i) => (
          <MenuItem key={i} value={col}>
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
        <Typography variant="h5">Map Columns</Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
          {renderDropdown("Case ID Column", caseIdCol, setCaseIdCol, isXES)}
          {renderDropdown("Activity Column", activityCol, setActivityCol, isXES)}
          {renderDropdown("Timestamp Column", timestampCol, setTimestampCol, isXES)}
          {renderDropdown("Resource Column (optional)", resourceCol1, setResourceCol1, false, false)}
          {renderDropdown("Resource 2 Column (optional)", resourceCol2, setResourceCol2, false, false)}
          <Button variant="contained" onClick={handleSubmit}>Confirm Mapping</Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default MappingPage;