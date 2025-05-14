import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  Divider,
} from '@mui/material';

const ResultsPage = () => {
  const [view, setView] = useState('log_skeleton');

  const renderInsight = () => {
    switch (view) {
      case 'log_skeleton':
        return <Typography>📊 Log Skeleton Placeholder</Typography>;
      case 'temporal':
        return <Typography>⏱ Temporal Insights Placeholder</Typography>;
      case 'declarative':
        return <Typography>⚖ Declarative Constraints Placeholder</Typography>;
      case 'resource':
        return <Typography>👥 Resource-based Insights Placeholder</Typography>;
      default:
        return null;
    }
  };

  return (
    <Card sx={{ mx: 'auto', mt: 4, maxWidth: 900, boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Conformance Insights
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, my: 2 }}>
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
        <Box sx={{ mt: 3 }}>{renderInsight()}</Box>
      </CardContent>
    </Card>
  );
};

export default ResultsPage;

//
// import React, { useState } from 'react';
// import { useLocation } from 'react-router-dom';
// import Graph from './Graph';
// import Table from './Table';
//
// const ResultsPage = () => {
//   const location = useLocation();
//   const results = location.state;
//
//   // ⬅ Start with log_skeleton as default
//   const [view, setView] = useState('log_skeleton');
//
//   const current = results?.[view];
//
//   return (
//     <div style={{ padding: '2rem' }}>
//       <h2>Conformance Insights</h2>
//
//       {/* ⬅ Add Log Skeleton button first */}
//       <div style={{ marginBottom: '1rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
//         <button onClick={() => setView('log_skeleton')}>Log Skeleton</button>
//         <button onClick={() => setView('temporal')}>Temporal</button>
//         <button onClick={() => setView('declarative')}>Declarative</button>
//         <button onClick={() => setView('resource')}>Resource</button>
//       </div>
//
//       {/* Conditional render: if graph/table exist for selected view */}
//       {current?.graph && <Graph graphData={current.graph} />}
//       {current?.table && <Table tableData={current.table} />}
//     </div>
//   );
// };
//
// export default ResultsPage;