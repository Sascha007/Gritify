// Gritify Frontend JavaScript
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';

// Global variables
const API_BASE = window.location.origin;
let currentDownloadUrl = null;
let scene, camera, renderer, controls;
let currentMesh = null;
let wireframeMode = false;

// Color constants
const MODEL_COLOR = 0x667eea;

// Material properties constants
const SOLID_MATERIAL_PROPS = {
    color: MODEL_COLOR,
    specular: 0x444444,
    shininess: 100,
    flatShading: false
};

// UI text constants
const WIREFRAME_BUTTON_TEXT = {
    solid: '🔲 Wireframe View',
    wireframe: '🔲 Solid View'
};

// Initialize Three.js viewer
function initViewer() {
    const container = document.getElementById('viewer');
    const width = container.clientWidth || 800; // Fallback dimensions
    const height = container.clientHeight || 600;
    
    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f5f5);
    
    // Camera
    camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(100, 100, 100);
    camera.lookAt(0, 0, 0);
    
    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);
    
    // Controls
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.screenSpacePanning = false;
    controls.minDistance = 10;
    controls.maxDistance = 500;
    
    // Enhanced Lights for better depth perception and contrast
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    const directionalLight1 = new THREE.DirectionalLight(0xffffff, 1.0);
    directionalLight1.position.set(1, 1, 1);
    directionalLight1.castShadow = true;
    // Configure shadow camera bounds for better shadow quality
    directionalLight1.shadow.camera.left = -100;
    directionalLight1.shadow.camera.right = 100;
    directionalLight1.shadow.camera.top = 100;
    directionalLight1.shadow.camera.bottom = -100;
    directionalLight1.shadow.camera.near = 0.5;
    directionalLight1.shadow.camera.far = 500;
    directionalLight1.shadow.mapSize.width = 2048;
    directionalLight1.shadow.mapSize.height = 2048;
    scene.add(directionalLight1);
    
    const directionalLight2 = new THREE.DirectionalLight(0xffffff, 0.6);
    directionalLight2.position.set(-1, 0.5, -0.5);
    scene.add(directionalLight2);
    
    // Add rim light for better edge definition
    const rimLight = new THREE.DirectionalLight(0xffffff, 0.4);
    rimLight.position.set(0, -1, 0);
    scene.add(rimLight);
    
    // Grid helper
    const gridHelper = new THREE.GridHelper(200, 20, 0xcccccc, 0xeeeeee);
    scene.add(gridHelper);
    
    // Axes helper
    const axesHelper = new THREE.AxesHelper(50);
    scene.add(axesHelper);
    
    // Handle window resize
    window.addEventListener('resize', onWindowResize);
    
    // Start animation loop
    animate();
}

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

// Window resize handler
function onWindowResize() {
    const container = document.getElementById('viewer');
    const width = container.clientWidth;
    const height = container.clientHeight;
    
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
}

// Load and display STL file
async function loadSTL(filename) {
    const loader = new STLLoader();
    const url = `${API_BASE}/api/download/${filename}`;
    
    return new Promise((resolve, reject) => {
        loader.load(
            url,
            (geometry) => {
                // Remove previous mesh if exists
                if (currentMesh) {
                    scene.remove(currentMesh);
                    currentMesh.geometry.dispose();
                    currentMesh.material.dispose();
                }
                
                // Create material with improved reflection and contrast
                const material = new THREE.MeshPhongMaterial(SOLID_MATERIAL_PROPS);
                
                // Create mesh
                currentMesh = new THREE.Mesh(geometry, material);
                currentMesh.castShadow = true;
                currentMesh.receiveShadow = true;
                
                // Center the geometry
                geometry.computeBoundingBox();
                const center = new THREE.Vector3();
                geometry.boundingBox.getCenter(center);
                geometry.translate(-center.x, -center.y, -center.z);
                
                // Add to scene
                scene.add(currentMesh);
                
                // Reset wireframe mode when loading new model
                resetWireframeState();
                
                // Adjust camera to fit model
                const box = new THREE.Box3().setFromObject(currentMesh);
                const size = box.getSize(new THREE.Vector3());
                const maxDim = Math.max(size.x, size.y, size.z);
                const fov = camera.fov * (Math.PI / 180);
                let cameraDistance = Math.abs(maxDim / Math.sin(fov / 2));
                
                // Clamp camera distance to reasonable bounds
                cameraDistance = Math.max(10, Math.min(cameraDistance, 500));
                
                camera.position.set(cameraDistance, cameraDistance, cameraDistance);
                camera.lookAt(0, 0, 0);
                controls.update();
                
                // Hide placeholder
                const placeholder = document.getElementById('viewer-placeholder');
                if (placeholder) {
                    placeholder.style.display = 'none';
                }
                
                resolve();
            },
            undefined, // Progress callback - removed for production
            (error) => {
                console.error('Error loading STL:', error);
                reject(error);
            }
        );
    });
}

// Reset wireframe state to default
function resetWireframeState() {
    wireframeMode = false;
    const wireframeButton = document.getElementById('wireframe-toggle');
    if (wireframeButton) {
        wireframeButton.textContent = WIREFRAME_BUTTON_TEXT.solid;
    }
}

// Toggle wireframe mode
function toggleWireframe() {
    if (!currentMesh) return;
    
    wireframeMode = !wireframeMode;
    
    // Update button text
    const button = document.getElementById('wireframe-toggle');
    if (!button) return;
    
    button.textContent = wireframeMode ? WIREFRAME_BUTTON_TEXT.wireframe : WIREFRAME_BUTTON_TEXT.solid;
    
    // Dispose old material and create new one
    const oldMaterial = currentMesh.material;
    
    if (wireframeMode) {
        // Create wireframe material
        currentMesh.material = new THREE.MeshBasicMaterial({
            color: MODEL_COLOR,
            wireframe: true,
            transparent: true,
            opacity: 0.8
        });
    } else {
        // Restore solid material
        currentMesh.material = new THREE.MeshPhongMaterial(SOLID_MATERIAL_PROPS);
        // Restore shadow properties
        currentMesh.castShadow = true;
        currentMesh.receiveShadow = true;
    }
    
    // Dispose old material after assignment
    oldMaterial.dispose();
}

// Show download section
function showDownload(filename, downloadUrl, dimensions) {
    const downloadSection = document.getElementById('download-section');
    const filenameEl = document.getElementById('filename');
    const downloadLink = document.getElementById('download-link');
    
    filenameEl.textContent = filename;
    downloadLink.href = downloadUrl;
    
    // Display dimensions if provided
    if (dimensions) {
        document.getElementById('dim-x').textContent = dimensions.x.toFixed(1);
        document.getElementById('dim-y').textContent = dimensions.y.toFixed(1);
        document.getElementById('dim-z').textContent = dimensions.z.toFixed(1);
        document.getElementById('dimensions-info').style.display = 'block';
    } else {
        document.getElementById('dimensions-info').style.display = 'none';
    }
    
    downloadSection.style.display = 'block';
    currentDownloadUrl = downloadUrl;
    
    // Load STL in viewer
    loadSTL(filename).catch(error => {
        console.error('Failed to load STL preview:', error);
        showMessage('Model generated but preview failed to load', 'error');
    });
}

// Show message
function showMessage(message, type = 'success') {
    const messageEl = document.getElementById('message');
    messageEl.textContent = message;
    messageEl.className = `message ${type} show`;
    
    setTimeout(() => {
        messageEl.classList.remove('show');
    }, 5000);
}

// Tab switching
function setupTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.dataset.tab;
            
            // Update buttons
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Update content
            tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(`${tabName}-tab`).classList.add('active');
        });
    });
}

// API call wrapper
async function apiCall(endpoint, data) {
    try {
        const response = await fetch(`${API_BASE}/api/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'API request failed');
        }
        
        return result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Generate Grid
async function generateGrid() {
    const button = document.getElementById('generate-grid');
    button.disabled = true;
    button.textContent = 'Generating...';
    
    try {
        const data = {
            width: parseInt(document.getElementById('grid-width').value),
            depth: parseInt(document.getElementById('grid-depth').value),
            include_base: document.getElementById('grid-base').checked
        };
        
        const result = await apiCall('generate/grid', data);
        
        showMessage('Grid generated successfully!', 'success');
        showDownload(result.filename, result.download_url, result.dimensions);
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    } finally {
        button.disabled = false;
        button.textContent = 'Generate Grid';
    }
}

// Generate Box
async function generateBox() {
    const button = document.getElementById('generate-box');
    button.disabled = true;
    button.textContent = 'Generating...';
    
    try {
        const data = {
            width: parseInt(document.getElementById('box-width').value),
            depth: parseInt(document.getElementById('box-depth').value),
            height: parseInt(document.getElementById('box-height').value),
            wall_thickness: parseFloat(document.getElementById('box-wall').value)
        };
        
        const result = await apiCall('generate/box', data);
        
        showMessage('Box generated successfully!', 'success');
        showDownload(result.filename, result.download_url, result.dimensions);
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    } finally {
        button.disabled = false;
        button.textContent = 'Generate Box';
    }
}

// Generate Inlay Box
async function generateInlay() {
    const button = document.getElementById('generate-inlay');
    button.disabled = true;
    button.textContent = 'Generating...';
    
    try {
        const data = {
            width: parseInt(document.getElementById('inlay-width').value),
            depth: parseInt(document.getElementById('inlay-depth').value),
            height: parseInt(document.getElementById('inlay-height').value),
            divisions_x: parseInt(document.getElementById('inlay-div-x').value),
            divisions_y: parseInt(document.getElementById('inlay-div-y').value),
            wall_thickness: parseFloat(document.getElementById('inlay-wall').value)
        };
        
        const result = await apiCall('generate/inlay', data);
        
        showMessage('Inlay box generated successfully!', 'success');
        showDownload(result.filename, result.download_url, result.dimensions);
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    } finally {
        button.disabled = false;
        button.textContent = 'Generate Inlay Box';
    }
}

// Calculate Printbed Breakdown
async function calculatePrintbed() {
    const button = document.getElementById('calculate-printbed');
    button.disabled = true;
    button.textContent = 'Calculating...';
    
    try {
        const data = {
            total_width: parseInt(document.getElementById('pb-width').value),
            total_depth: parseInt(document.getElementById('pb-depth').value),
            bed_length_x: parseFloat(document.getElementById('pb-bed-length-x').value),
            bed_length_y: parseFloat(document.getElementById('pb-bed-length-y').value)
        };
        
        const result = await apiCall('printbed/calculate', data);
        const breakdown = result.breakdown;
        
        let html = '<div class="info-box">';
        html += '<h3>Breakdown Result</h3>';
        
        if (breakdown.fits_bed) {
            html += '<p style="color: green; font-weight: bold;">✓ Fits on printer bed!</p>';
        } else {
            html += '<p style="color: orange; font-weight: bold;">⚠ Needs to be split into pieces</p>';
        }
        
        html += `<p><strong>Total Pieces:</strong> ${breakdown.total_pieces}</p>`;
        html += `<p><strong>Grid:</strong> ${breakdown.pieces_x} × ${breakdown.pieces_y}</p>`;
        html += `<p><strong>Piece Size:</strong> ${breakdown.piece_width.toFixed(1)} × ${breakdown.piece_depth.toFixed(1)} units</p>`;
        html += `<p><strong>Piece Size (mm):</strong> ${breakdown.piece_width_mm.toFixed(1)} × ${breakdown.piece_depth_mm.toFixed(1)} mm</p>`;
        
        // Show half grid and spacer information
        if (breakdown.uses_half_grids) {
            html += '<p style="color: blue;">✓ Using half grids (0.5 unit increments)</p>';
        }
        
        if (breakdown.uses_spacers) {
            html += '<p style="color: blue;">✓ Using spacers to fill remaining space</p>';
            html += `<p><strong>Spacer X:</strong> ${breakdown.spacer_x.toFixed(2)} units (${breakdown.spacer_x_mm.toFixed(1)} mm)</p>`;
            html += `<p><strong>Spacer Y:</strong> ${breakdown.spacer_y.toFixed(2)} units (${breakdown.spacer_y_mm.toFixed(1)} mm)</p>`;
        }
        
        html += '</div>';
        
        document.getElementById('printbed-result').innerHTML = html;
        showMessage('Breakdown calculated successfully!', 'success');
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    } finally {
        button.disabled = false;
        button.textContent = 'Calculate Breakdown';
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    setupTabs();
    initViewer();
    
    // Attach event listeners
    document.getElementById('generate-grid').addEventListener('click', generateGrid);
    document.getElementById('generate-box').addEventListener('click', generateBox);
    document.getElementById('generate-inlay').addEventListener('click', generateInlay);
    document.getElementById('calculate-printbed').addEventListener('click', calculatePrintbed);
    document.getElementById('wireframe-toggle').addEventListener('click', toggleWireframe);
});
