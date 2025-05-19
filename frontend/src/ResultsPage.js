// import React, { useState } from 'react';
// import {
//   Box,
//   Button,
//   Card,
//   CardContent,
//   Typography,
//   Divider,
// } from '@mui/material';
//
// const ResultsPage = () => {
//   const [view, setView] = useState('log_skeleton');
//
//   const renderInsight = () => {
//     switch (view) {
//       case 'log_skeleton':
//         return <Typography>📊 Log Skeleton Placeholder</Typography>;
//       case 'temporal':
//         return <Typography>⏱ Temporal Insights Placeholder</Typography>;
//       case 'declarative':
//         return <Typography>⚖ Declarative Constraints Placeholder</Typography>;
//       case 'resource':
//         return <Typography>👥 Resource-based Insights Placeholder</Typography>;
//       default:
//         return null;
//     }
//   };
//
//   return (
//     <Card sx={{ mx: 'auto', mt: 4, maxWidth: 900, boxShadow: 3 }}>
//       <CardContent>
//         <Typography variant="h5" gutterBottom>
//           Conformance Insights
//         </Typography>
//         <Box sx={{ display: 'flex', gap: 2, my: 2 }}>
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
//         <Divider />
//         <Box sx={{ mt: 3 }}>{renderInsight()}</Box>
//       </CardContent>
//     </Card>
//   );
// };
//
// export default ResultsPage;
//

//when connecting with actual data:
// import React, { useState } from 'react';
// import {
//   Box,
//   Button,
//   Card,
//   CardContent,
//   Typography,
//   Divider,
// } from '@mui/material';
// import { useLocation } from 'react-router-dom';
// import Graph from './Graph';
// import Table from './Table';
//
// const ResultsPage = () => {
//   const location = useLocation();
//   const results = location.state || {};  // received from backend
//   const [view, setView] = useState('log_skeleton');
//   const current = results[view];
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

import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  Divider,
} from '@mui/material';
import Graph from './Graph';
import Table from './Table';

const dummyData = {
  log_skeleton: {
    graph: {
      nodes: [
        { id: 'Start' },
        { id: 'Validate' },
        { id: 'Approve' },
        { id: 'Reject' },
        { id: 'End' }
      ],
      edges: [
        { from: 'Start', to: 'Validate', label: 'always before' },
        { from: 'Validate', to: 'Approve', label: 'sometimes before' },
        { from: 'Validate', to: 'Reject', label: 'sometimes before' },
        { from: 'Approve', to: 'End', label: 'always before' },
        { from: 'Reject', to: 'End', label: 'always before' }
      ]
    },
    table: [
      { constraint: 'Start always before Validate', violated: 'No' },
      { constraint: 'Validate sometimes before Approve', violated: 'Yes' },
      { constraint: 'Approve always before End', violated: 'No' },
      { constraint: 'Reject always before End', violated: 'No' }
    ]
  },

  temporal: {
    graph: {
      nodes: [
        { id: 'Submit Request' },
        { id: 'Review Request' },
        { id: 'Finalize' }
      ],
      edges: [
        { from: 'Submit Request', to: 'Review Request', label: 'avg 2.1d' },
        { from: 'Review Request', to: 'Finalize', label: 'avg 1.3d' }
      ]
    },
    table: [
      { activity: 'Submit Request', avg_duration: '1.8 days' },
      { activity: 'Review Request', avg_duration: '2.1 days' },
      { activity: 'Finalize', avg_duration: '0.9 days' },
      { activity: 'Total Flow', avg_duration: '4.8 days' }
    ]
  },

  declarative: {
    graph: {
      nodes: [
        { id: 'Login' },
        { id: 'Edit' },
        { id: 'Save' },
        { id: 'Logout' }
      ],
      edges: [
        { from: 'Login', to: 'Logout', label: 'eventually follows' },
        { from: 'Edit', to: 'Save', label: 'response' },
        { from: 'Save', to: 'Edit', label: 'not co-exist' }
      ]
    },
    table: [
      { rule: 'Login must eventually be followed by Logout', satisfied: 'Yes' },
      { rule: 'Edit should be followed by Save', satisfied: 'No' },
      { rule: 'Edit and Save should not co-exist', satisfied: 'Yes' },
      { rule: 'No duplicate Logout allowed', satisfied: 'Yes' }
    ]
  },

  resource: {
    graph: {
      nodes: [
        { id: 'Alice' },
        { id: 'Bob' },
        { id: 'Charlie' },
        { id: 'Diana' }
      ],
      edges: [
        { from: 'Alice', to: 'Bob', label: 'handover' },
        { from: 'Bob', to: 'Charlie', label: 'handover' },
        { from: 'Charlie', to: 'Diana', label: 'handover' },
        { from: 'Diana', to: 'Alice', label: 'handover' }
      ]
    },
    table: [
      { resource: 'Alice', actions: 12, handovers: 3 },
      { resource: 'Bob', actions: 15, handovers: 4 },
      { resource: 'Charlie', actions: 8, handovers: 2 },
      { resource: 'Diana', actions: 10, handovers: 3 }
    ]
  }
};

const ResultsPage = () => {
  const [view, setView] = useState('log_skeleton');
  const current = dummyData[view];

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

        <Divider />

        <Box sx={{ mt: 3 }}>
          {current?.graph && <Graph graphData={current.graph} />}
          {current?.table && <Table tableData={current.table} />}
          {!current?.graph && !current?.table && (
            <Typography color="text.secondary">
              ⚠ No data available for this conformance check.
            </Typography>
          )}
        </Box>
      </CardContent>
    </Card>
  );
};

export default ResultsPage;