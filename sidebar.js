// Sidebar JavaScript - Main Logic
console.log('🎬 MamaCat Sidebar Loaded');
console.log('[SIDEBAR] Chrome APIs available:', {
  tabs: !!chrome.tabs,
  runtime: !!chrome.runtime,
  scripting: !!chrome.scripting,
  storage: !!chrome.storage
});

// State Management
const state = {
  folderHandle: null,
  promptsData: null,
  ingredientsData: null,
  baseCat01: null,
  baseCat02: null,
  verified: false,
  stories: [],
  selectedStories: [],
  isRunning: false,
  scannedFiles: {
    promptsExcel: null,
    ingredientsExcel: null,
    baseCat01: null,
    baseCat02: null
  },
  currentProgress: {
    stories: 0,
    totalStories: 0,
    prompts: 0,
    totalPrompts: 0,
    videos: 0
  }
};

// DOM Elements
const elements = {
  // File selection
  selectAllFilesBtn: document.getElementById('selectAllFilesBtn'),
  allFilesInput: document.getElementById('allFilesInput'),
  scanFolderBtn: document.getElementById('scanFolderBtn'),
  changeFolderBtn: document.getElementById('changeFolderBtn'),
  folderInfo: document.getElementById('folderInfo'),
  folderName: document.getElementById('folderName'),
  scanResults: document.getElementById('scanResults'),
  scanResultsContent: document.getElementById('scanResultsContent'),
  
  // Buttons
  openFlowBtn: document.getElementById('openFlowBtn'),
  setupBtn: document.getElementById('setupBtn'),
  startBtn: document.getElementById('startBtn'),
  stopBtn: document.getElementById('stopBtn'),
  clearLogBtn: document.getElementById('clearLogBtn'),
  clearLogBtn2: document.getElementById('clearLogBtn2'),
  copyLogBtn: document.getElementById('copyLogBtn'),
  exportReportBtn: document.getElementById('exportReportBtn'),
  
  // Sections
  setupSection: document.getElementById('setupSection'),
  storiesSection: document.getElementById('storiesSection'),
  configSection: document.getElementById('configSection'),
  actionSection: document.getElementById('actionSection'),
  progressSection: document.getElementById('progressSection'),
  
  // Verification
  verificationResults: document.getElementById('verificationResults'),
  verificationContent: document.getElementById('verificationContent'),
  
  // Stories
  storiesList: document.getElementById('storiesList'),
  storySelection: document.getElementById('storySelection'),
  
  // Config
  maxConcurrent: document.getElementById('maxConcurrent'),
  reverseOrder: document.getElementById('reverseOrder'),
  wait50Percent: document.getElementById('wait50Percent'),
  
  // Progress
  storiesProgress: document.getElementById('storiesProgress'),
  promptsProgress: document.getElementById('promptsProgress'),
  videosProgress: document.getElementById('videosProgress'),
  progressBar: document.getElementById('progressBar'),
  currentTask: document.getElementById('currentTask'),
  
  // Status & Log
  statusDot: document.getElementById('statusDot'),
  statusText: document.getElementById('statusText'),
  logContainer: document.getElementById('logContainer')
};

// ═══════════════════════════════════════════════════════════
// UTILITY FUNCTIONS (Must be defined before use)
// ═══════════════════════════════════════════════════════════

// Logging
function addLog(type, message) {
  const timestamp = new Date().toLocaleTimeString();
  const logEntry = document.createElement('div');
  logEntry.className = `log-entry log-${type}`;
  logEntry.innerHTML = `<span class="log-time">[${timestamp}]</span>${message}`;
  
  if (elements.logContainer) {
    elements.logContainer.appendChild(logEntry);
    elements.logContainer.scrollTop = elements.logContainer.scrollHeight;
  } else {
    console.log(`[LOG-${type}]`, message);
  }
}

// Status Management
function updateStatus(type, message) {
  if (elements.statusDot && elements.statusText) {
    elements.statusDot.className = `status-dot ${type}`;
    elements.statusText.textContent = message;
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  console.log('[SIDEBAR] DOMContentLoaded - Initializing...');
  
  try {
    setupEventListeners();
    console.log('[SIDEBAR] Event listeners set up');
    
    checkGoogleLabsConnection();
    console.log('[SIDEBAR] Checked Google Labs connection');
    
    checkFileSystemAPISupport();
    console.log('[SIDEBAR] Checked file system support');
    
    addLog('info', '🎬 MamaCat Video Generator Ready');
    addLog('info', 'Please select all files to begin');
    console.log('[SIDEBAR] Initialization complete');
  } catch (error) {
    console.error('[SIDEBAR] Initialization error:', error);
    console.log('[SIDEBAR] Error details:', error.stack);
  }
});

// ═══════════════════════════════════════════════════════════
// FILE SELECTION (Multi-file upload)
// ═══════════════════════════════════════════════════════════

function checkFileSystemAPISupport() {
  addLog('info', '📁 Using multi-file selection (browser limitation workaround)');
  addLog('info', '💡 Select all 4 files at once: 2 Excel files + 2 images');
  return true;
}

async function handleAllFilesSelected(event) {
  const files = Array.from(event.target.files);
  
  if (files.length === 0) {
    addLog('warning', 'No files selected');
    return;
  }
  
  addLog('info', `📂 Processing ${files.length} files...`);
  
  const results = {
    promptsExcel: [],
    ingredientsExcel: [],
    baseCat01: null,
    baseCat02: null
  };
  
  // Process each file
  for (const file of files) {
    const fileName = file.name.toLowerCase();
    
    try {
      // Check for Excel files
      if (fileName.endsWith('.xlsx') || fileName.endsWith('.xls')) {
        addLog('info', `📊 Reading Excel: ${file.name}`);
        const fileData = await readExcelFile(file);
        const fileType = await detectExcelType(fileData, file.name);
        
        if (fileType === 'prompts') {
          results.promptsExcel.push({ file, data: fileData, name: file.name });
          addLog('success', `✅ Prompts Excel: ${file.name}`);
        } else if (fileType === 'ingredients') {
          results.ingredientsExcel.push({ file, data: fileData, name: file.name });
          addLog('success', `✅ Ingredients Excel: ${file.name}`);
        } else {
          addLog('warning', `⚠️ Unknown Excel type: ${file.name}`);
        }
      }
      
      // Check for base cat images
      if (fileName.match(/^01\.(jpg|jpeg|png)$/i)) {
        results.baseCat01 = file;
        addLog('success', `✅ Base Cat 01: ${file.name}`);
      }
      if (fileName.match(/^02\.(jpg|jpeg|png)$/i)) {
        results.baseCat02 = file;
        addLog('success', `✅ Base Cat 02: ${file.name}`);
      }
    } catch (error) {
      addLog('error', `Failed to process ${file.name}: ${error.message}`);
    }
  }
  
  // Display results
  displayScanResults(results);
  
  // Save to state if all files found
  if (results.promptsExcel.length > 0 && results.ingredientsExcel.length > 0 && 
      results.baseCat01 && results.baseCat02) {
    
    state.promptsData = results.promptsExcel[0].data;
    state.ingredientsData = results.ingredientsExcel[0].data;
    state.baseCat01 = results.baseCat01;
    state.baseCat02 = results.baseCat02;
    
    state.scannedFiles = {
      promptsExcel: results.promptsExcel[0],
      ingredientsExcel: results.ingredientsExcel[0],
      baseCat01: results.baseCat01,
      baseCat02: results.baseCat02
    };
    
    // Show results
    if (elements.folderInfo) elements.folderInfo.style.display = 'block';
    if (elements.folderName) elements.folderName.textContent = `${files.length} files loaded`;
    if (elements.scanResults) elements.scanResults.style.display = 'block';
    
    // Enable setup button
    elements.setupBtn.disabled = false;
    
    addLog('success', '✅ All required files found!');
    addLog('info', 'Click "Setup & Verify Files" to continue');
  } else {
    addLog('warning', '⚠️ Some required files are missing');
    addLog('info', 'Required: 2 Excel files (Prompts + Ingredients) + 2 images (01 + 02)');
  }
}



async function detectExcelType(data, fileName) {
  // Check worksheets for column patterns
  for (const sheetName in data) {
    const rows = data[sheetName];
    if (rows.length === 0) continue;
    
    const columns = Object.keys(rows[0]);
    
    // Prompts file has: Prompt, Ingredients_No
    if (columns.includes('Prompt') && columns.includes('Ingredients_No')) {
      return 'prompts';
    }
    
    // Ingredients file has: Ingredient_No, Title, Prompt
    if (columns.includes('Ingredient_No') && columns.includes('Title')) {
      return 'ingredients';
    }
  }
  
  return 'unknown';
}

function displayScanResults(results) {
  let html = '';
  
  // Prompts Excel
  if (results.promptsExcel.length > 0) {
    const file = results.promptsExcel[0];
    const worksheetCount = Object.keys(file.data).length;
    let totalPrompts = 0;
    for (const sheet in file.data) {
      totalPrompts += file.data[sheet].length;
    }
    
    html += `
      <div class="file-found">
        ✅ <strong>Prompts Excel:</strong> ${file.name}
        <div class="file-detail">📊 ${worksheetCount} worksheets, ${totalPrompts} total prompts</div>
      </div>
    `;
  } else {
    html += `
      <div class="file-error">
        ❌ <strong>Prompts Excel:</strong> Not found
        <div class="file-detail">Looking for Excel file with columns: Prompt, Ingredients_No</div>
      </div>
    `;
  }
  
  // Ingredients Excel
  if (results.ingredientsExcel.length > 0) {
    const file = results.ingredientsExcel[0];
    const worksheetCount = Object.keys(file.data).length;
    let totalIngredients = 0;
    for (const sheet in file.data) {
      totalIngredients += file.data[sheet].length;
    }
    
    html += `
      <div class="file-found">
        ✅ <strong>Ingredients Excel:</strong> ${file.name}
        <div class="file-detail">📊 ${worksheetCount} worksheets, ${totalIngredients} total ingredients</div>
      </div>
    `;
  } else {
    html += `
      <div class="file-error">
        ❌ <strong>Ingredients Excel:</strong> Not found
        <div class="file-detail">Looking for Excel file with columns: Ingredient_No, Title, Prompt</div>
      </div>
    `;
  }
  
  // Base Cat 01
  if (results.baseCat01) {
    const sizeKB = (results.baseCat01.size / 1024).toFixed(1);
    html += `
      <div class="file-found">
        ✅ <strong>Base Cat 01 (Mama Cat):</strong> ${results.baseCat01.name}
        <div class="file-detail">📸 ${sizeKB} KB</div>
      </div>
    `;
  } else {
    html += `
      <div class="file-error">
        ❌ <strong>Base Cat 01:</strong> Not found
        <div class="file-detail">Looking for: 01.jpg or 01.jpeg or 01.png</div>
      </div>
    `;
  }
  
  // Base Cat 02
  if (results.baseCat02) {
    const sizeKB = (results.baseCat02.size / 1024).toFixed(1);
    html += `
      <div class="file-found">
        ✅ <strong>Base Cat 02 (Kitten):</strong> ${results.baseCat02.name}
        <div class="file-detail">📸 ${sizeKB} KB</div>
      </div>
    `;
  } else {
    html += `
      <div class="file-error">
        ❌ <strong>Base Cat 02:</strong> Not found
        <div class="file-detail">Looking for: 02.jpg or 02.jpeg or 02.png</div>
      </div>
    `;
  }
  
  elements.scanResultsContent.innerHTML = html;
}



// Helper function to read Excel file
async function readExcelFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (e) => {
      try {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });
        
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

// Event Listeners
function setupEventListeners() {
  // File selection
  if (elements.selectAllFilesBtn) {
    elements.selectAllFilesBtn.addEventListener('click', () => {
      if (elements.allFilesInput) elements.allFilesInput.click();
    });
  }
  if (elements.allFilesInput) {
    elements.allFilesInput.addEventListener('change', handleAllFilesSelected);
  }
  
  // Buttons - with null checks
  if (elements.openFlowBtn) elements.openFlowBtn.addEventListener('click', openGoogleFlow);
  if (elements.setupBtn) elements.setupBtn.addEventListener('click', setupAndVerify);
  if (elements.startBtn) elements.startBtn.addEventListener('click', startGeneration);
  if (elements.stopBtn) elements.stopBtn.addEventListener('click', stopGeneration);
  if (elements.clearLogBtn) elements.clearLogBtn.addEventListener('click', clearLog);
  if (elements.clearLogBtn2) elements.clearLogBtn2.addEventListener('click', clearLog);
  if (elements.copyLogBtn) elements.copyLogBtn.addEventListener('click', copyLog);
  if (elements.exportReportBtn) elements.exportReportBtn.addEventListener('click', exportReport);
  
  // Quick select buttons
  document.querySelectorAll('.btn-quick').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const selection = e.target.dataset.select;
      if (elements.storySelection) elements.storySelection.value = selection;
    });
  });
  
  // Story selection input
  if (elements.storySelection) {
    elements.storySelection.addEventListener('input', validateStorySelection);
  }
}

// File Upload Handlers
async function handleFileUpload(event, type) {
  const file = event.target.files[0];
  if (!file) return;
  
  try {
    if (type === 'prompts' || type === 'ingredients') {
      const data = await readExcelFile(file);
      
      if (type === 'prompts') {
        state.promptsData = data;
        elements.promptsDisplay.textContent = file.name;
        elements.promptsDisplay.classList.add('has-file');
        addLog('success', `✅ Prompts file loaded: ${file.name}`);
      } else {
        state.ingredientsData = data;
        elements.ingredientsDisplay.textContent = file.name;
        elements.ingredientsDisplay.classList.add('has-file');
        addLog('success', `✅ Ingredients file loaded: ${file.name}`);
      }
    } else {
      // Base cat images
      const imageData = await fileToBase64(file);
      
      if (type === 'baseCat01') {
        state.baseCat01 = { name: '01.jpeg', data: imageData, type: file.type };
        elements.baseCat01Display.textContent = file.name;
        elements.baseCat01Display.classList.add('has-file');
        addLog('success', `✅ Base Cat 01 loaded: ${file.name}`);
      } else {
        state.baseCat02 = { name: '02.jpeg', data: imageData, type: file.type };
        elements.baseCat02Display.textContent = file.name;
        elements.baseCat02Display.classList.add('has-file');
        addLog('success', `✅ Base Cat 02 loaded: ${file.name}`);
      }
    }
    
    checkSetupReady();
  } catch (error) {
    addLog('error', `❌ Failed to load ${type}: ${error.message}`);
  }
}

function readExcelFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (e) => {
      try {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });
        
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

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

function checkSetupReady() {
  const ready = state.promptsData && state.ingredientsData && 
                state.baseCat01 && state.baseCat02;
  
  elements.setupBtn.disabled = !ready;
  
  if (ready) {
    updateStatus('ready', '✅ All files loaded - Ready to setup');
  }
}

// Setup and Verification
async function setupAndVerify() {
  addLog('info', '═══════════════════════════════════════');
  addLog('info', '🔍 SETUP & VERIFICATION STARTED');
  addLog('info', '═══════════════════════════════════════');
  
  updateStatus('working', '🔍 Verifying files...');
  
  const results = [];
  let hasErrors = false;
  
  // Check 1: Worksheet names match
  const promptSheets = Object.keys(state.promptsData);
  const ingredientSheets = Object.keys(state.ingredientsData);
  
  addLog('info', `📝 Found ${promptSheets.length} prompt worksheets`);
  addLog('info', `🎨 Found ${ingredientSheets.length} ingredient worksheets`);
  
  // Find matching worksheets
  const matchingSheets = promptSheets.filter(sheet => 
    ingredientSheets.includes(sheet)
  );
  
  if (matchingSheets.length === 0) {
    results.push({ type: 'error', message: '❌ No matching worksheet names found!' });
    hasErrors = true;
  } else {
    results.push({ type: 'success', message: `✅ Found ${matchingSheets.length} matching stories` });
  }
  
  // Check 2: Validate each story
  state.stories = [];
  matchingSheets.forEach((sheetName, index) => {
    const prompts = state.promptsData[sheetName];
    const ingredients = state.ingredientsData[sheetName];
    
    if (!prompts || prompts.length === 0) {
      results.push({ type: 'warning', message: `⚠️ "${sheetName}": No prompts found` });
    } else {
      const story = {
        number: index + 1,
        name: sheetName,
        promptCount: prompts.length,
        ingredientCount: ingredients ? ingredients.length : 0,
        prompts: prompts,
        ingredients: ingredients || []
      };
      
      state.stories.push(story);
      results.push({ 
        type: 'success', 
        message: `✅ Story ${index + 1}: "${sheetName}" - ${prompts.length} prompts, ${story.ingredientCount} ingredients` 
      });
    }
  });
  
  // Check 3: Base cat images
  if (state.baseCat01 && state.baseCat02) {
    results.push({ type: 'success', message: '✅ Both base cat images loaded' });
  } else {
    results.push({ type: 'error', message: '❌ Missing base cat images' });
    hasErrors = true;
  }
  
  // Display simplified results
  if (!hasErrors && state.stories.length > 0) {
    state.verified = true;
    
    // Show simple success message
    if (elements.verificationResults) elements.verificationResults.style.display = 'block';
    if (elements.verificationContent) {
      elements.verificationContent.innerHTML = `
        <div class="verify-item verify-success">
          ✅ All files matched! Found ${state.stories.length} synchronized stories ready to process.
        </div>
      `;
    }
    
    displayStories();
    
    // Hide upload section after successful verification
    const uploadSection = document.getElementById('uploadSection');
    if (uploadSection) uploadSection.style.display = 'none';
    
    if (elements.storiesSection) elements.storiesSection.style.display = 'block';
    if (elements.configSection) elements.configSection.style.display = 'block';
    if (elements.actionSection) elements.actionSection.style.display = 'block';
    updateStatus('ready', '✅ Verification complete - Select stories');
    addLog('success', `✅ All files matched! Found ${state.stories.length} stories`);
  } else {
    updateStatus('error', '❌ Verification failed');
    
    // Show errors
    if (elements.verificationResults) elements.verificationResults.style.display = 'block';
    if (elements.verificationContent) {
      elements.verificationContent.innerHTML = results
        .filter(r => r.type === 'error')
        .map(r => `<div class="verify-item verify-${r.type}">${r.message}</div>`)
        .join('');
    }
    
    addLog('error', '❌ Please fix errors and try again');
  }
}

function displayStories() {
  elements.storiesList.innerHTML = state.stories.map(story => `
    <div class="story-item">
      <span class="story-number">${story.number}</span>
      <span class="story-name">${story.name}</span>
      <span class="story-count">${story.promptCount} prompts</span>
    </div>
  `).join('');
}

function validateStorySelection() {
  const input = elements.storySelection.value.trim();
  // Just validate format, actual parsing happens on start
  return true;
}

// Start Generation
async function startGeneration() {
  console.log('[SIDEBAR] startGeneration called');
  console.log('[SIDEBAR] State:', state);
  
  if (!state.verified) {
    console.log('[SIDEBAR] Not verified');
    addLog('error', '❌ Please run Setup & Verify first');
    return;
  }
  
  // Parse story selection
  const selection = elements.storySelection.value.trim().toLowerCase();
  console.log('[SIDEBAR] Story selection:', selection);
  
  if (!selection) {
    console.log('[SIDEBAR] No selection');
    addLog('error', '❌ Please select stories to process');
    return;
  }
  
  state.selectedStories = parseStorySelection(selection);
  console.log('[SIDEBAR] Parsed stories:', state.selectedStories);
  
  if (state.selectedStories.length === 0) {
    console.log('[SIDEBAR] No stories parsed');
    addLog('error', '❌ Invalid story selection');
    return;
  }
  
  // Get active tab through background script (sidepanel can't query tabs directly)
  console.log('[SIDEBAR] Getting active tab info...');
  
  let tab;
  try {
    // Ask background script for tab info
    const response = await new Promise((resolve, reject) => {
      chrome.runtime.sendMessage({ action: 'getActiveTab' }, (response) => {
        if (chrome.runtime.lastError) {
          reject(chrome.runtime.lastError);
        } else {
          resolve(response);
        }
      });
    });
    
    tab = response.tab;
    console.log('[SIDEBAR] Active tab:', tab);
    
  } catch (error) {
    console.error('[SIDEBAR] Failed to get tab:', error);
    addLog('error', '❌ Failed to get active tab information');
    return;
  }
  
  if (!tab || !tab.url || !tab.url.includes('labs.google')) {
    console.log('[SIDEBAR] Not on Google Labs. Current URL:', tab?.url);
    addLog('error', '❌ Please open Google Labs Flow first');
    addLog('info', '💡 Navigate to: https://labs.google/fx/tools/flow');
    addLog('info', `Current page: ${tab?.url || 'unknown'}`);
    return;
  }
  
  addLog('success', '✅ On Google Labs page');
  console.log('[SIDEBAR] Verified on Google Labs');
  
  // Prepare configuration
  const config = {
    stories: state.selectedStories,
    maxConcurrent: parseInt(elements.maxConcurrent.value),
    reverseOrder: elements.reverseOrder.checked,
    wait50Percent: elements.wait50Percent.checked,
    baseCatImages: [state.baseCat01, state.baseCat02]
  };
  
  // Update UI safely
  state.isRunning = true;
  if (elements.startBtn) elements.startBtn.style.display = 'none';
  if (elements.stopBtn) elements.stopBtn.style.display = 'block';
  if (elements.progressSection) elements.progressSection.style.display = 'block';
  if (elements.exportReportBtn) elements.exportReportBtn.style.display = 'block';
  
  updateStatus('working', '🚀 Generation started');
  
  addLog('info', '═══════════════════════════════════════');
  addLog('info', '🚀 STARTING VIDEO GENERATION');
  addLog('info', `📚 Processing ${state.selectedStories.length} stories`);
  addLog('info', `⚙️ Max Concurrent: ${config.maxConcurrent}`);
  addLog('info', '═══════════════════════════════════════');
  
  // Send message through background script (sidepanel can't access chrome.tabs directly)
  try {
    addLog('info', '📝 Preparing to start generation...');
    console.log('[SIDEBAR] Starting generation process');
    console.log('[SIDEBAR] Tab ID:', tab.id);
    console.log('[SIDEBAR] Config:', config);
    
    // Check if chrome.runtime is available
    if (!chrome.runtime || !chrome.runtime.sendMessage) {
      throw new Error('Chrome runtime API not available. This is a browser limitation with sidepanels.');
    }
    
    addLog('info', '📤 Sending command to background script...');
    console.log('[SIDEBAR] Sending to background script');
    
    // Send to background script which will relay to content script
    chrome.runtime.sendMessage({
      action: 'startGenerationFromSidebar',
      tabId: tab.id,
      config: config
    }, (response) => {
      if (chrome.runtime.lastError) {
        console.error('[SIDEBAR] Runtime error:', chrome.runtime.lastError);
        addLog('error', `❌ Communication error: ${chrome.runtime.lastError.message}`);
        stopGeneration();
        return;
      }
      
      console.log('[SIDEBAR] Background script response:', response);
      
      if (response && response.success) {
        addLog('success', '✅ Command sent successfully');
      } else {
        addLog('error', `❌ Failed: ${response?.error || 'Unknown error'}`);
        stopGeneration();
      }
    });
    
  } catch (error) {
    console.error('[SIDEBAR] Error:', error);
    addLog('error', `❌ Failed to start: ${error.message}`);
    addLog('error', `💡 Error details: ${error.stack || 'No stack'}`);
    addLog('warning', '💡 Try refreshing the Google Labs page and reopening the sidebar');
    stopGeneration();
  }
}

function parseStorySelection(selection) {
  const stories = [];
  
  if (selection === 'all') {
    return state.stories;
  }
  
  // Parse ranges and individual numbers
  const parts = selection.split(',').map(p => p.trim());
  
  for (const part of parts) {
    if (part.includes('-')) {
      // Range: 1-5
      const [start, end] = part.split('-').map(n => parseInt(n.trim()));
      for (let i = start; i <= end && i <= state.stories.length; i++) {
        if (!stories.find(s => s.number === i)) {
          stories.push(state.stories[i - 1]);
        }
      }
    } else {
      // Single number
      const num = parseInt(part);
      if (num > 0 && num <= state.stories.length) {
        if (!stories.find(s => s.number === num)) {
          stories.push(state.stories[num - 1]);
        }
      }
    }
  }
  
  return stories;
}

async function stopGeneration() {
  state.isRunning = false;
  
  // Safely update UI elements
  if (elements.startBtn) elements.startBtn.style.display = 'block';
  if (elements.stopBtn) elements.stopBtn.style.display = 'none';
  
  updateStatus('ready', '⏹️ Stopped');
  addLog('warning', '⏹️ Generation stopped by user');
  
  // Send stop message through background script
  try {
    chrome.runtime.sendMessage({
      action: 'stopGeneration'
    }, (response) => {
      if (chrome.runtime.lastError) {
        console.error('[SIDEBAR] Stop message error:', chrome.runtime.lastError);
      } else {
        console.log('[SIDEBAR] Stop message sent');
      }
    });
  } catch (error) {
    console.error('[SIDEBAR] Failed to send stop message:', error);
  }
}

// Progress Updates
function updateProgress(data) {
  state.currentProgress = { ...state.currentProgress, ...data };
  
  const { stories, totalStories, prompts, totalPrompts, videos } = state.currentProgress;
  
  elements.storiesProgress.textContent = `${stories}/${totalStories}`;
  elements.promptsProgress.textContent = `${prompts}/${totalPrompts}`;
  elements.videosProgress.textContent = videos;
  
  // Update progress bar
  const progress = totalPrompts > 0 ? (prompts / totalPrompts) * 100 : 0;
  if (elements.progressBar) {
    elements.progressBar.style.width = `${progress}%`;
  }
}

function updateTask(task) {
  elements.currentTask.textContent = task;
}

// Helper functions for UI
function openGoogleFlow() {
  chrome.tabs.create({ url: 'https://labs.google/fx/tools/flow' });
  addLog('info', '🔗 Opening Google Flow in new tab...');
}

function copyLog() {
  const logEntries = elements.logContainer.querySelectorAll('.log-entry');
  const logText = Array.from(logEntries).map(entry => entry.textContent).join('\n');
  
  navigator.clipboard.writeText(logText).then(() => {
    addLog('success', '📋 Log copied to clipboard!');
  }).catch(err => {
    addLog('error', `Failed to copy log: ${err.message}`);
  });
}

function clearLog() {
  elements.logContainer.innerHTML = '';
  addLog('info', 'Log cleared');
}

// Report Export
function exportReport() {
  const report = generateReport();
  const blob = new Blob([report], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.href = url;
  a.download = `MamaCat_Report_${new Date().toISOString().slice(0, 10)}.txt`;
  a.click();
  
  URL.revokeObjectURL(url);
  addLog('success', '📄 Report exported');
}

function generateReport() {
  const lines = [];
  lines.push('╔═══════════════════════════════════════════════════════════╗');
  lines.push('║         MAMACAT VIDEO GENERATION REPORT                  ║');
  lines.push('╚═══════════════════════════════════════════════════════════╝');
  lines.push('');
  lines.push(`📅 Date: ${new Date().toLocaleString()}`);
  lines.push('');
  lines.push('📊 STATISTICS');
  lines.push('─────────────────────────────────────────────────────────');
  lines.push(`Stories Processed: ${state.currentProgress.stories}/${state.currentProgress.totalStories}`);
  lines.push(`Prompts Processed: ${state.currentProgress.prompts}/${state.currentProgress.totalPrompts}`);
  lines.push(`Videos Generated: ${state.currentProgress.videos}`);
  lines.push('');
  lines.push('📝 ACTIVITY LOG');
  lines.push('─────────────────────────────────────────────────────────');
  
  const logEntries = elements.logContainer.querySelectorAll('.log-entry');
  logEntries.forEach(entry => {
    lines.push(entry.textContent);
  });
  
  return lines.join('\n');
}

// Check Google Labs Connection
async function checkGoogleLabsConnection() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab && tab.url && tab.url.includes('labs.google')) {
      addLog('success', '✅ Connected to Google Labs');
      updateStatus('ready', 'Connected to Google Labs');
    } else {
      addLog('warning', '⚠️ Not on Google Labs');
      addLog('info', '💡 Navigate to: https://labs.google/fx/tools/flow');
      updateStatus('ready', 'Please open Google Labs');
    }
  } catch (error) {
    addLog('warning', '⚠️ Could not check connection');
  }
}

// Listen for messages from background/content script
if (chrome.runtime && chrome.runtime.onMessage) {
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('[SIDEBAR] Received message:', message);
    
    switch (message.action) {
      case 'updateProgress':
        updateProgress(message.data);
        break;
      case 'updateTask':
        updateTask(message.task);
        break;
      case 'log':
        addLog(message.type, message.message);
        break;
      case 'generationComplete':
        stopGeneration();
        updateStatus('ready', '✅ Generation complete');
        addLog('success', '🎉 All videos generated successfully!');
        break;
      case 'generationError':
        stopGeneration();
        updateStatus('error', '❌ Error occurred');
        addLog('error', `❌ Generation failed: ${message.error}`);
        break;
    }
    
    sendResponse({ received: true });
    return true;
  });
} else {
  console.error('[SIDEBAR] chrome.runtime.onMessage not available!');
  addLog('error', '❌ Chrome runtime API not available in sidebar');
}
