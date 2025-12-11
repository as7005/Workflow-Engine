from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio

router = APIRouter()

@router.websocket("/ws/code-review")
async def ws_code_review(websocket: WebSocket):
    await websocket.accept()
    print("✔ WebSocket accepted")

    try:
        while True:
            # Receive JSON message from client
            data = await websocket.receive_json()
            print("📥 received:", data)

            code = data.get("code", "")
            lang = data.get("language", "python")

            # Send streaming messages
            await websocket.send_text("🔍 analyzing code...")
            await asyncio.sleep(0.5)

            await websocket.send_text(f"📌 language: {lang}")
            await asyncio.sleep(0.5)

            await websocket.send_text("✔ analysis completed")
            print("📤 sent results")

    except WebSocketDisconnect:
        print("❌ client disconnected")
