from pydantic import BaseModel
from typing import List, Optional


class TableModel(BaseModel):
    headers: List[str]
    rows: List[List[str]]


class GraphNode(BaseModel):
    id: str


class GraphEdge(BaseModel):
    from_: str  # `from` is a reserved keyword
    to: str
    label: str

    class Config:
        fields = {
            'from_': 'from',
        }


class GraphModel(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]


class ResponseSchema(BaseModel):
    tables: Optional[List[TableModel]] = []
    graphs: Optional[List[GraphModel]] = []