from fastapi import FastAPI, WebSocket,WebSocketDisconnect
from .gameManager import GameManager

app =FastAPI()
game_manager=GameManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("hiii")
    await websocket.accept()
    try:
        await game_manager.addUser(websocket)
    except WebSocketDisconnect:
        await game_manager.removeUser(websocket)
    