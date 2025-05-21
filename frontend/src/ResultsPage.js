// import React, { useState } from 'react';
// import {
//   Box,
//   Button,
//   Card,
//   CardContent,
//   Typography,
//   Divider,
// } from '@mui/material';
// import Graph from './Graph';
// import Table from './Table';
//
// const dummyData = {
//   log_skeleton: {
//     graph: {
//       nodes: [
//         { id: 'Start' },
//         { id: 'Validate' },
//         { id: 'Approve' },
//         { id: 'Reject' },
//         { id: 'End' }
//       ],
//       edges: [
//         { from: "Start", to: 'Validate', label: 'always before' },
//         { from: 'Validate', to: 'Approve', label: 'sometimes before' },
//         { from: 'Validate', to: 'Reject', label: 'sometimes before' },
//         { from: 'Approve', to: 'End', label: 'always before' },
//         { from: 'Reject', to: 'End', label: 'always before' }
//       ]
//     },
//     table: [
//       { constraint: 'Start always before Validate', violated: 'No' },
//       { constraint: 'Validate sometimes before Approve', violated: 'Yes' },
//       { constraint: 'Approve always before End', violated: 'No' },
//       { constraint: 'Reject always before End', violated: 'No' }
//     ]
//   },
//
//   temporal: {
//     graph: {
//       nodes: [
//         { id: 'Submit Request' },
//         { id: 'Review Request' },
//         { id: 'Finalize' }
//       ],
//       edges: [
//         { from: 'Submit Request', to: 'Review Request', label: 'avg 2.1d' },
//         { from: 'Review Request', to: 'Finalize', label: 'avg 1.3d' }
//       ]
//     },
//     table: [
//       { activity: 'Submit Request', avg_duration: '1.8 days' },
//       { activity: 'Review Request', avg_duration: '2.1 days' },
//       { activity: 'Finalize', avg_duration: '0.9 days' },
//       { activity: 'Total Flow', avg_duration: '4.8 days' }
//     ]
//   },
//
//   declarative: {
//     graph: {
//       nodes: [
//         { id: 'Login' },
//         { id: 'Edit' },
//         { id: 'Save' },
//         { id: 'Logout' }
//       ],
//       edges: [
//         { from: 'Login', to: 'Logout', label: 'eventually follows' },
//         { from: 'Edit', to: 'Save', label: 'response' },
//         { from: 'Save', to: 'Edit', label: 'not co-exist' }
//       ]
//     },
//     table: [
//       { rule: 'Login must eventually be followed by Logout', satisfied: 'Yes' },
//       { rule: 'Edit should be followed by Save', satisfied: 'No' },
//       { rule: 'Edit and Save should not co-exist', satisfied: 'Yes' },
//       { rule: 'No duplicate Logout allowed', satisfied: 'Yes' }
//     ]
//   },
//
//   resource: {
//     graph: {
//       nodes: [
//         { id: 'Alice' },
//         { id: 'Bob' },
//         { id: 'Charlie' },
//         { id: 'Diana' }
//       ],
//       edges: [
//         { from: 'Alice', to: 'Bob', label: 'handover' },
//         { from: 'Bob', to: 'Charlie', label: 'handover' },
//         { from: 'Charlie', to: 'Diana', label: 'handover' },
//         { from: 'Diana', to: 'Alice', label: 'handover' }
//       ]
//     },
//     table: [
//       { resource: 'Alice', actions: 12, handovers: 3 },
//       { resource: 'Bob', actions: 15, handovers: 4 },
//       { resource: 'Charlie', actions: 8, handovers: 2 },
//       { resource: 'Diana', actions: 10, handovers: 3 }
//     ]
//   }
// };
//
// const ResultsPage = () => {
//   const [view, setView] = useState('log_skeleton');
//   const current = dummyData[view];
//
//   return (
//     <Card sx={{ mx: 'auto', mt: 4, maxWidth: 900, boxShadow: 3 }}>
//       <CardContent>
//         <Typography variant="h5" gutterBottom>
//           Conformance Insights
//         </Typography>
//
//         <Box sx={{ display: 'flex', gap: 2, my: 2, flexWrap: 'wrap' }}>
//           <Button
//             variant={view === 'log_skeleton' ? 'contained' : 'outlined'}
//             onClick={() => setView('log_skeleton')}
//           >
//             Log Skeleton
//           </Button>
//           <Button
//             variant={view === 'temporal' ? 'contained' : 'outlined'}
//             onClick={() => setView('temporal')}
//           >
//             Temporal
//           </Button>
//           <Button
//             variant={view === 'declarative' ? 'contained' : 'outlined'}
//             onClick={() => setView('declarative')}
//           >
//             Declarative
//           </Button>
//           <Button
//             variant={view === 'resource' ? 'contained' : 'outlined'}
//             onClick={() => setView('resource')}
//           >
//             Resource
//           </Button>
//         </Box>
//
//         <Divider />
//
//         <Box sx={{ mt: 3 }}>
//           {current?.graph && <Graph graphData={current.graph} />}
//           {current?.table && <Table tableData={current.table} />}
//           {!current?.graph && !current?.table && (
//             <Typography color="text.secondary">
//               ⚠ No data available for this conformance check.
//             </Typography>
//           )}
//         </Box>
//       </CardContent>
//     </Card>
//   );
// };
//
// export default ResultsPage;
import React, { useState, useEffect } from 'react';
import {
  Box, Button, Card, CardContent, Typography, Divider,
  MenuItem, Select, FormControl, InputLabel
} from '@mui/material';
import Graph from './Graph';
import Table from './Table';
import { API_BASE } from './config';

// ✅ Custom labels with URLs per option
const dropdownOptions = {
  log_skeleton: [
    { label: 'Log Skeleton A', endpoint: '/log_skeleton/a' },
    { label: 'Log Skeleton B', endpoint: '/log_skeleton/b' }
  ],
  declarative: [
    { label: 'Declare A', endpoint: '/declarative/a' },
    { label: 'Declare B', endpoint: '/declarative/b' }
  ],
  resource: [
    { label: 'Resource View A', endpoint: '/resource/a' },
    { label: 'Resource View B', endpoint: '/resource/b' }
  ]
};

const ResultsPage = () => {
  const [view, setView] = useState('log_skeleton');
  const [dropdownSelection, setDropdownSelection] = useState('');
  const [result, setResult] = useState({ graph: null, table: null });

  useEffect(() => {
    if (view === 'temporal') {
      fetch(`${API_BASE}/temporal`)
        .then(res => res.json())
        .then(data => setResult(data))
        .catch(err => console.error('Failed to fetch temporal data:', err));
    } else {
      setResult({ graph: null, table: null });
      setDropdownSelection('');
    }
  }, [view]);

  const handleDropdownChange = async (e) => {
    const selectedEndpoint = e.target.value;
    setDropdownSelection(selectedEndpoint);

    try {
      const res = await fetch(`${API_BASE}${selectedEndpoint}`);
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(`Failed to fetch ${selectedEndpoint}:`, err);
    }
  };

  const showDropdown = view !== 'temporal';
  const options = dropdownOptions[view] || [];

  return (
    <Card sx={{ mx: 'auto', mt: 4, maxWidth: 900, boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Conformance Insights
        </Typography>

        <Box sx={{ display: 'flex', gap: 2, my: 2, flexWrap: 'wrap' }}>
          <Button
            variant={view === 'log_skeleton' ? 'contained' : 'outlined'}
            onClick={() => setView('log_skeleton')}
          >
            Log Skeleton
          </Button>
          <Button
            variant={view === 'temporal' ? 'contained' : 'outlined'}
            onClick={() => setView('temporal')}
          >
            Temporal
          </Button>
          <Button
            variant={view === 'declarative' ? 'contained' : 'outlined'}
            onClick={() => setView('declarative')}
          >
            Declarative
          </Button>
          <Button
            variant={view === 'resource' ? 'contained' : 'outlined'}
            onClick={() => setView('resource')}
          >
            Resource
          </Button>
        </Box>

        {showDropdown && (
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>Select an option</InputLabel>
            <Select
              value={dropdownSelection}
              onChange={handleDropdownChange}
              label="Select an option"
            >
              {options.map((opt, i) => (
                <MenuItem key={i} value={opt.endpoint}>
                  {opt.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        )}

        <Divider />

        <Box sx={{ mt: 3 }}>
          {result.graph && <Graph graphData={result.graph} />}
          {result.table && <Table tableData={result.table} />}
        </Box>
      </CardContent>
    </Card>
  );
};

export default ResultsPage;