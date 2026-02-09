// Main JavaScript for the Transparent AI Agent UI

const API_BASE = '';

// DOM Elements
const instructionInput = document.getElementById('instructionInput');
const executeBtn = document.getElementById('executeBtn');
const outputContainer = document.getElementById('outputContainer');
const historyContainer = document.getElementById('historyContainer');
const clearHistoryBtn = document.getElementById('clearHistoryBtn');
const refreshHistoryBtn = document.getElementById('refreshHistoryBtn');
const statusText = document.getElementById('statusText');

// Event Listeners
executeBtn.addEventListener('click', executeInstruction);
instructionInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        executeInstruction();
    }
});
clearHistoryBtn.addEventListener('click', clearHistory);
refreshHistoryBtn.addEventListener('click', loadHistory);

// Execute instruction
async function executeInstruction() {
    const instruction = instructionInput.value.trim();
    
    if (!instruction) {
        return;
    }
    
    // Update UI
    executeBtn.disabled = true;
    statusText.textContent = 'Executing...';
    
    try {
        const response = await fetch(`${API_BASE}/api/instruct`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ instruction: instruction })
        });
        
        if (!response.ok) {
            throw new Error('Failed to execute instruction');
        }
        
        const result = await response.json();
        displayOutput(result);
        
        // Clear input
        instructionInput.value = '';
        
        // Refresh history
        loadHistory();
        
    } catch (error) {
        displayError(error.message);
    } finally {
        executeBtn.disabled = false;
        statusText.textContent = 'Ready';
    }
}

// Display output
function displayOutput(result) {
    // Remove empty state if present
    const emptyState = outputContainer.querySelector('.empty-state');
    if (emptyState) {
        emptyState.remove();
    }
    
    const outputItem = document.createElement('div');
    outputItem.className = `output-item ${result.status}`;
    
    const statusBadge = result.status === 'success' ? 
        '<span class="status-badge success">SUCCESS</span>' :
        '<span class="status-badge error">ERROR</span>';
    
    outputItem.innerHTML = `
        <div class="output-header">
            <strong>Execution Result</strong>
            ${statusBadge}
        </div>
        <div class="output-detail">
            <strong>Original Instruction:</strong> ${escapeHtml(result.original_instruction || result.command)}
        </div>
        <div class="output-detail">
            <strong>Interpreted Command:</strong> ${escapeHtml(result.interpreted_command || result.command)}
        </div>
        <div class="output-detail">
            <strong>Timestamp:</strong> ${formatTimestamp(result.timestamp)}
        </div>
        <div class="output-detail">
            <strong>Return Code:</strong> ${result.return_code}
        </div>
        <div class="output-detail">
            <strong>Output:</strong>
        </div>
        <div class="output-text">${escapeHtml(result.output)}</div>
    `;
    
    // Insert at the top
    outputContainer.insertBefore(outputItem, outputContainer.firstChild);
}

// Display error
function displayError(message) {
    const emptyState = outputContainer.querySelector('.empty-state');
    if (emptyState) {
        emptyState.remove();
    }
    
    const errorItem = document.createElement('div');
    errorItem.className = 'output-item error';
    errorItem.innerHTML = `
        <div class="output-header">
            <strong>Error</strong>
            <span class="status-badge error">ERROR</span>
        </div>
        <div class="output-text">${escapeHtml(message)}</div>
    `;
    
    outputContainer.insertBefore(errorItem, outputContainer.firstChild);
}

// Load history
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE}/api/history`);
        
        if (!response.ok) {
            throw new Error('Failed to load history');
        }
        
        const history = await response.json();
        displayHistory(history);
        
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// Display history
function displayHistory(history) {
    historyContainer.innerHTML = '';
    
    if (history.length === 0) {
        historyContainer.innerHTML = '<div class="empty-state">No actions recorded yet.</div>';
        return;
    }
    
    // Show most recent first
    history.reverse().forEach((item, index) => {
        const historyItem = document.createElement('div');
        historyItem.className = `history-item ${item.status}`;
        
        const resultPreview = item.result.length > 100 ? 
            item.result.substring(0, 100) + '...' : 
            item.result;
        
        historyItem.innerHTML = `
            <div class="history-timestamp">${formatTimestamp(item.timestamp)}</div>
            <div class="history-command"><strong>Command:</strong> ${escapeHtml(item.command)}</div>
            <div><strong>Status:</strong> ${item.status.toUpperCase()}</div>
            <div><strong>Result:</strong> ${escapeHtml(resultPreview)}</div>
        `;
        
        historyContainer.appendChild(historyItem);
    });
}

// Clear history
async function clearHistory() {
    if (!confirm('Are you sure you want to clear all history?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/history`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to clear history');
        }
        
        // Clear UI
        historyContainer.innerHTML = '<div class="empty-state">No actions recorded yet.</div>';
        outputContainer.innerHTML = '<div class="empty-state">No commands executed yet. Enter an instruction above to get started.</div>';
        
    } catch (error) {
        alert('Error clearing history: ' + error.message);
    }
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
}

// Load history on page load
document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
    
    // Focus on input
    instructionInput.focus();
});
