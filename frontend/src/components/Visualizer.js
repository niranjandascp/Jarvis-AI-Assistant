import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { gsap } from 'gsap';

const Visualizer = ({ active }) => {
    const mountRef = useRef(null);

    useEffect(() => {
        // Scene setup
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        
        renderer.setSize(200, 200);
        mountRef.current.appendChild(renderer.domElement);

        // Core Reactor Geometry
        const geometry = new THREE.IcosahedronGeometry(1, 2);
        const material = new THREE.MeshPhongMaterial({
            color: 0x00f2ff,
            wireframe: true,
            emissive: 0x00f2ff,
            emissiveIntensity: 0.5,
            transparent: true,
            opacity: 0.8
        });
        
        const core = new THREE.Mesh(geometry, material);
        scene.add(core);

        // Inner Glow
        const innerGeo = new THREE.SphereGeometry(0.6, 32, 32);
        const innerMat = new THREE.MeshBasicMaterial({ color: 0x00f2ff });
        const innerSphere = new THREE.Mesh(innerGeo, innerMat);
        scene.add(innerSphere);

        // Lights
        const light = new THREE.PointLight(0x00f2ff, 2, 10);
        light.position.set(2, 2, 2);
        scene.add(light);
        scene.add(new THREE.AmbientLight(0x404040));

        camera.position.z = 3;

        // Animation Loop
        const animate = () => {
            requestAnimationFrame(animate);
            core.rotation.x += 0.01;
            core.rotation.y += 0.01;
            
            if (active) {
                gsap.to(core.scale, { x: 1.2, y: 1.2, z: 1.2, duration: 0.2 });
                gsap.to(material, { emissiveIntensity: 2, duration: 0.2 });
            } else {
                gsap.to(core.scale, { x: 1, y: 1, z: 1, duration: 0.5 });
                gsap.to(material, { emissiveIntensity: 0.5, duration: 0.5 });
            }
            
            renderer.render(scene, camera);
        };

        animate();

        // Cleanup
        return () => {
            mountRef.current?.removeChild(renderer.domElement);
        };
    }, []);

    useEffect(() => {
        // Pre-load logic: We can trigger a GSAP sequence here
        gsap.fromTo(mountRef.current, { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 1, ease: "expo.out" });
    }, []);

    return <div ref={mountRef} className="three-container" />;
};

export default Visualizer;
