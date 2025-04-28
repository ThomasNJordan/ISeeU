import { Packets } from './Packets';

const WS_URL = 'ws://192.168.1.100:9000';

export class ServerListener {
    socket;
    packets;

    constructor() {
        this.packets = new Packets();
        this.socket = new WebSocket(WS_URL);
        this.socket.onopen = () => {
            console.log('[+] Connected to WebSocket server');
        };
        this.socket.onmessage = (event) => {
            this.onDataReceived(event.data);
        };
        this.socket.onclose = () => {
            console.log('[+] WebSocket connection closed');
        };
        this.socket.onerror = (err) => {
            console.error('[-] WebSocket error:', err.message);
        };
    }

    onDataReceived(data) {
        console.log(`[+] Packet: ${data}`);
        try {
            const packetData = JSON.parse(data);
            if (packetData.distance !== void 0) {
                this.packets.addPacket(packetData);
            } else {
                console.error('[-] Invalid data structure:', data.toString());
            }
        } catch (err) {
            console.error('[-] Failed to parse data:', err.message);
        }
    }

    generateTestPackets() {
        for (let i = 0; i < 3; i++) {
            const distance = Math.random() * 10;
            this.onDataReceived(JSON.stringify({
                distance: distance,
                timestamp: Date.now()
            }));
        }
    }
}