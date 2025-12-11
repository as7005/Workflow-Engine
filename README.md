# Minimal Agent Workflow Engine (FastAPI + WebSocket)

Small workflow/graph engine demonstrating nodes → state → edges → loops with a **Code Review Mini-Agent** sample workflow.

---

## What this repo contains

- **`app/`** — FastAPI app and engine:
  - `main.py` — API + WebSocket endpoints
  - `engine.py` — workflow execution engine (async)
  - `models.py` — Pydantic models
  - `tools.py` — tool registry (register helper functions)
  - `workflows.py` — Code Review nodes + registry
  - `websocket_manager.py` — per-run queues for streaming
  - `storage.py` — in-memory run storage
- **`tests/`** — small pytest smoke tests
- **`.github/workflows/ci.yml`** — runs tests on push

---

## Features

- **Nodes:** Python callables (async supported) that update shared `state`.
- **Edges:** Define successor nodes; nodes may override next node with `"next"`.
- **Branching:** Nodes can return a `next` node name for conditional routing.
- **Looping:** Nodes may route to a previous node; engine enforces a loop limit to avoid infinite loops.
- **Tool registry:** Maintain reusable helper functions.
- **FastAPI endpoints:**
  - `POST /graph/create` — create a graph JSON → returns `graph_id`
  - `POST /graph/run` — start a run with initial state → returns `run_id`
  - `GET /graph/state/{run_id}` — poll current state + logs
  - `WS /graph/stream/{run_id}` — JSON event stream of execution
- 
**Example workflow:** **Code Review Mini-Agent**
  - `extract_functions` → `check_complexity` → `detect_issues` → `suggest_improvements` → `review_wait` → loop until `quality_score >= threshold`

---

## Sample Workflow Diagram
extract_functions → check_complexity → detect_issues → suggest_improvements → review_wait


- The loop continues until the workflow’s `quality_score` reaches the desired threshold.
- Engine ensures **max iterations per node** to prevent infinite loops.

---

## Sample Run

**Request:**

```json
POST /graph/run
{
  "graph_id": "your-graph-id",
  "state": { "input": "def foo(): pass" }
}
```
**Response:**
{
  "run_id": "1234-5678",
  "graph_id": "your-graph-id",
  "state": {
    "functions_extracted": 5,
    "complexity_score": 10,
    "issues_found": 0,
    "quality_score": 22,
    "suggestions": [
      "Refactor function A",
      "Simplify loop in function B"
    ]
  },
  "logs": [
    {"timestamp": "...", "node": "extract", "status": "success"},
    {"timestamp": "...", "node": "complexity", "status": "success"},
    {"timestamp": "...", "node": "issues", "status": "success"},
    {"timestamp": "...", "node": "improvements", "status": "success"},
    {"timestamp": "...", "node": "wait", "status": "success"},
    {"timestamp": "...", "node": "complexity", "status": "success"}
  ],
  "finished": true
}

## Quick start
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows PowerShell:
# .\venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

## Running Tests
pytest tests/

## What this engine supports

- Sequential and looped workflows
- Conditional branching based on state
- Async node execution
- Polling and WebSocket-based run monitoring
- Simple tool registry for reusable functions

