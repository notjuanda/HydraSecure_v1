from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# Sirve archivos estáticos (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return FileResponse("static/index.html")

# Gestión simple de conexiones WebSocket
class ConnectionManager:
    def __init__(self):
        # {claveHash: [WebSocket, ...]}
        self.salas = {}
        self.ws_to_sala = {}  # WebSocket -> claveHash
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
    def disconnect(self, websocket: WebSocket):
        claveHash = self.ws_to_sala.get(websocket)
        if claveHash and websocket in self.salas.get(claveHash, []):
            self.salas[claveHash].remove(websocket)
            if not self.salas[claveHash]:
                del self.salas[claveHash]
        if websocket in self.ws_to_sala:
            del self.ws_to_sala[websocket]
    def join_sala(self, websocket: WebSocket, claveHash: str):
        if claveHash not in self.salas:
            self.salas[claveHash] = []
        if websocket not in self.salas[claveHash]:
            self.salas[claveHash].append(websocket)
        self.ws_to_sala[websocket] = claveHash
    async def send_to_sala(self, claveHash: str, message: str):
        for ws in self.salas.get(claveHash, []):
            await ws.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            import json
            try:
                msg = json.loads(data)
            except Exception:
                continue
            if msg.get('tipo') == 'join' and 'claveHash' in msg:
                manager.join_sala(websocket, msg['claveHash'])
            elif msg.get('tipo') == 'msg' and 'claveHash' in msg:
                # Solo reenvía a la sala correspondiente
                await manager.send_to_sala(msg['claveHash'], data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True) 