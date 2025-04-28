import { EMAFilter } from "./EMAFilter";
import { framePointBuffer } from "./FramePointBuffer";
import { KalmanFilter } from "./KalmanFilter";

export class Packets {
    constructor() {
        this.lastPacket = null;
        this.currentPacket = null;
    }

    addPacket(packet) {
        this.lastPacket = this.currentPacket;
        this.currentPacket = packet;
        const smoothedDistance = this.currentPacket.distance;
        // const smoothedDistance = this.getNextSmoothedDistance();
        if (smoothedDistance === void 0)
            return;
        this.currentPacket.distance = smoothedDistance;
        if (this.isMotionDetected())
            console.log("[!] MOTION DETECTED")
        framePointBuffer.addPoint(smoothedDistance);
    }

    getNextSmoothedDistance() {
        return EMAFilter.filter(this.lastPacket, this.currentPacket);
    }

    isMotionDetected() {
        return (this.currentPacket.distance - this.lastPacket.distance) > 20;
    }
}