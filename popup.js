// State management
let state = {
  promptsData: null,
  ingredientsData: null,
  baseCatImages: null, // Store base cat image files
  isRunning: false,
  currentProgress: {
    prompts: 0,
    totalPrompts: 0,
    ingredients: 0,
    totalIngredients: 0,
    videos: 0
  },
  logs: []
};

// DOM elements
const elements = {
  promptsFile: document.getElementById('promptsFile'),
  ingredientsFile: document.getElementById('ingredientsFile'),
  baseCatFiles: document.getElementById('baseCatFiles'),
  promptsFileName: document.getElementById('promptsFileName'),
  ingredientsFileName: document.getElementById('ingredientsFileName'),
  baseCatFilesName: document.getElementById('baseCatFilesName'),
  projectName: document.getElementById('projectName'),
  maxConcurrent: document.getElementById('maxConcurrent'),
  reverseOrder: document.getElementById('reverseOrder'),
  wait50Percent: document.getElementById('wait50Percent'),
  startBtn: document.getElementById('startBtn'),
  stopBtn: document.getElementById('stopBtn'),
  exportReportBtn: document.getElementById('exportReportBtn'),
  clearLogBtn: document.getElementById('clearLogBtn'),
  statusBar: document.getElementById('statusBar'),
  statusText: document.getElementById('statusText'),
  progressSection: document.getElementById('progressSection'),
  logSection: document.getElementById('logSection'),
  promptsProgress: document.getElementById('promptsProgress'),
  ingredientsProgress: document.getElementById('ingredientsProgress'),
  videosProgress: document.getElementById('videosProgress'),
  progressFill: document.getElementById('progressFill'),
  currentTask: document.getElementById('currentTask'),
  logContainer: document.getElementById('logContainer')
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  loadSavedState();
  setupEventListeners();
  checkIfOnGoogleLabs();
});

function setupEventListeners() {
  // File uploads
  elements.promptsFile.addEventListener('change', (e) => handleFileUpload(e, 'prompts'));
  elements.ingredientsFile.addEventListener('change', (e) => handleFileUpload(e, 'ingredients'));
  elements.baseCatFiles.addEventListener('change', handleBaseCatUpload);
  
  // Buttons
  elements.startBtn.addEventListener('click', startGeneration);
  elements.stopBtn.addEventListener('click', stopGeneration);
  elements.exportReportBtn.addEventListener('click', exportReport);
  elements.clearLogBtn.addEventListener('click', clearLog);
  
  // Save config on change
  elements.projectName.addEventListener('input', saveState);
  elements.maxConcurrent.addEventListener('change', saveState);
  elements.reverseOrder.addEventListener('change', saveState);
  elements.wait50Percent.addEventListener('change', saveState);
}

async function handleFileUpload(event, type) {
  const file = event.target.files[0];
  if (!file) return;
  
  try {
    const data = await readExcelFile(file);
    
    if (type === 'prompts') {
      state.promptsData = data;
      elements.promptsFileName.textContent = file.name;
      addLog('success', `Prompts file loaded: ${file.name}`);
    } else {
      state.ingredientsData = data;
      elements.ingredientsFileName.textContent = file.name;
      addLog('success', `Ingredients file loaded: ${file.name}`);
    }
    
    updateStatus();
    saveState();
  } catch (error) {
    addLog('error', `Failed to read ${type} file: ${error.message}`);
  }
}

async function handleBaseCatUpload(event) {
  const files = Array.from(event.target.files);
  if (files.length === 0) return;
  
  try {
    // Convert files to base64 for storage and transfer
    const imageData = await Promise.all(files.map(async (file) => {
      const base64 = await fileToBase64(file);
      return {
        name: file.name,
        data: base64,
        type: file.type
      };
    }));
    
    // Sort by filename to ensure 01.jpeg comes before 02.jpeg
    imageData.sort((a, b) => a.name.localeCompare(b.name));
    
    state.baseCatImages = imageData;
    
    const fileNames = imageData.map(img => img.name).join(', ');
    elements.baseCatFilesName.textContent = fileNames;
    
    addLog('success', `Base cat images loaded: ${fileNames}`);
    addLog('info', `📸 Found ${imageData.length} base cat images`);
    
    // Validate we have the expected files
    const hasImage01 = imageData.some(img => img.name.includes('01'));
    const hasImage02 = imageData.some(img => img.name.includes('02'));
    
    if (hasImage01 && hasImage02) {
      addLog('success', '✅ Both base cat images detected (01 & 02)');
    } else {
      addLog('warning', '⚠️ Expected files: 01.jpeg (Mama Cat) and 02.jpeg (Kitten)');
    }
    
    updateStatus();
    saveState();
  } catch (error) {
    addLog('error', `Failed to load base cat images: ${error.message}`);
  }
}

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

function readExcelFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (e) => {
      try {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });
        
        // Parse all worksheets
        const result = {};
        workbook.SheetNames.forEach(sheetName => {
          const worksheet = workbook.Sheets[sheetName];
          result[sheetName] = XLSX.utils.sheet_to_json(worksheet);
        });
        
        resolve(result);
      } catch (error) {
        reject(error);
      }
    };
    
    reader.onerror = () => reject(new Error('Failed to read file'));
    reader.readAsArrayBuffer(file);
  });
}

async function startGeneration() {
  // Validation
  if (!state.promptsData) {
    addLog('error', 'Please upload prompts Excel file');
    return;
  }
  
  if (!state.ingredientsData) {
    addLog('error', 'Please upload ingredients Excel file');
    return;
  }
  
  if (!state.baseCatImages) {
    addLog('error', 'Please upload base cat images (01.jpeg, 02.jpeg)');
    return;
  }
  
  // Validate base cat images
  const hasImage01 = state.baseCatImages.some(img => img.name.includes('01'));
  const hasImage02 = state.baseCatImages.some(img => img.name.includes('02'));
  
  if (!hasImage01 || !hasImage02) {
    addLog('error', 'Missing base cat images. Need: 01.jpeg (Mama Cat) and 02.jpeg (Kitten)');
    return;
  }
  
  // Check if on Google Labs
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab.url.includes('labs.google')) {
    addLog('error', 'Please navigate to Google Labs Flow first');
    return;
  }
  
  // Prepare configuration
  const config = {
    projectName: elements.projectName.value || 'MamaCat Project',
    maxConcurrent: parseInt(elements.maxConcurrent.value),
    reverseOrder: elements.reverseOrder.checked,
    wait50Percent: elements.wait50Percent.checked,
    promptsData: state.promptsData,
    ingredientsData: state.ingredientsData,
    baseCatImages: state.baseCatImages // Include base cat images
  };
  
  // Update UI
  state.isRunning = true;
  elements.startBtn.style.display = 'none';
  elements.stopBtn.style.display = 'block';
  elements.exportReportBtn.style.display = 'block';
  elements.progressSection.style.display = 'block';
  elements.logSection.style.display = 'block';
  
  updateStatus('🚀 Generation started');
  addLog('info', '═══════════════════════════════════════');
  addLog('info', '🎬 STARTING VIDEO GENERATION');
  addLog('info', `📁 Project: ${config.projectName}`);
  addLog('info', `⚙️ Max Concurrent: ${config.maxConcurrent}`);
  addLog('info', `🔄 Reverse Order: ${config.reverseOrder ? 'Yes' : 'No'}`);
  addLog('info', `🐱 Base Cat Images: ${state.baseCatImages.length} files`);
  addLog('info', '═══════════════════════════════════════');
  
  // Send message to content script
  try {
    await chrome.tabs.sendMessage(tab.id, {
      action: 'startGeneration',
      config: config
    });
  } catch (error) {
    addLog('error', `Failed to start: ${error.message}`);
    stopGeneration();
  }
}

function stopGeneration() {
  state.isRunning = false;
  elements.startBtn.style.display = 'block';
  elements.stopBtn.style.display = 'none';
  
  updateStatus('⏹️ Stopped');
  addLog('warning', 'Generation stopped by user');
  
  // Send stop message to content script
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0]) {
      chrome.tabs.sendMessage(tabs[0].id, { action: 'stopGeneration' });
    }
  });
}

function updateProgress(data) {
  state.currentProgress = { ...state.currentProgress, ...data };
  
  const { prompts, totalPrompts, ingredients, totalIngredients, videos } = state.currentProgress;
  
  elements.promptsProgress.textContent = `${prompts}/${totalPrompts}`;
  elements.ingredientsProgress.textContent = `${ingredients}/${totalIngredients}`;
  elements.videosProgress.textContent = videos;
  
  // Update progress bar
  const totalProgress = totalPrompts > 0 ? (prompts / totalPrompts) * 100 : 0;
  elements.progressFill.style.width = `${totalProgress}%`;
}

function updateCurrentTask(task) {
  elements.currentTask.textContent = task;
}

function addLog(type, message) {
  const timestamp = new Date().toLocaleTimeString();
  const logEntry = {
    time: timestamp,
    type: type,
    message: message
  };
  
  state.logs.push(logEntry);
  
  const logElement = document.createElement('div');
  logElement.className = `log-entry log-${type}`;
  logElement.innerHTML = `<span class="log-time">[${timestamp}]</span>${message}`;
  
  elements.logContainer.appendChild(logElement);
  elements.logContainer.scrollTop = elements.logContainer.scrollHeight;
  
  // Limit log entries
  if (state.logs.length > 500) {
    state.logs.shift();
    elements.logContainer.removeChild(elements.logContainer.firstChild);
  }
}

function clearLog() {
  state.logs = [];
  elements.logContainer.innerHTML = '';
  addLog('info', 'Log cleared');
}

function updateStatus(text) {
  if (text) {
    elements.statusText.textContent = text;
  } else {
    const hasPrompts = state.promptsData !== null;
    const hasIngredients = state.ingredientsData !== null;
    const hasBaseCats = state.baseCatImages !== null;
    
    if (hasPrompts && hasIngredients && hasBaseCats) {
      elements.statusText.textContent = '✅ Ready to start';
    } else {
      const missing = [];
      if (!hasPrompts) missing.push('prompts');
      if (!hasIngredients) missing.push('ingredients');
      if (!hasBaseCats) missing.push('base cat images');
      elements.statusText.textContent = `⚠️ Upload ${missing.join(', ')}`;
    }
  }
}

function checkIfOnGoogleLabs() {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0] && tabs[0].url.includes('labs.google')) {
      addLog('success', 'Connected to Google Labs');
    } else {
      addLog('warning', 'Not on Google Labs - navigate to labs.google/fx/tools/flow');
    }
  });
}

function exportReport() {
  const report = generateReport();
  const blob = new Blob([report], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.href = url;
  a.download = `MamaCat_Report_${new Date().toISOString().slice(0, 10)}.txt`;
  a.click();
  
  URL.revokeObjectURL(url);
  addLog('success', 'Report exported');
}

function generateReport() {
  const lines = [];
  lines.push('╔═══════════════════════════════════════════════════════════╗');
  lines.push('║         MAMACAT VIDEO GENERATION REPORT                  ║');
  lines.push('╚═══════════════════════════════════════════════════════════╝');
  lines.push('');
  lines.push(`📅 Date: ${new Date().toLocaleString()}`);
  lines.push(`📁 Project: ${elements.projectName.value || 'N/A'}`);
  lines.push('');
  lines.push('📊 STATISTICS');
  lines.push('─────────────────────────────────────────────────────────');
  lines.push(`Prompts Processed: ${state.currentProgress.prompts}/${state.currentProgress.totalPrompts}`);
  lines.push(`Ingredients Used: ${state.currentProgress.ingredients}/${state.currentProgress.totalIngredients}`);
  lines.push(`Videos Generated: ${state.currentProgress.videos}`);
  lines.push('');
  lines.push('📝 ACTIVITY LOG');
  lines.push('─────────────────────────────────────────────────────────');
  
  state.logs.forEach(log => {
    lines.push(`[${log.time}] [${log.type.toUpperCase()}] ${log.message}`);
  });
  
  lines.push('');
  lines.push('╔═══════════════════════════════════════════════════════════╗');
  lines.push('║                    END OF REPORT                          ║');
  lines.push('╚═══════════════════════════════════════════════════════════╝');
  
  return lines.join('\n');
}

function saveState() {
  const stateToSave = {
    projectName: elements.projectName.value,
    maxConcurrent: elements.maxConcurrent.value,
    reverseOrder: elements.reverseOrder.checked,
    wait50Percent: elements.wait50Percent.checked
  };
  
  chrome.storage.local.set({ mamacatState: stateToSave });
}

function loadSavedState() {
  chrome.storage.local.get(['mamacatState'], (result) => {
    if (result.mamacatState) {
      const saved = result.mamacatState;
      elements.projectName.value = saved.projectName || '';
      elements.maxConcurrent.value = saved.maxConcurrent || 8;
      elements.reverseOrder.checked = saved.reverseOrder !== false;
      elements.wait50Percent.checked = saved.wait50Percent !== false;
    }
  });
}

// Listen for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  switch (message.action) {
    case 'updateProgress':
      updateProgress(message.data);
      break;
    case 'updateTask':
      updateCurrentTask(message.task);
      break;
    case 'log':
      addLog(message.type, message.message);
      break;
    case 'generationComplete':
      stopGeneration();
      updateStatus('✅ Generation complete');
      addLog('success', '🎉 All videos generated successfully!');
      break;
    case 'generationError':
      stopGeneration();
      updateStatus('❌ Error occurred');
      addLog('error', `Generation failed: ${message.error}`);
      break;
  }
});
