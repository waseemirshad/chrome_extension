// Sidebar JavaScript - Main Logic
console.log('🎬 MamaCat Sidebar Loaded');

// State Management
const state = {
  promptsData: null,
  ingredientsData: null,
  baseCat01: null,
  baseCat02: null,
  verified: false,
  stories: [],
  selectedStories: [],
  isRunning: false,
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
  // File inputs
  promptsFile: document.getElementById('promptsFile'),
  ingredientsFile: document.getElementById('ingredientsFile'),
  baseCat01: document.getElementById('baseCat01'),
  baseCat02: document.getElementById('baseCat02'),
  
  // Displays
  promptsDisplay: document.getElementById('promptsDisplay'),
  ingredientsDisplay: document.getElementById('ingredientsDisplay'),
  baseCat01Display: document.getElementById('baseCat01Display'),
  baseCat02Display: document.getElementById('baseCat02Display'),
  
  // Buttons
  setupBtn: document.getElementById('setupBtn'),
  startBtn: document.getElementById('startBtn'),
  stopBtn: document.getElementById('stopBtn'),
  clearLogBtn: document.getElementById('clearLogBtn'),
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

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  checkGoogleLabsConnection();
  addLog('info', '🎬 MamaCat Video Generator Ready');
  addLog('info', 'Please upload your files to begin');
});

// Event Listeners
function setupEventListeners() {
  // File uploads
  elements.promptsFile.addEventListener('change', (e) => handleFileUpload(e, 'prompts'));
  elements.ingredientsFile.addEventListener('change', (e) => handleFileUpload(e, 'ingredients'));
  elements.baseCat01.addEventListener('change', (e) => handleFileUpload(e, 'baseCat01'));
  elements.baseCat02.addEventListener('change', (e) => handleFileUpload(e, 'baseCat02'));
  
  // Buttons
  elements.setupBtn.addEventListener('click', setupAndVerify);
  elements.startBtn.addEventListener('click', startGeneration);
  elements.stopBtn.addEventListener('click', stopGeneration);
  elements.clearLogBtn.addEventListener('click', clearLog);
  elements.exportReportBtn.addEventListener('click', exportReport);
  
  // Quick select buttons
  document.querySelectorAll('.btn-quick').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const selection = e.target.dataset.select;
      elements.storySelection.value = selection;
    });
  });
  
  // Story selection input
  elements.storySelection.addEventListener('input', validateStorySelection);
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
    elements.verificationResults.style.display = 'block';
    elements.verificationContent.innerHTML = `
      <div class="verify-item verify-success">
        ✅ All files matched! Found ${state.stories.length} synchronized stories ready to process.
      </div>
    `;
    
    displayStories();
    
    // Hide upload section after successful verification
    document.getElementById('uploadSection').style.display = 'none';
    
    elements.storiesSection.style.display = 'block';
    elements.configSection.style.display = 'block';
    elements.actionSection.style.display = 'block';
    updateStatus('ready', '✅ Verification complete - Select stories');
    addLog('success', `✅ All files matched! Found ${state.stories.length} stories`);
  } else {
    updateStatus('error', '❌ Verification failed');
    
    // Show errors
    elements.verificationResults.style.display = 'block';
    elements.verificationContent.innerHTML = results
      .filter(r => r.type === 'error')
      .map(r => `<div class="verify-item verify-${r.type}">${r.message}</div>`)
      .join('');
    
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
  if (!state.verified) {
    addLog('error', '❌ Please run Setup & Verify first');
    return;
  }
  
  // Parse story selection
  const selection = elements.storySelection.value.trim().toLowerCase();
  
  if (!selection) {
    addLog('error', '❌ Please select stories to process');
    return;
  }
  
  state.selectedStories = parseStorySelection(selection);
  
  if (state.selectedStories.length === 0) {
    addLog('error', '❌ Invalid story selection');
    return;
  }
  
  // Check if on Google Labs
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab || !tab.url.includes('labs.google')) {
    addLog('error', '❌ Please open Google Labs Flow first');
    addLog('info', '💡 Navigate to: https://labs.google/fx/tools/flow');
    return;
  }
  
  // Prepare configuration
  const config = {
    stories: state.selectedStories,
    maxConcurrent: parseInt(elements.maxConcurrent.value),
    reverseOrder: elements.reverseOrder.checked,
    wait50Percent: elements.wait50Percent.checked,
    baseCatImages: [state.baseCat01, state.baseCat02]
  };
  
  // Update UI
  state.isRunning = true;
  elements.startBtn.style.display = 'none';
  elements.stopBtn.style.display = 'block';
  elements.progressSection.style.display = 'block';
  elements.exportReportBtn.style.display = 'block';
  
  updateStatus('working', '🚀 Generation started');
  
  addLog('info', '═══════════════════════════════════════');
  addLog('info', '🚀 STARTING VIDEO GENERATION');
  addLog('info', `📚 Processing ${state.selectedStories.length} stories`);
  addLog('info', `⚙️ Max Concurrent: ${config.maxConcurrent}`);
  addLog('info', '═══════════════════════════════════════');
  
  // Inject content script if needed, then send message
  try {
    // First, try to inject the content script
    try {
      await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ['content.js']
      });
      addLog('info', '📝 Content script injected');
      await new Promise(resolve => setTimeout(resolve, 1000)); // Wait for script to initialize
    } catch (injectError) {
      // Script might already be injected, that's okay
      addLog('info', '📝 Using existing content script');
    }
    
    // Now send the message
    await chrome.tabs.sendMessage(tab.id, {
      action: 'startGeneration',
      config: config
    });
  } catch (error) {
    addLog('error', `❌ Failed to start: ${error.message}`);
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
  elements.startBtn.style.display = 'block';
  elements.stopBtn.style.display = 'none';
  
  updateStatus('ready', '⏹️ Stopped');
  addLog('warning', '⏹️ Generation stopped by user');
  
  // Send stop message to content script
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab) {
      await chrome.tabs.sendMessage(tab.id, { action: 'stopGeneration' });
    }
  } catch (error) {
    console.error('Failed to send stop message:', error);
  }
  
  // Also send stop via window message if on same page
  try {
    window.postMessage({ type: 'MAMACAT_STOP' }, '*');
  } catch (error) {
    console.error('Failed to post stop message:', error);
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
  elements.progressBar.style.width = `${progress}%`;
}

function updateTask(task) {
  elements.currentTask.textContent = task;
}

// Status Management
function updateStatus(type, message) {
  elements.statusDot.className = `status-dot ${type}`;
  elements.statusText.textContent = message;
}

// Logging
function addLog(type, message) {
  const timestamp = new Date().toLocaleTimeString();
  const logEntry = document.createElement('div');
  logEntry.className = `log-entry log-${type}`;
  logEntry.innerHTML = `<span class="log-time">[${timestamp}]</span>${message}`;
  
  elements.logContainer.appendChild(logEntry);
  elements.logContainer.scrollTop = elements.logContainer.scrollHeight;
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

// Listen for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
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
});
