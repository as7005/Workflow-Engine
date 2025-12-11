# Minimal Agent Workflow Engine

A simplified workflow/graph engine built with **FastAPI** and Python, demonstrating nodes → state → edges → loops with a **Code Review Mini-Agent** workflow. This project simulates a minimal version of tools like LangGraph.

---

## 🚀 Overview

This project implements a small agent workflow engine where:

- **Nodes** represent Python functions that read and modify a shared state.
- **Edges** define the execution sequence of nodes.
- **Branching** allows conditional routing based on state values.
- **Looping** supports repeated execution until a condition is met.
- **Tool Registry** provides reusable helper functions for nodes.
- **APIs** allow creation, execution, and monitoring of workflows.
- **WebSocket Streaming** enables live monitoring of workflow runs (optional enhancement).

The primary goal is **clarity, structure, and correctness** of a minimal workflow engine.

---

## 🛠 Features

- **Workflow Engine**
  - Async Python nodes
  - Shared state propagation
  - Edges, branching, and looping
  - Loop protection to prevent infinite loops

- **Tool Registry**
  - Pre-registered Python functions
  - Nodes can call tools to perform tasks

- **FastAPI Endpoints**
  - `POST /graph/create` → Register a workflow graph
  - `POST /graph/run` → Start a workflow run with initial state
  - `GET /graph/state/{run_id}` → Poll current state and logs
  - `WS /ws/{run_id}` → Stream workflow events in real-time

- **Sample Workflow: Code Review Mini-Agent**
  1. Extract functions
  2. Check complexity
  3. Detect issues
  4. Suggest improvements
  5. Loop until `quality_score >= threshold`

- **Optional Enhancements**
  - WebSocket streaming
  - Async background execution
  - Reusable tool registry

---

## 📁 Project Structure
```
workflow-engine/
├── app/
│ ├── main.py # FastAPI app & endpoints
│ ├── engine.py # Workflow engine logic
│ ├── workflows.py # Node definitions & sample workflow
│ ├── models.py # Pydantic models
│ ├── websocket_manager.py # WebSocket connection handling
│ ├── graph_store.py # In-memory storage for graphs and runs
| |── workflows/
|   ├── __init_.py
|   ├── code_review.py
├── tests/
│ └── test_engine.py # Minimal smoke tests
├── requirements.txt
├── README.md
└── .github/workflows/ci.yml # CI pipeline
```
---

## 📊 Workflow Diagram

```text
[extract functions] --> [check complexity] --> [detect issues] --> [suggest improvements]
        ^                                                                 |
        |                                                                 v
        --------------------------------------------------- [loop until quality_score >= threshold]
---

## ⚡ Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows PowerShell:
# .\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the FastAPI server
uvicorn app.main:app --reload --port 8000

Access Swagger UI: http://localhost:8000/docs
WebSocket endpoint: ws://localhost:8000/ws/{run_id}
```
---
## 📌 How to Use
Create a Graph
```json
POST /graph/create
{
  "nodes": [
    { "name": "extract", "func": "extract_functions" },
    { "name": "complexity", "func": "check_complexity" },
    { "name": "issues", "func": "detect_issues" },
    { "name": "improvements", "func": "suggest_improvements" },
    { "name": "wait", "func": "review_wait" }
  ],
  "edges": {
    "extract": ["complexity"],
    "complexity": ["issues"],
    "issues": ["improvements"],
    "improvements": ["wait"],
    "wait": ["complexity"]
  },
  "start_node": "extract"
}
```
# Run a Graph
```
POST /graph/run
{
  "graph_id": "<graph_id>",
  "state": {
    "input": "print('hello world')",
    "quality_score": 0
  }
}
```
# Check Run State
GET /graph/state/{run_id}

# WebSocket Streaming
Connect to ws://localhost:8000/ws/{run_id} to receive live workflow events.

---

## 📝 Improvements with More Time
- Persist workflows and runs in SQLite/Postgres
- Better workflow DAG visualization
- Custom error handling for each node
- Distributed execution and concurrent runs support
- Enhanced logging and metrics
- Dynamic workflow creation via API

---

## 🧪 Testing & Validation
- Linting: flake8 app/ → ensures PEP8 compliance
- Run Tests: pytest tests/ → basic smoke tests
- WebSocket Testing: Send code snippets and check live responses

---
## 🔧 Future Enhancements

- Database persistence: Store graphs and runs in SQLite/Postgres.
- Dynamic workflow creation: Allow runtime addition of nodes and edges.
- Multiple concurrent runs: Support distributed execution.
- Better visualization: DAG diagrams for workflows.
- Custom error handling per node: Graceful failure and retry strategies.
- Authentication / Authorization: Restrict workflow access.
- UI dashboard: Monitor runs, logs, and workflow metrics in real-time.

---

## 📌 Conclusion
This project demonstrates a minimal but fully functional workflow engine in Python with:
- Node execution
- State management
- Branching & looping
- FastAPI endpoints
- Optional WebSocket streaming
- Focus was on clarity, structure, and correctness, ensuring the engine is maintainable and easy to extend.

---
## 📚 References
- FastAPI Documentation
- Pydantic Models
- AsyncIO Documentation
