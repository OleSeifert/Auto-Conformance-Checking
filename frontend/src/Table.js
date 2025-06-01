
// import React from 'react';
// import {
//   Table as MuiTable,
//   TableHead,
//   TableBody,
//   TableRow,
//   TableCell
// } from '@mui/material';

// const Table = ({ headers, rows }) => {
//   return (
//     <MuiTable>
//       <TableHead>
//         <TableRow>
//           {headers.map((header, idx) => (
//             <TableCell key={idx}><strong>{header}</strong></TableCell>
//           ))}
//         </TableRow>
//       </TableHead>
//       <TableBody>
//         {rows.map((row, i) => (
//           <TableRow key={i}>
//             {row.map((cell, j) => (
//               <TableCell key={j}>{cell}</TableCell>
//             ))}
//           </TableRow>
//         ))}
//       </TableBody>
//     </MuiTable>
//   );
// };

// export default Table;
import React from 'react';
import {
  Table as MuiTable,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Paper,
  TableContainer
} from '@mui/material';

const Table = ({ headers, rows }) => {
  return (
    <TableContainer component={Paper} sx={{ my: 2, border: '1px solid #ccc' }}>
      <MuiTable sx={{ minWidth: 650 }} size="small" aria-label="styled table">
        <TableHead>
          <TableRow sx={{ backgroundColor: '#e0f0ff' }}> {/* light blue background */}
            {headers.map((header, idx) => (
              <TableCell
                key={idx}
                sx={{
                  borderRight: '1px solid #ccc',
                  fontWeight: 'bold'
                }}
              >
                {header}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row, i) => (
            <TableRow key={i}>
              {row.map((cell, j) => (
                <TableCell
                  key={j}
                  sx={{ borderRight: '1px solid #eee', borderTop: '1px solid #eee' }}
                >
                  {cell}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </MuiTable>
    </TableContainer>
  );
};

export default Table;