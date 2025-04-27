import asyncio, json, time, sys
import websockets
import threading
import random

# Configuration
WS_URI = "ws://192.168.1.198:9000/"  # Your websocket server

async def websocket_sender(queue):
    while True:
        try:
            async with websockets.connect(WS_URI) as ws:
                print("[+] Connected to WebSocket server.")
                while True:
                    pw = await queue.get()
                    packet = {
                        "distance": pw,
                        # "timestamp": int(time.time() * 1000)
                    }
                    print("[>] Sending packet:", packet)
                    await ws.send(json.dumps(packet))
        except Exception as e:
            print(f"[!] WebSocket connection error: {e}")
            print("[*] Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

def fake_packet_generator(queue):
    while True:
        # Generate a random RSSI value between -90 and -30
        fake_rssi = random.randint(-90, -30)
        try:
            queue.put_nowait(fake_rssi)
            print(f"[*] Simulated RSSI: {fake_rssi}")
        except asyncio.QueueFull:
            print("[!] Queue full. Dropping fake packet.")
        time.sleep(1)  # simulate 1 packet per second

async def main():
    queue = asyncio.Queue()
    print("[*] Starting WebSocket sender...")
    asyncio.create_task(websocket_sender(queue))

    # Instead of sniffing real packets, start fake generator
    fake_thread = threading.Thread(target=lambda: fake_packet_generator(queue), daemon=True)
    fake_thread.start()

    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] KeyboardInterrupt caught. Exiting...")
        sys.exit(0)

