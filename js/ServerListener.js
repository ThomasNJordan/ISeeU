import { framePointBuffer } from './FramePointBuffer';

const WS_URL = 'ws://localhost:9000';

export class ServerListener {
    socket;

    constructor() {
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
        console.log(`[+] Receiving data chunk (${data.length} bytes)`);
        console.log(`[+] Data chunk: ${data}`);
        try {
            const point = JSON.parse(data);
            if (point.theta !== void 0 && point.distance !== void 0) {
                framePointBuffer.addPoint(point.theta, point.distance);
            } else {
                console.error('[-] Invalid data structure:', data.toString());
            }
        } catch (err) {
            console.error('[-] Failed to parse data:', err.message);
        }
    }
}