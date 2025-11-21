import asyncio
import websockets
import json

WS_URL = "ws://localhost:8000/ws/updates"

async def listen_ws():
    print(f"Conectando a {WS_URL} ...")

    while True:
        try:
            async with websockets.connect(WS_URL) as ws:
                print("🔗 Conectado al WebSocket! Esperando eventos...\n")

                while True:
                    message = await ws.recv()

                    try:
                        data = json.loads(message)
                    except:
                        print("Mensaje recibido (no JSON):", message)
                        continue

                    print("\n📨 EVENTO RECIBIDO:")
                    print(json.dumps(data, indent=4))

        except Exception as e:
            print(f"\n❌ Error de conexión: {e}")
            print("⏳ Reintentando en 3 segundos...\n")
            await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(listen_ws())
