// import React, { useState, useEffect } from 'react';
// import {
//   Box, Button, Card, CardContent, Typography,
//   FormControl, InputLabel, MenuItem, Select, FormHelperText
// } from '@mui/material';
// import { useNavigate } from 'react-router-dom';
// import { API_BASE } from './config';

// const MappingPage = () => {
//   const navigate = useNavigate();

//   const [columns, setColumns] = useState([]);
//   const [isXES, setIsXES] = useState(false);

//   const [caseIdCol, setCaseIdCol] = useState('');
//   const [activityCol, setActivityCol] = useState('');
//   const [timestampCol, setTimestampCol] = useState('');
//   const [resourceCol1, setResourceCol1] = useState('');
//   const [resourceCol2, setResourceCol2] = useState('');

//   useEffect(() => {
//     const fetchColumns = async () => {
//       try {
//         const res = await fetch(`${API_BASE}/get-columns`);
//         const result = await res.json();
//         const cols = result.columns || [];

//         setColumns(cols);

//         // If it's .xes, use first 3 as fixed values
//         if (cols.length >= 3 && cols[0].toLowerCase().includes('case')) {
//           setIsXES(true);
//           setCaseIdCol(cols[0]);
//           setActivityCol(cols[1]);
//           setTimestampCol(cols[2]);
//         }
//       } catch (err) {
//         alert('Failed to fetch column names: ' + err.message);
//       }
//     };

//     fetchColumns();
//   }, []);

//   const handleSubmit = async () => {
//     const payload = {
//       case_id_col: caseIdCol,
//       activity_col: activityCol,
//       timestamp_col: timestampCol,
//       resource_col1: resourceCol1,
//       resource_col2: resourceCol2
//     };

//     try {
//       const res = await fetch(`${API_BASE}/mapping-columns`, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify(payload)
//       });

//       const result = await res.json();
//       navigate('/results', { state: result });
//     } catch (err) {
//       alert('Failed to send mappings: ' + err.message);
//     }
//   };

//   const renderDropdown = (label, value, setter, disabled = false, required = true) => (
//     <FormControl fullWidth required={required} error={required && !value} disabled={disabled}>
//       <InputLabel>{label}</InputLabel>
//       <Select value={value} onChange={(e) => setter(e.target.value)} label={label}>
//         {columns.map((col, i) => (
//           <MenuItem key={i} value={col}>
//             {col}
//           </MenuItem>
//         ))}
//       </Select>
//       {required && !value && <FormHelperText>Required</FormHelperText>}
//     </FormControl>
//   );

//   return (
//     <Card sx={{ maxWidth: 600, mx: 'auto', mt: 4, boxShadow: 3 }}>
//       <CardContent>
//         <Typography variant="h5">Map Columns</Typography>
//         <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
//           {renderDropdown("Case ID Column", caseIdCol, setCaseIdCol, isXES)}
//           {renderDropdown("Activity Column", activityCol, setActivityCol, isXES)}
//           {renderDropdown("Timestamp Column", timestampCol, setTimestampCol, isXES)}
//           {renderDropdown("Resource Column (optional)", resourceCol1, setResourceCol1, false, false)}
//           {renderDropdown("Resource 2 Column (optional)", resourceCol2, setResourceCol2, false, false)}
//           <Button variant="contained" onClick={handleSubmit}>Confirm Mapping</Button>
//         </Box>
//       </CardContent>
//     </Card>
//   );
// };

// export default MappingPage;
import React, { useState, useEffect } from 'react';
import {
  Box, Button, Card, CardContent, Typography,
  FormControl, InputLabel, MenuItem, Select, FormHelperText
} from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';
import { MAPPING_COLUMNS } from './config';

const MappingPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const columns = location.state?.columns || [];
  const fileType = location.state?.fileType || 'csv';
  const isXES = fileType === 'xes';

  const [caseIdCol, setCaseIdCol] = useState('');
  const [activityCol, setActivityCol] = useState('');
  const [timestampCol, setTimestampCol] = useState('');
  const [resourceCol1, setResourceCol1] = useState('');
  const [resourceCol2, setResourceCol2] = useState('');

  const reservedCols = ['concept:name', 'Activity', 'time:timestamp'];
  const resourceOptions = isXES
    ? columns.filter(col => !reservedCols.includes(col))
    : columns;

  useEffect(() => {
    if (isXES) {
      setCaseIdCol('concept:name');
      setActivityCol('Activity');
      setTimestampCol('time:timestamp');
    }
  }, [columns, isXES]);

  const handleSubmit = async () => {
    const payload = {
      case_id_col: caseIdCol,
      activity_col: activityCol,
      timestamp_col: timestampCol,
      resource_col1: resourceCol1,
      resource_col2: resourceCol2
    };

    try {
      const res = await fetch(`${MAPPING_COLUMNS}`, {
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

  const renderDropdown = (
    label,
    value,
    setter,
    disabled = false,
    required = true,
    options = columns
  ) => (
    <FormControl fullWidth required={required} error={required && !value} disabled={disabled}>
      <InputLabel>{label}</InputLabel>
      <Select value={value} onChange={(e) => setter(e.target.value)} label={label}>
        {options.map((col, i) => (
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
          {renderDropdown("Resource Column (optional)", resourceCol1, setResourceCol1, false, false, resourceOptions)}
          {renderDropdown("Resource 2 Column (optional)", resourceCol2, setResourceCol2, false, false, resourceOptions)}
          <Button variant="contained" onClick={handleSubmit}>Confirm Mapping</Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default MappingPage;