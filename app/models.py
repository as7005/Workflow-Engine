from pydantic import BaseModel, model_validator
from typing import Dict, List, Optional
from datetime import datetime

class NodeDef(BaseModel):
    name: str
    func: str


class GraphDef(BaseModel):
    nodes: List[NodeDef]
    edges: Dict[str, List[str]]
    start_node: str

    # ALLOW extra fields like "nodes_by_name"
    model_config = {
        "extra": "allow"
    }

    @model_validator(mode="after")
    def validate_edges(self):
        node_names = {n.name for n in self.nodes}

        for src in self.edges.keys():
            if src not in node_names:
                raise ValueError(f"Edge source '{src}' not found in nodes")

        for src, targets in self.edges.items():
            for t in targets:
                if t not in node_names:
                    raise ValueError(f"Edge target '{t}' not found in nodes")

        if self.start_node not in node_names:
            raise ValueError(f"start_node '{self.start_node}' not found in nodes")

        return self


class RunState(BaseModel):
    run_id: str
    graph_id: str
    state: dict
    logs: List[dict] = []
    current_node: Optional[str] = None
    finished: bool = False
    finished_at: Optional[datetime] = None


class RunRequest(BaseModel):
    graph_id: str
    state: dict = {}
