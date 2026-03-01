import asyncio
import websockets
import json

async def test_notif():
    uri = "ws://localhost:8000/ws/chats/test_uri/" # Replace with valid URI if needed
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({
            "message": "Hello from test script!",
            "user_id": 1 # Assuming test user ID 1 exists
        }))
        # Wait a bit for the server to process
        await asyncio.sleep(2)

if __name__ == "__main__":
    try:
        asyncio.run(test_notif())
    except Exception as e:
        print(f"Error: {e}")
