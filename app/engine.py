# app/engine.py
import asyncio
from datetime import datetime
from app.graph_store import store
from app.websocket_manager import ws_manager
from app.workflows import NODE_REGISTRY

QUALITY_THRESHOLD = 20  # set your threshold here

class SimpleEngine:
    async def start(self, run):
        # start the workflow
        await self.run_graph(run)

    async def run_graph(self, run):
        try:
            graph = store.get_graph(run.graph_id)
        except KeyError as e:
            await ws_manager.push(run.run_id, {"event": "workflow_error", "error": str(e)})
            run.finished = True
            return

        nodes_by_name = {n.name: n for n in graph.nodes}
        node = graph.start_node
        visited_nodes = set()  # to avoid infinite loops in case threshold is never reached

        while node:
            run.current_node = node
            await ws_manager.push(run.run_id, {"event": "node_start", "node": node, "state": run.state})

            node_def = nodes_by_name.get(node)
            if node_def is None:
                await ws_manager.push(run.run_id, {"event": "node_error", "node": node, "message": "node_def_missing"})
                break

            func = NODE_REGISTRY.get(node_def.func)
            if func is None:
                await ws_manager.push(run.run_id, {"event": "node_error", "node": node, "message": f"func '{node_def.func}' not registered"})
                break

            try:
                output = await func(run.state) if asyncio.iscoroutinefunction(func) else func(run.state)
            except Exception as e:
                await ws_manager.push(run.run_id, {"event": "node_error", "node": node, "message": str(e)})
                run.logs.append({"timestamp": datetime.utcnow().isoformat(), "node": node, "status": "error", "message": str(e)})
                break

            if not isinstance(output, dict):
                await ws_manager.push(run.run_id, {"event": "node_error", "node": node, "message": "node output must be dict"})
                break

            run.state.update(output)
            run.logs.append({"timestamp": datetime.utcnow().isoformat(), "node": node, "status": "success"})
            await ws_manager.push(run.run_id, {"event": "node_end", "node": node, "state": run.state})

            # ----------------------------
            # LOOP EXIT CONDITION
            # ----------------------------
            if run.state.get("quality_score", 0) >= QUALITY_THRESHOLD:
                # Stop the loop if threshold is reached
                break

            next_nodes = graph.edges.get(node, [])
            if not next_nodes:
                break
            node = next_nodes[0]  # pick first in the list for simplicity

        run.current_node = None
        run.finished = True
        run.finished_at = datetime.utcnow()
        await ws_manager.push(run.run_id, {"event": "workflow_complete", "run_id": run.run_id, "final_state": run.state})
