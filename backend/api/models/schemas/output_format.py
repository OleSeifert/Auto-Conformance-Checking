"""Contains the schemas for the output format of the API responses."""

from typing import List, Optional

from pydantic import BaseModel


class TableModel(BaseModel):
    """Represents a table with headers and rows."""

    headers: List[str]
    rows: List[List[str]]


class GraphNode(BaseModel):
    """Represents a node in a graph."""

    id: str


class GraphEdge(BaseModel):
    """Represents an edge with a label in a graph.

    Connects two nodes.
    """

    from_: str  # `from` is a reserved keyword
    to: str
    label: str

    class Config:
        """Represents a mapping for reserved keywords in Pydantic models."""

        fields = {
            "from_": "from",
        }


class GraphModel(BaseModel):
    """Represents a complete graph with nodes and edges."""

    nodes: List[GraphNode]
    edges: List[GraphEdge]


class ResponseSchema(BaseModel):
    """Represents the response schema for API endpoints."""

    tables: Optional[List[TableModel]] = []
    graphs: Optional[List[GraphModel]] = []
