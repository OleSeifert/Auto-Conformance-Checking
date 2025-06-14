import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

const Graph = ({ graphData }) => {
  const svgRef = useRef();

  useEffect(() => {
    const width = 900;
    const height = 600;
    const padding = 50;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const zoomGroup = svg.append("g");

    const zoom = d3
      .zoom()
      .scaleExtent([1, 2]) // restrict zoom-out below 1x
      .filter((event) => {
        // Only allow zoom via mouse wheel or dragging (not touch or pinch)
        return event.type === "wheel" || event.type === "mousedown";
      })
      .on("zoom", (event) => zoomGroup.attr("transform", event.transform));

    svg.call(zoom);
    const { nodes = [], edges = [] } = graphData;

    const colorScale = d3.scaleOrdinal(d3.schemeCategory10);
    const nodeColorMap = {};
    nodes.forEach((n, i) => {
      nodeColorMap[n.id] = colorScale(i);
    });

    const nodeById = new Map(nodes.map((n) => [n.id, n]));

    // Merge duplicate edges
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

    // Initialize node positions to avoid placing them outside
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
      .attr("stroke", (d) => d.color);

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
      .attr("r", 38)
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
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

      edgeLabel
        .attr("x", (d, i) => (d.source.x + d.target.x) / 2)
        .attr("y", (d, i) => (d.source.y + d.target.y) / 2 - 6 + (i % 5) * 12);
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
      // Keep fixed position after drag
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

export default Graph;
