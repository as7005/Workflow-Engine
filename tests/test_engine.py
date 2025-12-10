import asyncio
from app.models import GraphDef, NodeDef, RunState
from app.engine import engine
from app.workflows import NODE_REGISTRY


def make_graph():
    return GraphDef(
        nodes=[
            NodeDef(name="start", func="extract"),
            NodeDef(name="mid", func="check_complexity"),
            NodeDef(name="end", func="detect_issues"),
        ],
        edges={"start": ["mid"], "mid": ["end"], "end": []},
        start_node="start",
    )


def test_run_simple_workflow():
    g = make_graph()
    run = RunState(run_id="r1", graph_id="g1", state={"code": "def a(): pass"})

    asyncio.run(engine.run_graph(run))

    assert run.finished is True
    assert "issues" in run.state
