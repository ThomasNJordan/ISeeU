import { Point } from "./Point";

class FramePointBuffer {
    scene;
    points;

    constructor() {
        this.points = [];
    }

    setScene(scene) {
        this.scene = scene;
    }

    addPoint(distance) {
        const point = new Point(distance);
        this.points.push(point);
    }

    flush() {
        for (const point of this.points) {
            point.render(this.scene);
        }
        this.points = this.points.filter(point => !point.isDead());
    }
}

export const framePointBuffer = new FramePointBuffer();