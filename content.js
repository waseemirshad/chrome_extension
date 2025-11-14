// Content script - runs on Google Labs pages
console.log('🎬 MamaCat Video Generator - Content Script Loaded');

let automationState = {
  isRunning: false,
  config: null,
  currentStep: null,
  ingredientMapping: {}
};

// Listen for messages from popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'startGeneration') {
    startAutomation(message.config);
    sendResponse({ success: true });
  } else if (message.action === 'stopGeneration') {
    stopAutomation();
    sendResponse({ success: true });
  }
  return true;
});

async function startAutomation(config) {
  automationState.isRunning = true;
  automationState.config = config;
  
  sendLog('info', '🚀 Starting automation...');
  sendLog('info', `📸 Base cat images: ${config.baseCatImages.length} files`);
  sendLog('info', `📚 Stories to process: ${config.stories.length}`);
  
  try {
    // Inject automation script with config
    await injectAutomationScript(config);
    
    // Process each story
    for (const story of config.stories) {
      if (!automationState.isRunning) break;
      
      sendLog('info', `📖 Processing story: ${story.name}`);
      
      // Create project for this story
      await processStory(story, config);
    }
    
    if (automationState.isRunning) {
      sendMessage('generationComplete');
    }
    
  } catch (error) {
    sendLog('error', `Automation failed: ${error.message}`);
    sendMessage('generationError', { error: error.message });
  }
}

async function processStory(story, config) {
  try {
    sendLog('info', `🎬 Creating project: MamaCat - ${story.name}`);
    
    // Send story data to injected script
    window.postMessage({
      type: 'MAMACAT_PROCESS_STORY',
      story: story,
      config: config
    }, '*');
    
    // Wait for story completion
    await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        reject(new Error('Story processing timeout'));
      }, 3600000); // 1 hour timeout
      
      const handler = (event) => {
        if (event.source !== window) return;
        
        if (event.data.type === 'MAMACAT_STORY_COMPLETE') {
          clearTimeout(timeout);
          window.removeEventListener('message', handler);
          resolve();
        } else if (event.data.type === 'MAMACAT_ERROR') {
          clearTimeout(timeout);
          window.removeEventListener('message', handler);
          reject(new Error(event.data.error));
        }
      };
      
      window.addEventListener('message', handler);
    });
    
  } catch (error) {
    sendLog('error', `Story processing failed: ${error.message}`);
    throw error;
  }
}

function stopAutomation() {
  automationState.isRunning = false;
  sendLog('warning', 'Automation stopped');
  
  // Send stop message to injected script
  window.postMessage({ type: 'MAMACAT_STOP' }, '*');
}

async function injectAutomationScript(config) {
  // First inject the automation core
  const coreScript = document.createElement('script');
  coreScript.src = chrome.runtime.getURL('automation-core.js');
  
  await new Promise((resolve, reject) => {
    coreScript.onload = resolve;
    coreScript.onerror = reject;
    (document.head || document.documentElement).appendChild(coreScript);
  });
  
  sendLog('info', '✅ Automation core loaded');
  
  // Wait a bit for the class to be available
  await new Promise(resolve => setTimeout(resolve, 500));
  
  // Send config via postMessage instead of inline script
  window.postMessage({
    type: 'MAMACAT_INIT',
    config: config
  }, '*');
}

// Helper functions
function sendLog(type, message) {
  chrome.runtime.sendMessage({
    action: 'log',
    type: type,
    message: message
  });
}

function sendMessage(action, data = {}) {
  chrome.runtime.sendMessage({
    action: action,
    ...data
  });
}

function updateProgress(data) {
  chrome.runtime.sendMessage({
    action: 'updateProgress',
    data: data
  });
}

function updateTask(task) {
  chrome.runtime.sendMessage({
    action: 'updateTask',
    task: task
  });
}

// Listen for messages from injected script
window.addEventListener('message', (event) => {
  if (event.source !== window) return;
  
  const message = event.data;
  
  switch (message.type) {
    case 'MAMACAT_LOG':
      sendLog(message.logType, message.message);
      break;
    case 'MAMACAT_PROGRESS':
      updateProgress(message.data);
      break;
    case 'MAMACAT_TASK':
      updateTask(message.task);
      break;
    case 'MAMACAT_COMPLETE':
      sendMessage('generationComplete');
      break;
    case 'MAMACAT_ERROR':
      sendMessage('generationError', { error: message.error });
      break;
  }
});
