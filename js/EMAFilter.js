export class EMAFilter {
    static filter(lastPacket, currentPacket) {
        if (lastPacket === undefined || currentPacket === undefined) {
            return void 0;
        }
        const alpha = 0.27; // Smoothing factor
        const ema_c = currentPacket.distance;
        const ema_p = lastPacket.distance;
        return alpha * ema_c + (1-alpha) * ema_p;
    }
}