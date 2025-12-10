import uuid
from typing import Dict
from app.models import GraphDef, RunState


class GraphStore:
    def __init__(self):
        self.graphs: Dict[str, GraphDef] = {}
        self.runs: Dict[str, RunState] = {}

    def save_graph(self, graph: GraphDef) -> str:
        graph_id = str(uuid.uuid4())
        self.graphs[graph_id] = graph
        graph.nodes_by_name = {n.name: n for n in graph.nodes}

        return graph_id

    def get_graph(self, graph_id: str) -> GraphDef:
        if graph_id not in self.graphs:
            raise KeyError(f"Graph '{graph_id}' not found")
        return self.graphs[graph_id]

    def create_run(self, graph_id: str, state: dict) -> RunState:
        if graph_id not in self.graphs:
            raise KeyError(f"Graph '{graph_id}' not found")
        run_id = str(uuid.uuid4())
        run = RunState(run_id=run_id, graph_id=graph_id, state=state)
        self.runs[run_id] = run
        return run

    def get_run(self, run_id: str) -> RunState:
        if run_id not in self.runs:
            raise KeyError(f"Run '{run_id}' not found")
        return self.runs[run_id]


store = GraphStore()
