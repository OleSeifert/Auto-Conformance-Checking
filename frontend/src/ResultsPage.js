
// import React, { useState, useEffect } from 'react';
// import {
//   Box,
//   Button,
//   Card,
//   CardContent,
//   Typography,
//   Divider,
//   MenuItem,
//   Select,
//   InputLabel,
//   FormControl,
//   CircularProgress
// } from '@mui/material';
// import Graph from './Graph';
// import Table from './Table';
// import {
//   COMPUTE_SKELETON,
//   GET_EQUVALENCE,
//   GET_ALWAYS_BEFORE,
//   GET_ALWAYS_AFTER,
//   GET_NEVER_TOGETHER,
//   GET_DIRECTLY_FOLLOWS,
//   GET_ACTIVITY_FREQUENCIES
// } from './config';

// const LOG_SKELETON_OPTIONS = [
//   { label: "Get Equivalence", value: "get_equivalence", endpoint: GET_EQUVALENCE },
//   { label: "Always Before", value: "get_always_before", endpoint: GET_ALWAYS_BEFORE },
//   { label: "Always After", value: "get_always_after", endpoint: GET_ALWAYS_AFTER },
//   { label: "Never Together", value: "get_never_together", endpoint: GET_NEVER_TOGETHER },
//   { label: "Directly Follows", value: "get_directly_follows", endpoint: GET_DIRECTLY_FOLLOWS },
//   { label: "Activity Frequencies", value: "get_activity_frequencies", endpoint: GET_ACTIVITY_FREQUENCIES }
// ];

// const ResultsPage = () => {
//   const [view, setView] = useState('log_skeleton');
//   const [jobId, setJobId] = useState(null);
//   const [selectedOption, setSelectedOption] = useState('');
//   const [graphData, setGraphData] = useState([]);
//   const [tableData, setTableData] = useState([]);
//   const [loading, setLoading] = useState(false);

//   useEffect(() => {
//     const computeJob = async () => {
//       try {
//         const res = await fetch(COMPUTE_SKELETON, { method: 'POST' });
//         const data = await res.json();
//         setJobId(data.job_id);
//       } catch (err) {
//         alert('Error starting log skeleton computation: ' + err.message);
//       }
//     };
//     computeJob();
//   }, []);

//   const handleOptionSelect = async (option) => {
//     setSelectedOption(option.value);
//     setGraphData([]);
//     setTableData([]);
//     setLoading(true);

//     try {
//       const res = await fetch(`${option.endpoint}/${jobId}`);
//       const result = await res.json();
//       setGraphData(result.graphs || []);
//       setTableData(result.tables || []);
//     } catch (err) {
//       alert('Failed to fetch result: ' + err.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const renderGraphAndTable = () => (
//     <>
//       {Array.isArray(graphData) && graphData.length > 0 ? (
//         graphData.map((graph, idx) => (
//           <Box key={idx} sx={{ mt: 4 }}>
//             <Typography variant="h6">Graph {idx + 1}</Typography>
//             <Graph graphData={graph} />
//           </Box>
//         ))
//       ) : (
//         <Typography color="text.secondary" sx={{ mt: 2 }}>
//           No graph data
//         </Typography>
//       )}

//       {Array.isArray(tableData) && tableData.length > 0 ? (
//         tableData.map((table, idx) => (
//           <Box key={idx} sx={{ mt: 4 }}>
//             <Typography variant="h6">Table {idx + 1}</Typography>
//             <Table headers={table.headers} rows={table.rows} />
//           </Box>
//         ))
//       ) : (
//         <Typography color="text.secondary" sx={{ mt: 2 }}>
//           No table data
//         </Typography>
//       )}
//     </>
//   );

//   return (
//     <Card sx={{ mx: 'auto', mt: 4, maxWidth: 1000, boxShadow: 3 }}>
//       <CardContent>
//         <Typography variant="h5" gutterBottom>
//           Conformance Insights
//         </Typography>

//         <Box sx={{ display: 'flex', gap: 2, my: 2 }}>
//           <Button variant={view === 'log_skeleton' ? 'contained' : 'outlined'} onClick={() => setView('log_skeleton')}>
//             Log Skeleton
//           </Button>
//           <Button variant={view === 'temporal' ? 'contained' : 'outlined'} onClick={() => setView('temporal')}>
//             Temporal
//           </Button>
//           <Button variant={view === 'declarative' ? 'contained' : 'outlined'} onClick={() => setView('declarative')}>
//             Declarative
//           </Button>
//           <Button variant={view === 'resource' ? 'contained' : 'outlined'} onClick={() => setView('resource')}>
//             Resource
//           </Button>
//         </Box>

//         <Divider />

//         <Box sx={{ mt: 3 }}>
//           {view === 'log_skeleton' && (
//             <>
//               <FormControl fullWidth sx={{ mb: 2 }}>
//                 <InputLabel>Select Log Skeleton Operation</InputLabel>
//                 <Select
//                   value={selectedOption}
//                   label="Select Log Skeleton Operation"
//                   onChange={(e) =>
//                     handleOptionSelect(
//                       LOG_SKELETON_OPTIONS.find(opt => opt.value === e.target.value)
//                     )
//                   }
//                   disabled={!jobId}
//                 >
//                   {LOG_SKELETON_OPTIONS.map((opt) => (
//                     <MenuItem key={opt.value} value={opt.value}>
//                       {opt.label}
//                     </MenuItem>
//                   ))}
//                 </Select>
//               </FormControl>

//               {loading ? (
//                 <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
//                   <CircularProgress />
//                 </Box>
//               ) : (
//                 renderGraphAndTable()
//               )}
//             </>
//           )}
//         </Box>
//       </CardContent>
//     </Card>
//   );
// };

// export default ResultsPage;

import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  Divider,
  MenuItem,
  Select,
  InputLabel,
  FormControl,
  CircularProgress
} from '@mui/material';
import Graph from './Graph';
import Table from './Table';
import {
  COMPUTE_SKELETON,
  GET_EQUVALENCE,
  GET_ALWAYS_BEFORE,
  GET_ALWAYS_AFTER,
  GET_NEVER_TOGETHER,
  GET_DIRECTLY_FOLLOWS,
  GET_ACTIVITY_FREQUENCIES
} from './config';

const LOG_SKELETON_OPTIONS = [
  { label: "Get Equivalence", value: "get_equivalence", endpoint: GET_EQUVALENCE },
  { label: "Always Before", value: "get_always_before", endpoint: GET_ALWAYS_BEFORE },
  { label: "Always After", value: "get_always_after", endpoint: GET_ALWAYS_AFTER },
  { label: "Never Together", value: "get_never_together", endpoint: GET_NEVER_TOGETHER },
  { label: "Directly Follows", value: "get_directly_follows", endpoint: GET_DIRECTLY_FOLLOWS },
  { label: "Activity Frequencies", value: "get_activity_frequencies", endpoint: GET_ACTIVITY_FREQUENCIES }
];

const ResultsPage = () => {
  const [view, setView] = useState('log_skeleton');
  const [jobId, setJobId] = useState(null);
  const [selectedOption, setSelectedOption] = useState('');
  const [graphData, setGraphData] = useState([]);
  const [tableData, setTableData] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const computeJob = async () => {
      try {
        const res = await fetch(COMPUTE_SKELETON, { method: 'POST' });
        const data = await res.json();
        setJobId(data.job_id);
      } catch (err) {
        alert('Error starting log skeleton computation: ' + err.message);
      }
    };
    computeJob();
  }, []);

  const handleOptionSelect = async (option) => {
    setSelectedOption(option.value);
    setGraphData([]);
    setTableData([]);
    setLoading(true);

    try {
      const res = await fetch(`${option.endpoint}/${jobId}`);
      const result = await res.json();
      setGraphData(result.graphs || []);
      setTableData(result.tables || []);
    } catch (err) {
      alert('Failed to fetch result: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderGraphAndTable = () => {
    const hasGraphs = Array.isArray(graphData) && graphData.length > 0;
    const hasTables = Array.isArray(tableData) && tableData.length > 0;

    return (
      <>
        {hasGraphs &&
          graphData.map((graph, idx) => (
            <Box key={idx} sx={{ mt: 4 }}>
              <Typography variant="h6">Graph {idx + 1}</Typography>
              <Graph graphData={graph} />
            </Box>
          ))}

        {hasTables &&
          tableData.map((table, idx) => (
            <Box key={idx} sx={{ mt: 4 }}>
              <Typography variant="h6">Table {idx + 1}</Typography>
              <Table headers={table.headers} rows={table.rows} />
            </Box>
          ))}

        {!hasGraphs && !hasTables && (
          <Typography color="text.secondary" sx={{ mt: 2 }}>
            No data to display.
          </Typography>
        )}
      </>
    );
  };

  return (
    <Card sx={{ mx: 'auto', mt: 4, maxWidth: 1000, boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Conformance Insights
        </Typography>

        <Box sx={{ display: 'flex', gap: 2, my: 2 }}>
          <Button variant={view === 'log_skeleton' ? 'contained' : 'outlined'} onClick={() => setView('log_skeleton')}>
            Log Skeleton
          </Button>
          <Button variant={view === 'temporal' ? 'contained' : 'outlined'} onClick={() => setView('temporal')}>
            Temporal
          </Button>
          <Button variant={view === 'declarative' ? 'contained' : 'outlined'} onClick={() => setView('declarative')}>
            Declarative
          </Button>
          <Button variant={view === 'resource' ? 'contained' : 'outlined'} onClick={() => setView('resource')}>
            Resource
          </Button>
        </Box>

        <Divider />

        <Box sx={{ mt: 3 }}>
          {view === 'log_skeleton' && (
            <>
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Select Log Skeleton Operation</InputLabel>
                <Select
                  value={selectedOption}
                  label="Select Log Skeleton Operation"
                  onChange={(e) =>
                    handleOptionSelect(
                      LOG_SKELETON_OPTIONS.find(opt => opt.value === e.target.value)
                    )
                  }
                  disabled={!jobId}
                >
                  {LOG_SKELETON_OPTIONS.map((opt) => (
                    <MenuItem key={opt.value} value={opt.value}>
                      {opt.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              {loading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                  <CircularProgress />
                </Box>
              ) : (
                renderGraphAndTable()
              )}
            </>
          )}
        </Box>
      </CardContent>
    </Card>
  );
};

export default ResultsPage;