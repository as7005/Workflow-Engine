import time
import asyncio
from typing import Dict, Any
from .workflows.code_review import NODE_REGISTRY



class WorkflowEngine:
    def __init__(self):
        self.run_logs = {}

    async def execute_node(self, node_def, state):
        """Executes a node with timing and optional parameters."""
        func = NODE_REGISTRY[node_def.func]

        params = node_def.params or {}
        merged_input = {**state, **params}

        start_time = time.time()
        try:
            if asyncio.iscoroutinefunction(func):
                new_state = await func(merged_input)
            else:
                new_state = func(merged_input)

            duration = (time.time() - start_time) * 1000

            return {
                "status": "success",
                "duration_ms": duration,
                "output_state": new_state,
            }

        except Exception as e:
            duration = (time.time() - start_time) * 1000
            return {
                "status": "error",
                "duration_ms": duration,
                "error_message": str(e),
                "output_state": state
            }

    async def execute_workflow(self, workflow_def, run_id, ws_manager=None):
        state = {}
        node_durations = {}
        loop_counter = {}
        workflow_start = time.time()

        self.run_logs[run_id] = []

        for node_def in workflow_def.nodes:
            node_name = node_def.name
            loop_counter.setdefault(node_name, 0)
            loop_counter[node_name] += 1

            result = await self.execute_node(node_def, state)

            # Track time
            node_durations[node_name] = node_durations.get(node_name, 0) + result["duration_ms"]

            # Logging
            log_entry = {
                "run_id": run_id,
                "node": node_name,
                "loop_count": loop_counter[node_name],
                "status": result["status"],
                "duration_ms": result["duration_ms"],
                "state_snapshot": result["output_state"],
                "error": result.get("error_message")
            }
            self.run_logs[run_id].append(log_entry)

            # WebSocket broadcast
            if ws_manager:
                await ws_manager.broadcast(run_id, log_entry)

            state = result["output_state"]

        total_duration = (time.time() - workflow_start) * 1000

        state["metrics"] = {
            "node_durations_ms": node_durations,
            "total_workflow_duration_ms": total_duration,
            "loop_counts": loop_counter,
        }

        return state
