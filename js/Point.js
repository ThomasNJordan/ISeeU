import * as THREE from 'three';

export class Point {
    constructor(distance) {
        this.distance = distance;
        this.isRendered = false;
        this.lifetime = 60*10;
        this.dot = null;
    }

    calculateX() {
        return this.distance / 10;
    }

    calculateY() {
        return 0;
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
        this.dot.position.set(this.calculateX(), 0, this.calculateY());
        scene.add(this.dot);
        this.isRendered = true;
    }
}