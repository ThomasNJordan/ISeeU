import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader';
import { framePointBuffer } from './FramePointBuffer';
import { ServerListener } from './serverListener';

// Scene Setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x202020);

const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
// camera.position.set(-2.5, 3, 5);
camera.position.set(4.5, 3, 5);
camera.rotation.set(-Math.PI/6, 0, 0);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Orbit Controls
// const controls = new OrbitControls(camera, renderer.domElement);

// Router Model
const objLoader = new OBJLoader();
objLoader.load('../models/router.obj', (object) => {
	object.scale.set(5, 5, 5);
	object.position.set(0.25, -0.5, 1.5);
	object.rotation.set(0, -Math.PI/2, 0);
	scene.add(object);
});

// Infinite Floor (Grid Helper)
const gridHelper = new THREE.GridHelper(100, 100, 0x808080, 0x404040);
gridHelper.position.y = -0.5;
scene.add(gridHelper);

// Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 10, 7.5);
scene.add(directionalLight);

// Handle Window Resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth/window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

framePointBuffer.setScene(scene);

// Open Server Listener
const listener = new ServerListener();

// Animate Loop
function animate() {
	requestAnimationFrame(animate);

	// listener.generateTestPackets();
	framePointBuffer.flush();

	// controls.update();
	renderer.render(scene, camera);
}
animate();
