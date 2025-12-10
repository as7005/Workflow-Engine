# app/main.py
import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from app.models import GraphDef, RunRequest, RunState
from app.graph_store import store
from app.engine import SimpleEngine
from app.websocket_manager import ws_manager

app = FastAPI(title="Workflow Engine with WebSocket Streaming", version="0.1.0")
engine = SimpleEngine()


@app.post("/graph/create", status_code=201)
def create_graph(graph: GraphDef):
    """
    Create/register a graph. Returns graph_id.
    """
    try:
        gid = store.save_graph(graph)
        return {"graph_id": gid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/graph/run")
async def run_graph(req: RunRequest):
    """
    Start a run in the background. Returns run_id immediately.
    Events are streamed over WebSocket /ws/{run_id}.
    """
    try:
        run = store.create_run(req.graph_id, req.state or {})
    except KeyError:
        raise HTTPException(status_code=404, detail="graph not found; create graph first")

    # schedule background execution
    import asyncio
    asyncio.create_task(engine.start(run))

    return {"run_id": run.run_id}


@app.get("/graph/state/{run_id}", response_model=RunState)
def get_state(run_id: str):
    """
    Retrieve current RunState (polling style).
    """
    try:
        run = store.get_run(run_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="run not found")
    return run


@app.websocket("/ws/{run_id}")
async def websocket_endpoint(websocket: WebSocket, run_id: str):
    """
    Connect using a websocket client to receive events for a run.
    Example (JS): ws = new WebSocket("ws://localhost:8000/ws/<run_id>")
    """
    # register connection and start streaming queued events
    await ws_manager.connect(run_id, websocket)
    try:
        # Keep the connection open until the manager closes it after workflow_complete
        while True:
            # Receive pings from client (optional) to keep connection alive
            try:
                await websocket.receive_text()
            except WebSocketDisconnect:
                break
    finally:
        await ws_manager.disconnect(run_id)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
