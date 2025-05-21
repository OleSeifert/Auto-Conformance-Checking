// import React from 'react';
//
// const Table = ({ tableData }) => {
//   if (!tableData?.length) return null;
//
//   const headers = Object.keys(tableData[0]);
//
//   return (
//     <table border="1" style={{ marginTop: '2rem', width: '100%' }}>
//       <thead>
//         <tr>
//           {headers.map((h, i) => <th key={i}>{h}</th>)}
//         </tr>
//       </thead>
//       <tbody>
//         {tableData.map((row, i) => (
//           <tr key={i}>
//             {headers.map((h, j) => <td key={j}>{row[h]}</td>)}
//           </tr>
//         ))}
//       </tbody>
//     </table>
//   );
// };
//
// export default Table;

import React from 'react';

const Table = ({ tableData }) => {
  if (!tableData || !tableData.length) return null;

  const headers = Object.keys(tableData[0]);

  return (
    <table border="1" style={{ marginTop: '1rem', width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr>
          {headers.map((h, i) => (
            <th key={i} style={{ padding: '8px', background: '#eee' }}>{h}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {tableData.map((row, i) => (
          <tr key={i}>
            {headers.map((h, j) => (
              <td key={j} style={{ padding: '8px' }}>{row[h]}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default Table;