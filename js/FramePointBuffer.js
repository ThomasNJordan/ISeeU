import { Point } from "./Point";

export class FramePointBuffer {
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

    generateTestPoints() {
        for (let i = 0; i < 3; i++) {
            const distance = Math.random() * 20;
            this.addPoint(distance);
        }
    }
}

export const framePointBuffer = new FramePointBuffer();