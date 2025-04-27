import { EMAFilter } from "./EMAFilter";
import { framePointBuffer } from "./FramePointBuffer";

export class Packets {
    constructor() {
        this.lastPacket = null;
        this.currentPacket = null;
    }

    addPacket(packet) {
        this.lastPacket = this.currentPacket;
        this.currentPacket = packet;
        const smoothedDistance = this.getNextSmoothedDistance();
        if (smoothedDistance === void 0)
            return;
        framePointBuffer.addPoint(smoothedDistance);
    }

    getNextSmoothedDistance() {
        return EMAFilter.filter(this.lastPacket, this.currentPacket);
    }
}