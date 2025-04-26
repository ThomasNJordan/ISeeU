import * as THREE from 'three';

export class Point {
    constructor(distance) {
        this.theta = 0;
        this.distance = distance;
        this.x = this.calculateX();
        this.y = this.calculateY();
        this.isRendered = false;
        this.lifetime = 60;
        this.dot = null;
    }

    calculateX() {
        return this.distance * Math.cos(this.theta * Math.PI / 180);
    }

    calculateY() {
        return this.distance * Math.sin(this.theta * Math.PI / 180);
    }

    isDead() {
        return this.lifetime < 0;
    }

    render(scene) {
        this.lifetime -= 1;
        if (this.isDead()) {
            scene.remove(this.dot);
            return;
        }
        if (this.isRendered)
            return;
        const dotGeometry = new THREE.SphereGeometry(0.05, 16, 16);
        const dotMaterial = new THREE.MeshBasicMaterial({ color: 0xff5555 });
        this.dot = new THREE.Mesh(dotGeometry, dotMaterial);
        this.dot.position.set(this.x, 0, this.y);
        scene.add(this.dot);
        this.isRendered = true;
    }
}