// Gritify Frontend JavaScript

// Global variables
const API_BASE = window.location.origin;
let currentDownloadUrl = null;

// Show download section
function showDownload(filename, downloadUrl) {
    const downloadSection = document.getElementById('download-section');
    const filenameEl = document.getElementById('filename');
    const downloadLink = document.getElementById('download-link');
    const placeholder = document.getElementById('viewer-placeholder');
    
    filenameEl.textContent = filename;
    downloadLink.href = downloadUrl;
    downloadSection.style.display = 'block';
    if (placeholder) {
        placeholder.style.display = 'none';
    }
    currentDownloadUrl = downloadUrl;
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
        showDownload(result.filename, result.download_url);
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
        showDownload(result.filename, result.download_url);
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
        showDownload(result.filename, result.download_url);
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
    setupTabs();
    
    // Attach event listeners
    document.getElementById('generate-grid').addEventListener('click', generateGrid);
    document.getElementById('generate-box').addEventListener('click', generateBox);
    document.getElementById('generate-inlay').addEventListener('click', generateInlay);
    document.getElementById('calculate-printbed').addEventListener('click', calculatePrintbed);
});
