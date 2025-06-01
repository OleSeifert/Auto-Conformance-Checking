
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
//   CircularProgress,
//   TextField
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
//   GET_ACTIVITY_FREQUENCIES,
//   GET_RESULT_TEMPORAL_PROFILE,
//   TEMPORAL_PROFILE
// } from './config';


// // -------------------- Log Skeleton Options --------------------

// const LOG_SKELETON_OPTIONS = [
//   { label: "Get Equivalence", value: "get_equivalence", endpoint: GET_EQUVALENCE },
//   { label: "Always Before", value: "get_always_before", endpoint: GET_ALWAYS_BEFORE },
//   { label: "Always After", value: "get_always_after", endpoint: GET_ALWAYS_AFTER },
//   { label: "Never Together", value: "get_never_together", endpoint: GET_NEVER_TOGETHER },
//   { label: "Directly Follows", value: "get_directly_follows", endpoint: GET_DIRECTLY_FOLLOWS },
//   { label: "Activity Frequencies", value: "get_activity_frequencies", endpoint: GET_ACTIVITY_FREQUENCIES }
// ];


// // -------------------- Resource Options --------------------

// const resourceOptions = {
//   sna: [
//     "Handover of Work",
//     "Subcontracting",
//     "Working together",
//     "Similar Activities"
//   ],
//   role_discovery: [
//     "Role Discovery"
//   ],
//   resource_profiles: [
//     "Distinct Activities",
//     "Activity Frequency",
//     "Activity Completions",
//     "Case-Completions",
//     "Fraction-Case Completions",
//     "Average workload",
//     "Multitasking",
//     "Average Activity Duration",
//     "Average case duration",
//     "Interaction Two Resources",
//     "Social Position"
//   ],
//   organizational_mining: [
//     "Group Relative Focus",
//     "Group Relative Stake",
//     "Group Coverage",
//     "Group Member Contributions"
//   ]
// };


// // -------------------- Main Component --------------------

// const ResultsPage = () => {
//   const [view, setView] = useState('log_skeleton');

//   // Shared
//   const [graphData, setGraphData] = useState([]);
//   const [tableData, setTableData] = useState([]);

//   // Log Skeleton
//   const [jobId, setJobId] = useState(null);
//   const [selectedOption, setSelectedOption] = useState('');
//   const [loading, setLoading] = useState(false);

//   // Temporal Profile
//   const [zeta, setZeta] = useState('');
//   const [temporalJobId, setTemporalJobId] = useState(null);
//   const [showResultLoading, setShowResultLoading] = useState(false);

//   // Resource-based Conformance
//   const [selectedResourceType, setSelectedResourceType] = useState('');
//   const [selectedResourceOption, setSelectedResourceOption] = useState('');


//   // -------------------- Log Skeleton: Fetch Job ID --------------------

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


//   // -------------------- Log Skeleton: Handle Option Selection --------------------

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


//   // -------------------- Temporal Profile: Submit Zeta --------------------

//   const handleComputeTemporal = async () => {
//     if (!zeta) {
//       alert("Please enter a zeta value.");
//       return;
//     }

//     try {
//       const computeRes = await fetch(`${TEMPORAL_PROFILE}?zeta=${parseFloat(zeta)}`, {
//         method: 'POST'
//       });

//       if (!computeRes.ok) {
//         const errorText = await computeRes.text();
//         throw new Error(`Error computing job: ${errorText}`);
//       }

//       const computeData = await computeRes.json();
//       setTemporalJobId(computeData.job_id);
//       alert("Zeta submitted successfully. You can now click 'Show Temporal Results' to view the result.");

//     } catch (err) {
//       alert("Error submitting zeta value: " + err.message);
//       console.error(err);
//     }
//   };


//   // -------------------- Temporal Profile: Fetch Results --------------------

//   const handleFetchTemporalResults = async () => {
//     if (!temporalJobId) {
//       alert("Please submit zeta first.");
//       return;
//     }

//     setGraphData([]);
//     setTableData([]);
//     setShowResultLoading(true);

//     try {
//       let attempts = 0;
//       let resultData = null;

//       while (attempts < 20) {
//         const resultRes = await fetch(`${GET_RESULT_TEMPORAL_PROFILE}/${temporalJobId}`);
//         if (resultRes.ok) {
//           resultData = await resultRes.json();
//           break;
//         } else {
//           await new Promise(res => setTimeout(res, 500));
//           attempts++;
//         }
//       }

//       if (!resultData) {
//         throw new Error("Timeout: backend did not return results in time.");
//       }

//       setGraphData(resultData.graphs || []);
//       setTableData(resultData.tables || []);

//     } catch (err) {
//       alert("Error fetching temporal profile result: " + err.message);
//       console.error("Detailed error:", err);
//     } finally {
//       setShowResultLoading(false);
//     }
//   };


//   // -------------------- Render Graphs & Tables --------------------

//   const renderGraphAndTable = () => {
//     const hasGraphs = Array.isArray(graphData) && graphData.length > 0;
//     const hasTables = Array.isArray(tableData) && tableData.length > 0;

//     return (
//       <>
//         {hasGraphs && graphData.map((graph, idx) => (
//           <Box key={idx} sx={{ mt: 4 }}>
//             <Typography variant="h6">Graph {idx + 1}</Typography>
//             <Graph graphData={graph} />
//           </Box>
//         ))}

//         {hasTables && tableData.map((table, idx) => (
//           <Box key={idx} sx={{ mt: 4 }}>
//             <Typography variant="h6">Table {idx + 1}</Typography>
//             <Table headers={table.headers} rows={table.rows} />
//           </Box>
//         ))}

//         {!hasGraphs && !hasTables && (
//           <Typography color="text.secondary" sx={{ mt: 2 }}>
//             No data to display.
//           </Typography>
//         )}
//       </>
//     );
//   };


//   // -------------------- UI --------------------

//   return (
//     <Card sx={{ mx: 'auto', mt: 4, maxWidth: 1000, boxShadow: 3 }}>
//       <CardContent>
//         <Typography variant="h5" gutterBottom>
//           Conformance Insights
//         </Typography>

//         {/* View Selector */}
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
//           {/* -------- Log Skeleton Section -------- */}
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

//           {/* -------- Temporal Profile Section -------- */}
//           {view === 'temporal' && (
//             <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
//               <TextField
//                 label="Zeta Value"
//                 variant="outlined"
//                 type="number"
//                 value={zeta}
//                 onChange={(e) => setZeta(e.target.value)}
//                 fullWidth
//               />
//               <Button variant="contained" onClick={handleComputeTemporal}>Submit Zeta</Button>
//               <Button variant="outlined" onClick={handleFetchTemporalResults}>Show Temporal Results</Button>

//               {showResultLoading ? (
//                 <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
//                   <CircularProgress />
//                 </Box>
//               ) : (
//                 renderGraphAndTable()
//               )}
//             </Box>
//           )}

//           {/* -------- Resource-Based Section -------- */}
//           {view === 'resource' && (
//             <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
//               {/* Primary Dropdown */}
//               <FormControl fullWidth>
//                 <InputLabel>Resource Perspective</InputLabel>
//                 <Select
//                   value={selectedResourceType}
//                   label="Resource Perspective"
//                   onChange={(e) => {
//                     setSelectedResourceType(e.target.value);
//                     setSelectedResourceOption('');
//                   }}
//                 >
//                   <MenuItem value="sna">Social Network Analysis</MenuItem>
//                   <MenuItem value="role_discovery">Role Discovery</MenuItem>
//                   <MenuItem value="resource_profiles">Resource Profiles</MenuItem>
//                   <MenuItem value="organizational_mining">Organizational Mining</MenuItem>
//                 </Select>
//               </FormControl>

//               {/* Secondary Dropdown */}
//               {selectedResourceType && (
//                 <FormControl fullWidth>
//                   <InputLabel>Resource Insight</InputLabel>
//                   <Select
//                     value={selectedResourceOption}
//                     label="Resource Insight"
//                     onChange={(e) => setSelectedResourceOption(e.target.value)}
//                   >
//                     {resourceOptions[selectedResourceType].map((opt) => (
//                       <MenuItem key={opt} value={opt}>{opt}</MenuItem>
//                     ))}
//                   </Select>
//                 </FormControl>
//               )}
//             </Box>
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
  CircularProgress,
  TextField
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
  GET_ACTIVITY_FREQUENCIES,
  GET_RESULT_TEMPORAL_PROFILE,
  TEMPORAL_PROFILE,
  RESOURCE_BASED,
  HANDOVER_OF_WORK,
  SUBCONTRACTING,
  WORKING_TOGETHER,
  SIMILAR_ACTIVITIES
} from './config';


// -------------------- Log Skeleton Options --------------------

const LOG_SKELETON_OPTIONS = [
  { label: "Get Equivalence", value: "get_equivalence", endpoint: GET_EQUVALENCE },
  { label: "Always Before", value: "get_always_before", endpoint: GET_ALWAYS_BEFORE },
  { label: "Always After", value: "get_always_after", endpoint: GET_ALWAYS_AFTER },
  { label: "Never Together", value: "get_never_together", endpoint: GET_NEVER_TOGETHER },
  { label: "Directly Follows", value: "get_directly_follows", endpoint: GET_DIRECTLY_FOLLOWS },
  { label: "Activity Frequencies", value: "get_activity_frequencies", endpoint: GET_ACTIVITY_FREQUENCIES }
];


// -------------------- Resource Options --------------------

const resourceOptions = {
  sna: [
    "Handover of Work",
    "Subcontracting",
    "Working together",
    "Similar Activities"
  ],
  role_discovery: [
    "Role Discovery"
  ],
  resource_profiles: [
    "Distinct Activities",
    "Activity Frequency",
    "Activity Completions",
    "Case-Completions",
    "Fraction-Case Completions",
    "Average workload",
    "Multitasking",
    "Average Activity Duration",
    "Average case duration",
    "Interaction Two Resources",
    "Social Position"
  ],
  organizational_mining: [
    "Group Relative Focus",
    "Group Relative Stake",
    "Group Coverage",
    "Group Member Contributions"
  ]
};


// -------------------- Main Component --------------------

const ResultsPage = () => {
  const [view, setView] = useState('log_skeleton');

  // Shared
  const [graphData, setGraphData] = useState([]);
  const [tableData, setTableData] = useState([]);

  // Log Skeleton
  const [jobId, setJobId] = useState(null);
  const [selectedOption, setSelectedOption] = useState('');
  const [loading, setLoading] = useState(false);

  // Temporal Profile
  const [zeta, setZeta] = useState('');
  const [temporalJobId, setTemporalJobId] = useState(null);
  const [showResultLoading, setShowResultLoading] = useState(false);

  // Resource-based Conformance
  const [selectedResourceType, setSelectedResourceType] = useState('');
  const [selectedResourceOption, setSelectedResourceOption] = useState('');
  const [resourceJobId, setResourceJobId] = useState(null);


  // -------------------- Log Skeleton: Fetch Job ID --------------------

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


  // -------------------- Resource-Based: Fetch Job ID --------------------

  useEffect(() => {
    if (view === 'resource') {
      const computeResourceJob = async () => {
        try {
          const res = await fetch(RESOURCE_BASED, { method: 'POST' });
          const data = await res.json();
          setResourceJobId(data.job_id);
        } catch (err) {
          alert("Error starting resource-based computation: " + err.message);
        }
      };
      computeResourceJob();
    }
  }, [view]);


  // -------------------- Log Skeleton: Handle Option Selection --------------------

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


  // -------------------- Temporal Profile: Submit Zeta --------------------

  const handleComputeTemporal = async () => {
    if (!zeta) {
      alert("Please enter a zeta value.");
      return;
    }

    try {
      const computeRes = await fetch(`${TEMPORAL_PROFILE}?zeta=${parseFloat(zeta)}`, {
        method: 'POST'
      });

      if (!computeRes.ok) {
        const errorText = await computeRes.text();
        throw new Error(`Error computing job: ${errorText}`);
      }

      const computeData = await computeRes.json();
      setTemporalJobId(computeData.job_id);
      alert("Zeta submitted successfully. You can now click 'Show Temporal Results' to view the result.");

    } catch (err) {
      alert("Error submitting zeta value: " + err.message);
      console.error(err);
    }
  };


  // -------------------- Temporal Profile: Fetch Results --------------------

  const handleFetchTemporalResults = async () => {
    if (!temporalJobId) {
      alert("Please submit zeta first.");
      return;
    }

    setGraphData([]);
    setTableData([]);
    setShowResultLoading(true);

    try {
      let attempts = 0;
      let resultData = null;

      while (attempts < 20) {
        const resultRes = await fetch(`${GET_RESULT_TEMPORAL_PROFILE}/${temporalJobId}`);
        if (resultRes.ok) {
          resultData = await resultRes.json();
          break;
        } else {
          await new Promise(res => setTimeout(res, 500));
          attempts++;
        }
      }

      if (!resultData) {
        throw new Error("Timeout: backend did not return results in time.");
      }

      setGraphData(resultData.graphs || []);
      setTableData(resultData.tables || []);

    } catch (err) {
      alert("Error fetching temporal profile result: " + err.message);
      console.error("Detailed error:", err);
    } finally {
      setShowResultLoading(false);
    }
  };


  // -------------------- Resource-Based: Handle SNA Option Selection --------------------

  const handleSNAOptionSelect = async (selected) => {
    const endpointMap = {
     "Handover of Work": HANDOVER_OF_WORK,
      "Subcontracting": SUBCONTRACTING,
     "Working together": WORKING_TOGETHER,
      "Similar Activities": SIMILAR_ACTIVITIES
    };

  const endpoint = endpointMap[selected];
  if (!endpoint || !resourceJobId) return;

  setGraphData([]);
  setTableData([]);
  setLoading(true);

  try {
      const res = await fetch(`${endpoint}/${resourceJobId}`);
      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(errorText);
      }

      const result = await res.json();
      setGraphData(result.graphs || []);
      setTableData(result.tables || []);
    } catch (err) {
      alert("Error fetching resource-based result: " + err.message);
      console.error(err);
    } finally {
      setLoading(false);
   }
  };

  // -------------------- Render Graphs & Tables --------------------

  const renderGraphAndTable = () => {
    const hasGraphs = Array.isArray(graphData) && graphData.length > 0;
    const hasTables = Array.isArray(tableData) && tableData.length > 0;

    return (
      <>
        {hasGraphs && graphData.map((graph, idx) => (
          <Box key={idx} sx={{ mt: 4 }}>
            <Typography variant="h6">Graph {idx + 1}</Typography>
            <Graph graphData={graph} />
          </Box>
        ))}

        {hasTables && tableData.map((table, idx) => (
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


  // -------------------- UI --------------------

  return (
    <Card sx={{ mx: 'auto', mt: 4, maxWidth: 1000, boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Conformance Insights
        </Typography>

        {/* View Selector */}
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
          {/* -------- Log Skeleton Section -------- */}
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

          {/* -------- Temporal Profile Section -------- */}
          {view === 'temporal' && (
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <TextField
                label="Zeta Value"
                variant="outlined"
                type="number"
                value={zeta}
                onChange={(e) => setZeta(e.target.value)}
                fullWidth
              />
              <Button variant="contained" onClick={handleComputeTemporal}>Submit Zeta</Button>
              <Button variant="outlined" onClick={handleFetchTemporalResults}>Show Temporal Results</Button>

              {showResultLoading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                  <CircularProgress />
                </Box>
              ) : (
                renderGraphAndTable()
              )}
            </Box>
          )}

          {/* -------- Resource-Based Section -------- */}
          {view === 'resource' && (
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {/* Primary Dropdown */}
              <FormControl fullWidth>
                <InputLabel>Resource Perspective</InputLabel>
                <Select
                  value={selectedResourceType}
                  label="Resource Perspective"
                  onChange={(e) => {
                    setSelectedResourceType(e.target.value);
                    setSelectedResourceOption('');
                  }}
                >
                  <MenuItem value="sna">Social Network Analysis</MenuItem>
                  <MenuItem value="role_discovery">Role Discovery</MenuItem>
                  <MenuItem value="resource_profiles">Resource Profiles</MenuItem>
                  <MenuItem value="organizational_mining">Organizational Mining</MenuItem>
                </Select>
              </FormControl>

              {/* Secondary Dropdown */}
              {selectedResourceType && (
                <FormControl fullWidth>
                  <InputLabel>Resource Insight</InputLabel>
                  <Select
                    value={selectedResourceOption}
                    label="Resource Insight"
                    onChange={(e) => {
                      setSelectedResourceOption(e.target.value);
                      if (selectedResourceType === 'sna') {
                        handleSNAOptionSelect(e.target.value);
                      }
                    }}
                  >
                    {resourceOptions[selectedResourceType].map((opt) => (
                      <MenuItem key={opt} value={opt}>{opt}</MenuItem>
                    ))}
                  </Select>
                </FormControl>
              )}

              {loading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                  <CircularProgress />
                </Box>
              ) : (
                renderGraphAndTable()
              )}
            </Box>
          )}
        </Box>
      </CardContent>
    </Card>
  );
};

export default ResultsPage;