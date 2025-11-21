import asyncio
import websockets
import json

async def listen():
    # URL del WebSocket (asegúrate que el puerto coincida con tu uvicorn)
    uri = "ws://localhost:8000/ws/updates"
    print(f"Intentando conectar a {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print(" ¡Conexión exitosa! Escuchando eventos...")
            print("(Abre otra terminal y envía una petición POST a /simulate-event/new-order)")
            
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                print("\n NOTIFICACIÓN RECIBIDA:")
                print(json.dumps(data, indent=2))
                
    except Exception as e:
        print(f" Error de conexión: {e}")
        print("Asegúrate de ejecutar el servidor con: uvicorn main:app --reload")

if __name__ == "__main__":
    asyncio.run(listen())