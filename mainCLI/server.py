import asyncio
import websockets

async def handler(websocket):
    print("[*] Client connected.")
    try:
        async for message in websocket:
            print("[>] Received:", message)
    except websockets.ConnectionClosed:
        print("[!] Connection closed.")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 9000):
        print("[*] WebSocket server started on port 9000")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Server interrupted. Exiting.")
