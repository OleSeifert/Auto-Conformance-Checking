// // import React, { useEffect, useRef } from 'react';
// // import * as d3 from 'd3';
// //
// // const Graph = ({ graphData }) => {
// //   const svgRef = useRef();
// //
// //   useEffect(() => {
// //     const svg = d3.select(svgRef.current);
// //     svg.selectAll('*').remove(); // clear previous
// //
// //     const { nodes, edges } = graphData;
// //
// //     const simulation = d3.forceSimulation(nodes)
// //       .force('link', d3.forceLink(edges).id(d => d.id).distance(120))
// //       .force('charge', d3.forceManyBody().strength(-300))
// //       .force('center', d3.forceCenter(300, 200));
// //
// //     const link = svg.append('g')
// //       .selectAll('line')
// //       .data(edges)
// //       .enter().append('line')
// //       .attr('stroke', '#999');
// //
// //     const edgeLabels = svg.append('g')
// //       .selectAll('text')
// //       .data(edges)
// //       .enter().append('text')
// //       .text(d => d.label)
// //       .attr('font-size', 12)
// //       .attr('fill', '#333');
// //
// //     const node = svg.append('g')
// //       .selectAll('circle')
// //       .data(nodes)
// //       .enter().append('circle')
// //       .attr('r', 20)
// //       .attr('fill', '#69b3a2')
// //       .call(d3.drag()
// //         .on('start', dragStart)
// //         .on('drag', dragged)
// //         .on('end', dragEnd));
// //
// //     const label = svg.append('g')
// //       .selectAll('text')
// //       .data(nodes)
// //       .enter().append('text')
// //       .text(d => d.id)
// //       .attr('font-size', 14)
// //       .attr('text-anchor', 'middle')
// //       .attr('dy', 4);
// //
// //     simulation.on('tick', () => {
// //       node.attr('cx', d => d.x).attr('cy', d => d.y);
// //       label.attr('x', d => d.x).attr('y', d => d.y);
// //       link
// //         .attr('x1', d => d.source.x)
// //         .attr('y1', d => d.source.y)
// //         .attr('x2', d => d.target.x)
// //         .attr('y2', d => d.target.y);
// //       edgeLabels
// //         .attr('x', d => (d.source.x + d.target.x) / 2)
// //         .attr('y', d => (d.source.y + d.target.y) / 2);
// //     });
// //
// //     function dragStart(event, d) {
// //       if (!event.active) simulation.alphaTarget(0.3).restart();
// //       d.fx = d.x;
// //       d.fy = d.y;
// //     }
// //
// //     function dragged(event, d) {
// //       d.fx = event.x;
// //       d.fy = event.y;
// //     }
// //
// //     function dragEnd(event, d) {
// //       if (!event.active) simulation.alphaTarget(0);
// //       d.fx = null;
// //       d.fy = null;
// //     }
// //
// //   }, [graphData]);
// //
// //   return <svg ref={svgRef} width={600} height={400}></svg>;
// // };
// //
// // export default Graph;
// import React, { useEffect, useRef } from 'react';
// import * as d3 from 'd3';
//
// const Graph = ({ graphData }) => {
//   const svgRef = useRef();
//
//   useEffect(() => {
//     const svg = d3.select(svgRef.current);
//     svg.selectAll('*').remove(); // Clear previous
//
//     const { nodes = [], edges = [] } = graphData;
//
//     // Build color scale and color map for nodes
//     const colorScale = d3.scaleOrdinal(d3.schemeCategory10);
//     const nodeColorMap = {};
//     nodes.forEach((n, i) => {
//       nodeColorMap[n.id] = colorScale(i);
//     });
//
//     // Convert edges to D3 format + assign source color
//     const nodeIds = new Set(nodes.map(n => n.id));
//     const d3Edges = edges
//       .filter(e => nodeIds.has(e.from) && nodeIds.has(e.to))
//       .map(e => ({
//         source: e.from,
//         target: e.to,
//         label: e.label,
//         color: nodeColorMap[e.from] || '#aaa' // use source node's color
//       }));
//
//     const simulation = d3
//       .forceSimulation(nodes)
//       .force('link', d3.forceLink(d3Edges).id(d => d.id).distance(120))
//       .force('charge', d3.forceManyBody().strength(-300))
//       .force('center', d3.forceCenter(300, 200));
//
//     // Draw links (colored by source node)
//     const link = svg.append('g')
//       .selectAll('line')
//       .data(d3Edges)
//       .enter()
//       .append('line')
//       .attr('stroke', d => d.color)
//       .attr('stroke-width', 2)
//       .attr('opacity', 0.8);
//
//     // Draw edge labels
//     const edgeLabels = svg.append('g')
//       .selectAll('text')
//       .data(d3Edges)
//       .enter()
//       .append('text')
//       .text(d => d.label)
//       .attr('font-size', 12)
//       .attr('fill', '#444')
//       .attr('text-anchor', 'middle');
//
//     // Draw nodes (neutral color or light gray)
//     const node = svg.append('g')
//       .selectAll('circle')
//       .data(nodes)
//       .enter()
//       .append('circle')
//       .attr('r', 20)
//       .attr('fill', '#ddd') // neutral node fill
//       .attr('stroke', d => nodeColorMap[d.id])
//       .attr('stroke-width', 3)
//       .call(
//         d3.drag()
//           .on('start', dragStart)
//           .on('drag', dragged)
//           .on('end', dragEnd)
//       );
//
//     // Node labels
//     const label = svg.append('g')
//       .selectAll('text')
//       .data(nodes)
//       .enter()
//       .append('text')
//       .text(d => d.id)
//       .attr('font-size', 14)
//       .attr('text-anchor', 'middle')
//       .attr('dy', 4)
//       .attr('fill', '#333');
//
//     simulation.on('tick', () => {
//       node.attr('cx', d => d.x).attr('cy', d => d.y);
//       label.attr('x', d => d.x).attr('y', d => d.y);
//       link
//         .attr('x1', d => d.source.x)
//         .attr('y1', d => d.source.y)
//         .attr('x2', d => d.target.x)
//         .attr('y2', d => d.target.y);
//       edgeLabels
//         .attr('x', d => (d.source.x + d.target.x) / 2)
//         .attr('y', d => (d.source.y + d.target.y) / 2 - 6);
//     });
//
//     function dragStart(event, d) {
//       if (!event.active) simulation.alphaTarget(0.3).restart();
//       d.fx = d.x;
//       d.fy = d.y;
//     }
//
//     function dragged(event, d) {
//       d.fx = event.x;
//       d.fy = event.y;
//     }
//
//     function dragEnd(event, d) {
//       if (!event.active) simulation.alphaTarget(0);
//       d.fx = null;
//       d.fy = null;
//     }
//   }, [graphData]);
//
//   return (
//     <svg
//       ref={svgRef}
//       width={600}
//       height={400}
//       style={{
//         border: '1px solid #ccc',
//         borderRadius: '8px',
//         background: '#f9f9f9'
//       }}
//     />
//   );
// };
//
// export default Graph;

import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const Graph = ({ graphData }) => {
  const svgRef = useRef();

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const { nodes = [], edges = [] } = graphData;
    const colorScale = d3.scaleOrdinal(d3.schemeCategory10);
    const nodeColorMap = {};
    nodes.forEach((n, i) => {
      nodeColorMap[n.id] = colorScale(i);
    });

    const d3Edges = edges
      .map(e => ({
        source: e.from,
        target: e.to,
        label: e.label,
        color: nodeColorMap[e.from] || '#aaa'
      }));

    const simulation = d3
      .forceSimulation(nodes)
      .force('link', d3.forceLink(d3Edges).id(d => d.id).distance(120))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(300, 200));

    const link = svg.append('g')
      .selectAll('line')
      .data(d3Edges)
      .enter().append('line')
      .attr('stroke', d => d.color)
      .attr('stroke-width', 2)
      .attr('opacity', 0.8);

    const edgeLabels = svg.append('g')
      .selectAll('text')
      .data(d3Edges)
      .enter()
      .append('text')
      .text(d => d.label)
      .attr('font-size', 12)
      .attr('fill', '#444')
      .attr('text-anchor', 'middle');

    const node = svg.append('g')
      .selectAll('circle')
      .data(nodes)
      .enter().append('circle')
      .attr('r', 20)
      .attr('fill', '#ddd')
      .attr('stroke', d => nodeColorMap[d.id])
      .attr('stroke-width', 3)
      .call(d3.drag()
        .on('start', dragStart)
        .on('drag', dragged)
        .on('end', dragEnd));

    const label = svg.append('g')
      .selectAll('text')
      .data(nodes)
      .enter().append('text')
      .text(d => d.id)
      .attr('font-size', 14)
      .attr('text-anchor', 'middle')
      .attr('dy', 4)
      .attr('fill', '#333');

    simulation.on('tick', () => {
      node.attr('cx', d => d.x).attr('cy', d => d.y);
      label.attr('x', d => d.x).attr('y', d => d.y);
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);
      edgeLabels
        .attr('x', d => (d.source.x + d.target.x) / 2)
        .attr('y', d => (d.source.y + d.target.y) / 2 - 6);
    });

    function dragStart(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragEnd(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
  }, [graphData]);

  return (
    <svg ref={svgRef} width={600} height={400} style={{
      border: '1px solid #ccc',
      borderRadius: '8px',
      background: '#f9f9f9'
    }} />
  );
};

export default Graph;