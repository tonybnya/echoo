import asyncio
import websockets
import json

async def test_notif():
    uri = "ws://localhost:8001/ws/chats/test_uri/" 
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({
            "message": "Hello from test script!",
            "user_id": 1 
        }))
        await asyncio.sleep(2)

if __name__ == "__main__":
    try:
        asyncio.run(test_notif())
    except Exception as e:
        print(f"Error: {e}")
