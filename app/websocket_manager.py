# app/websocket_manager.py
import asyncio
from fastapi import WebSocket
from typing import Dict, List, Optional


class WebSocketManager:
    """
    Manages one websocket connection and queue per run_id.
    If you need multiple subscribers per run_id, change connections -> List[WebSocket].
    """
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}
        self.queues: Dict[str, asyncio.Queue] = {}

    async def connect(self, run_id: str, ws: WebSocket):
        await ws.accept()
        self.connections[run_id] = ws
        q = asyncio.Queue()
        self.queues[run_id] = q
        # Start the streamer task that forwards queue -> websocket
        asyncio.create_task(self._stream_queue_to_ws(run_id, ws, q))

    async def disconnect(self, run_id: str):
        ws = self.connections.pop(run_id, None)
        if ws:
            try:
                await ws.close()
            except Exception:
                pass
        self.queues.pop(run_id, None)

    async def push(self, run_id: str, event: dict):
        q = self.queues.get(run_id)
        if q:
            await q.put(event)

    async def _stream_queue_to_ws(self, run_id: str, ws: WebSocket, queue: asyncio.Queue):
        try:
            while True:
                event = await queue.get()
                # Try to send; if send fails, break and cleanup
                try:
                    await ws.send_json(event)
                except Exception:
                    break
                if event.get("event") == "workflow_complete":
                    break
        finally:
            # best-effort cleanup
            await self.disconnect(run_id)


ws_manager = WebSocketManager()
