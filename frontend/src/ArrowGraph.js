import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

const ArrowGraph = ({ graphData }) => {
  const svgRef = useRef();

  useEffect(() => {
    const width = 900;
    const height = 600;
    const padding = 50;
    const nodeRadius = 38;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const zoomGroup = svg.append("g");

    svg.call(
      d3.zoom().on("zoom", (event) => {
        zoomGroup.attr("transform", event.transform);
      })
    );

    const { nodes = [], edges = [] } = graphData;

    const colorScale = d3.scaleOrdinal(d3.schemeCategory10);
    const nodeColorMap = {};
    nodes.forEach((n, i) => {
      nodeColorMap[n.id] = colorScale(i);
    });

    const nodeById = new Map(nodes.map((n) => [n.id, n]));

    const edgeMap = new Map();
    edges.forEach((e) => {
      const key = `${e.from}|||${e.to}`;
      const label = String(e.label);
      if (edgeMap.has(key)) {
        edgeMap.get(key).labels.push(label);
      } else {
        edgeMap.set(key, {
          from: e.from,
          to: e.to,
          labels: [label],
        });
      }
    });

    const d3Edges = Array.from(edgeMap.values())
      .map((e) => ({
        source: nodeById.get(e.from),
        target: nodeById.get(e.to),
        label: e.labels.join(", "),
        weight: e.labels.length,
        color: nodeColorMap[e.from] || "#ccc",
      }))
      .filter((e) => e.source && e.target);

    // Marker for arrows — refX must match the shortened line offset
    svg
      .append("defs")
      .append("marker")
      .attr("id", "arrowhead")
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 10) // arrowhead offset relative to the shortened line
      .attr("refY", 0)
      .attr("markerWidth", 6)
      .attr("markerHeight", 6)
      .attr("orient", "auto")
      .append("path")
      .attr("d", "M0,-5L10,0L0,5")
      .attr("fill", "#555");

    // Initialize node positions
    nodes.forEach((node) => {
      node.x = Math.random() * (width - 2 * padding) + padding;
      node.y = Math.random() * (height - 2 * padding) + padding;
    });

    const simulation = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3
          .forceLink(d3Edges)
          .id((d) => d.id)
          .distance(220)
      )
      .force("charge", d3.forceManyBody().strength(-600))
      .force("center", d3.forceCenter(width / 2, height / 2));

    const link = zoomGroup
      .append("g")
      .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(d3Edges)
      .enter()
      .append("line")
      .attr("stroke-width", (d) => Math.max(1.5, Math.min(8, d.weight)))
      .attr("stroke", (d) => d.color)
      .attr("marker-end", "url(#arrowhead)");

    const edgeLabel = zoomGroup
      .append("g")
      .selectAll("text")
      .data(d3Edges)
      .enter()
      .append("text")
      .attr("font-size", 10)
      .attr("fill", "#333")
      .attr("text-anchor", "middle")
      .append("tspan")
      .text((d) => d.label);

    const nodeGroup = zoomGroup
      .append("g")
      .selectAll("g")
      .data(nodes)
      .enter()
      .append("g")
      .call(
        d3.drag().on("start", dragStart).on("drag", dragged).on("end", dragEnd)
      );

    nodeGroup
      .append("circle")
      .attr("r", nodeRadius)
      .attr("fill", (d) => nodeColorMap[d.id])
      .attr("stroke", "#333")
      .attr("stroke-width", 1.5);

    nodeGroup.append("title").text((d) => d.id);

    nodeGroup
      .append("text")
      .attr("text-anchor", "middle")
      .attr("dy", 0)
      .attr("font-size", 10)
      .attr("fill", "#fff")
      .style("pointer-events", "none")
      .selectAll("tspan")
      .data((d) =>
        d.id.length > 12
          ? [d.id.slice(0, d.id.length / 2), d.id.slice(d.id.length / 2)]
          : [d.id]
      )
      .enter()
      .append("tspan")
      .attr("x", 0)
      .attr("dy", (d, i) => (i === 0 ? 0 : 12))
      .text((d) => d);

    simulation.on("tick", () => {
      nodeGroup.attr("transform", (d) => {
        d.x = Math.max(padding, Math.min(width - padding, d.x));
        d.y = Math.max(padding, Math.min(height - padding, d.y));
        return `translate(${d.x},${d.y})`;
      });

      link
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => {
          const dx = d.target.x - d.source.x;
          const dy = d.target.y - d.source.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          return d.target.x - (dx * (nodeRadius + 5)) / dist;
        })
        .attr("y2", (d) => {
          const dx = d.target.x - d.source.x;
          const dy = d.target.y - d.source.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          return d.target.y - (dy * (nodeRadius + 5)) / dist;
        });

      // Track label counts between same source-target pairs
      const labelOffsets = new Map();
      edgeLabel
        .attr("x", (d) => (d.source.x + d.target.x) / 2)
        .attr("y", function (d) {
          const key = `${d.source.id}|||${d.target.id}`;
          const count = labelOffsets.get(key) || 0;
          labelOffsets.set(key, count + 1);

          // Alternate label positions around the line
          const baseY = (d.source.y + d.target.y) / 2;
          const offset = (count - 1) * 12;
          return baseY + (count % 2 === 0 ? offset : -offset);
        });
    });

    setTimeout(() => simulation.stop(), 3000);

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
    }
  }, [graphData]);

  return (
    <svg
      ref={svgRef}
      width={900}
      height={600}
      style={{
        border: "1px solid #ccc",
        borderRadius: "10px",
        background: "#fcfcfc",
        marginTop: "10px",
      }}
    />
  );
};

export default ArrowGraph;
