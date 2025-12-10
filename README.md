# Minimal Agent Workflow Engine (FastAPI + WebSocket)

Small workflow/graph engine demonstrating nodes → state → edges → loops with a Code Review sample workflow.

## What this repo contains
- `app/` — FastAPI app and engine:
  - `main.py` — API + WebSocket endpoints
  - `engine.py` — workflow execution engine (async)
  - `models.py` — Pydantic models
  - `tools.py` — tool registry (register helper functions)
  - `workflows.py` — Code Review nodes + registry
  - `websocket_manager.py` — per-run queues for streaming
  - `storage.py` — in-memory run storage
- `tests/` — small pytest smoke test
- `.github/workflows/ci.yml` — runs tests on push

## Features
- Nodes are Python callables (async supported) that update shared `state`.
- Edges define successor nodes; nodes may override next node with `"next"`.
- Branching: nodes can return a `next` node name for conditional routing.
- Looping: nodes may route to a previous node; engine enforces loop limit to avoid infinite loops.
- Tool registry for reusable helpers.
- FastAPI endpoints:
  - `POST /graph/create` — create graph JSON → returns `graph_id`
  - `POST /graph/run` — start run with initial state → returns `run_id`
  - `GET /graph/state/{run_id}` — poll current state + logs
  - `WS  /graph/stream/{run_id}` — JSON event stream of execution
- Example workflow: **Code Review Mini-Agent** — extract functions, measure complexity, detect issues, suggest improvements, loop until `quality_score >= quality_threshold`.

## Quick start
```bash
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows PowerShell:
# .\venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
