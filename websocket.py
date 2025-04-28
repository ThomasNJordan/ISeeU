import argparse, json, asyncio, sys, threading
import websockets
from scapy.all import sniff, RadioTap, Dot11

# Set this!
WS_URI = "ws://192.168.1.100:9000/"  # Your WebSocket server

# Global
last_seen = {}
packet_queue = asyncio.Queue()

async def websocket_sender():
    while True:
        try:
            async with websockets.connect(WS_URI) as ws:
                print("[+] Connected to WebSocket server.")
                while True:
                    out = await packet_queue.get()
                    print("[>] Sending packet:", out)
                    await ws.send(json.dumps(out))
        except Exception as e:
            print(f"[!] WebSocket connection error: {e}")
            print("[*] Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

def handle_packet(pkt):
    if not pkt.haslayer(RadioTap) or not pkt.haslayer(Dot11):
        return

    rt = pkt[RadioTap]
    dot11 = pkt[Dot11]

    if (dot11.type == 0 and dot11.subtype == 8):  # Beacon frame
        src = dot11.addr2
    elif (dot11.FCfield & 0x03) == 0x01:  # FromDS=1, ToDS=0
        src = dot11.addr2
    else:
        return

    if args.bssid and src.lower() != args.bssid.lower():
        return

    val = None
    if hasattr(rt, 'dBm_AntSignal') and rt.dBm_AntSignal is not None:
        val = rt.dBm_AntSignal
    elif hasattr(rt, 'DB_AntSignal') and rt.DB_AntSignal is not None:
        val = rt.DB_AntSignal

    if val is None:
        return

    last = last_seen.get(src)
    if last == val:
        return
    last_seen[src] = val

    out = {
        "distance": int(val),
        "time": pkt.time
    }
try:                                                             
    packet_queue.put_nowait(out)                                 
except asyncio.QueueFull:                                        
    print("[!] Queue full. Dropping packet.")                    
                                                                     
def sniff_packets():                                                 
    print("[+] Starting Packet Capture")                             
    sniff(iface=args.iface, prn=handle_packet, store=False)          
                                                                     
async def main():                                                    
    asyncio.create_task(websocket_sender())                          
                                                                     
    sniff_thread = threading.Thread(target=sniff_packets, daemon=True)
    sniff_thread.start()                                              
                                                                      
    while True:                                                       
        await asyncio.sleep(1)                                        
                                                                      
if __name__ == "__main__":                                            
    p = argparse.ArgumentParser(description="Sniff Radiotap power levels and send over WebSocket")
    p.add_argument("-i", "--iface", required=True, help="Monitor-mode interface (e.g. wlan0mon)") 
    p.add_argument("-b", "--bssid", default=None, help="Only show power for this BSSID (optional)")
    args = p.parse_args()                                                                          
                                                                                                   
    try:                                                                                           
        asyncio.run(main())                                                                        
    except KeyboardInterrupt:                                                                      
        print("\n[!] KeyboardInterrupt caught. Exiting...")                                        
        sys.exit(0)     