// Gritify Frontend JavaScript

// Global variables
let scene, camera, renderer, controls, currentMesh;
const API_BASE = window.location.origin;

// Initialize Three.js viewer
function initViewer() {
    const container = document.getElementById('viewer');
    const width = container.clientWidth;
    const height = container.clientHeight;
    
    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f5f5);
    
    // Camera
    camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 2000);
    camera.position.set(100, 100, 100);
    
    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    container.appendChild(renderer.domElement);
    
    // Controls
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    
    // Lights
    const ambientLight = new THREE.AmbientLight(0x404040, 2);
    scene.add(ambientLight);
    
    const directionalLight1 = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight1.position.set(1, 1, 1);
    scene.add(directionalLight1);
    
    const directionalLight2 = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight2.position.set(-1, -1, -1);
    scene.add(directionalLight2);
    
    // Grid helper
    const gridHelper = new THREE.GridHelper(200, 20);
    scene.add(gridHelper);
    
    // Animation loop
    animate();
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

// Load and display STL
function loadSTL(filename) {
    const loader = new THREE.STLLoader();
    const url = `${API_BASE}/api/download/${filename}`;
    
    // Remove existing mesh
    if (currentMesh) {
        scene.remove(currentMesh);
    }
    
    loader.load(url, function(geometry) {
        const material = new THREE.MeshPhongMaterial({
            color: 0x667eea,
            specular: 0x111111,
            shininess: 200
        });
        
        currentMesh = new THREE.Mesh(geometry, material);
        
        // Center the geometry
        geometry.computeBoundingBox();
        const center = new THREE.Vector3();
        geometry.boundingBox.getCenter(center);
        geometry.translate(-center.x, -center.y, -geometry.boundingBox.min.z);
        
        scene.add(currentMesh);
        
        // Adjust camera
        const box = new THREE.Box3().setFromObject(currentMesh);
        const size = box.getSize(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z);
        const fov = camera.fov * (Math.PI / 180);
        let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2));
        cameraZ *= 1.5;
        
        camera.position.set(cameraZ, cameraZ, cameraZ);
        camera.lookAt(0, 0, 0);
        controls.target.set(0, 0, 0);
        controls.update();
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
        loadSTL(result.filename);
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
        loadSTL(result.filename);
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
        loadSTL(result.filename);
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
            bed_width: parseFloat(document.getElementById('pb-bed-width').value),
            bed_depth: parseFloat(document.getElementById('pb-bed-depth').value)
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
    initViewer();
    setupTabs();
    
    // Attach event listeners
    document.getElementById('generate-grid').addEventListener('click', generateGrid);
    document.getElementById('generate-box').addEventListener('click', generateBox);
    document.getElementById('generate-inlay').addEventListener('click', generateInlay);
    document.getElementById('calculate-printbed').addEventListener('click', calculatePrintbed);
    
    // Handle window resize
    window.addEventListener('resize', () => {
        const container = document.getElementById('viewer');
        const width = container.clientWidth;
        const height = container.clientHeight;
        
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    });
});
