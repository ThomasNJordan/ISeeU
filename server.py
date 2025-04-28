#Goes on Computer. NOT ROUTER
import asyncio
import websockets

PORT = 9000
clients = set()

async def handler(websocket):
    print("[*] Client connected.")
    clients.add(websocket)  # Add the client to the set of connected clients
    try:
        async for message in websocket:
            print("[>] Received:", message)
            # Broadcast the message to all other connected clients
            for client in clients:
                if client != websocket:  # Don't send the message back to the sender
                    await client.send(message)
    except websockets.ConnectionClosed:
        print("[!] Connection closed.")
    finally:
        clients.remove(websocket)  # Remove the client when it disconnects

async def main():
    async with websockets.serve(handler, "192.168.1.100", 9000):
        print("[*] WebSocket server started on port 9000")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Server interrupted. Exiting.")