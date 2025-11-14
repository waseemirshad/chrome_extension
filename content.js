// Content script - runs on Google Labs pages
console.log('🎬 MamaCat Video Generator - Content Script Loaded');
console.log('📍 Current URL:', window.location.href);
console.log('📍 Page title:', document.title);

let automationState = {
  isRunning: false,
  config: null,
  currentStep: null,
  ingredientMapping: {},
  debugMode: true
};

// Debug logger
function debugLog(message, data = null) {
  if (automationState.debugMode) {
    console.log(`[MAMACAT DEBUG] ${message}`, data || '');
  }
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  debugLog('Received message:', message);
  
  if (message.action === 'ping') {
    debugLog('Ping received, sending pong');
    sendResponse({ success: true, message: 'pong', timestamp: Date.now() });
    return true;
  }
  
  if (message.action === 'startGeneration') {
    debugLog('Starting generation with config:', message.config);
    startAutomation(message.config);
    sendResponse({ success: true, message: 'Generation started' });
  } else if (message.action === 'stopGeneration') {
    debugLog('Stopping generation');
    stopAutomation();
    sendResponse({ success: true, message: 'Generation stopped' });
  }
  return true;
});

async function startAutomation(config) {
  automationState.isRunning = true;
  automationState.config = config;
  
  debugLog('Automation state set to running');
  debugLog('Config received:', config);
  
  sendLog('info', '═══════════════════════════════════════');
  sendLog('info', '🚀 AUTOMATION STARTED');
  sendLog('info', '═══════════════════════════════════════');
  sendLog('info', `📸 Base cat images: ${config.baseCatImages ? config.baseCatImages.length : 0} files`);
  sendLog('info', `📚 Stories to process: ${config.stories ? config.stories.length : 0}`);
  sendLog('info', `⚙️ Max concurrent: ${config.maxConcurrent || 4}`);
  sendLog('info', `🔄 Reverse order: ${config.reverseOrder ? 'Yes' : 'No'}`);
  
  try {
    // Verify we're on Google Labs
    if (!window.location.href.includes('labs.google')) {
      throw new Error('Not on Google Labs page. Please navigate to https://labs.google/fx/tools/flow');
    }
    
    debugLog('URL verified - on Google Labs');
    sendLog('success', '✅ Verified: On Google Labs page');
    
    // Inject automation script with config
    debugLog('Injecting automation script...');
    await injectAutomationScript(config);
    debugLog('Automation script injected successfully');
    
    // Process each story
    for (let i = 0; i < config.stories.length; i++) {
      if (!automationState.isRunning) {
        sendLog('warning', '⏹️ Automation stopped by user');
        break;
      }
      
      const story = config.stories[i];
      sendLog('info', '═══════════════════════════════════════');
      sendLog('info', `📖 Story ${i + 1}/${config.stories.length}: ${story.name}`);
      sendLog('info', `📝 Prompts: ${story.promptCount || story.prompts?.length || 0}`);
      sendLog('info', `🎨 Ingredients: ${story.ingredientCount || story.ingredients?.length || 0}`);
      sendLog('info', '═══════════════════════════════════════');
      
      debugLog(`Processing story ${i + 1}:`, story);
      
      // Create project for this story
      await processStory(story, config);
      
      sendLog('success', `✅ Story "${story.name}" completed!`);
    }
    
    if (automationState.isRunning) {
      sendLog('info', '═══════════════════════════════════════');
      sendLog('success', '🎉 ALL STORIES COMPLETED!');
      sendLog('info', '═══════════════════════════════════════');
      sendMessage('generationComplete');
    }
    
  } catch (error) {
    debugLog('Automation error:', error);
    console.error('Automation error details:', error);
    sendLog('error', `❌ Automation failed: ${error.message}`);
    sendLog('error', `💡 Check browser console (F12) for details`);
    sendMessage('generationError', { error: error.message });
  }
}

async function processStory(story, config) {
  try {
    debugLog('Processing story:', story.name);
    sendLog('info', `🎬 Creating project: MamaCat - ${story.name}`);
    
    // Verify story has required data
    if (!story.name) {
      throw new Error('Story missing name');
    }
    
    debugLog('Story data:', {
      name: story.name,
      prompts: story.prompts?.length || 0,
      ingredients: story.ingredients?.length || 0
    });
    
    // Send story data to injected script
    debugLog('Sending MAMACAT_PROCESS_STORY message');
    window.postMessage({
      type: 'MAMACAT_PROCESS_STORY',
      story: story,
      config: config
    }, '*');
    
    debugLog('Message sent, waiting for completion...');
    
    // Wait for story completion
    await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        debugLog('Story processing timeout!');
        reject(new Error('Story processing timeout (1 hour)'));
      }, 3600000); // 1 hour timeout
      
      const handler = (event) => {
        if (event.source !== window) return;
        
        debugLog('Received window message:', event.data.type);
        
        if (event.data.type === 'MAMACAT_STORY_COMPLETE') {
          debugLog('Story completed successfully');
          clearTimeout(timeout);
          window.removeEventListener('message', handler);
          resolve();
        } else if (event.data.type === 'MAMACAT_ERROR') {
          debugLog('Story error:', event.data.error);
          clearTimeout(timeout);
          window.removeEventListener('message', handler);
          reject(new Error(event.data.error));
        }
      };
      
      window.addEventListener('message', handler);
    });
    
    debugLog('Story processing completed');
    
  } catch (error) {
    debugLog('Story processing error:', error);
    console.error('Story processing error details:', error);
    sendLog('error', `❌ Story processing failed: ${error.message}`);
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
  console.log('🔴 [INJECT] Function called!');
  try {
    console.log('🔴 [INJECT] Starting injection...');
    debugLog('Starting script injection...');
    
    // Check if already injected
    console.log('🔴 [INJECT] Checking if already loaded...');
    
    // Check if script element already exists
    const existingScript = document.querySelector('script[src*="automation-core-debug.js"]');
    if (existingScript) {
      console.log('🔴 [INJECT] Script already injected, waiting for ready signal...');
      debugLog('Automation core script already in DOM');
      sendLog('info', '✅ Automation core already injected');
      
      // Just wait for the ready signal
      await new Promise((resolve, reject) => {
        const timeout = setTimeout(() => {
          reject(new Error('Automation core did not initialize'));
        }, 5000);
        
        const handler = (event) => {
          if (event.source !== window) return;
          if (event.data.type === 'MAMACAT_CORE_READY') {
            clearTimeout(timeout);
            window.removeEventListener('message', handler);
            debugLog('Core ready signal received');
            resolve();
          }
        };
        
        window.addEventListener('message', handler);
      });
      
      sendLog('success', '✅ Automation core initialized');
      return;
    }
    
    console.log('🔴 [INJECT] Not loaded, proceeding with injection...');
    
    // First inject the automation core (DEBUG VERSION)
    debugLog('Creating script element...');
    const coreScript = document.createElement('script');
    coreScript.src = chrome.runtime.getURL('automation-core-debug.js');
    
    await new Promise((resolve, reject) => {
      coreScript.onload = () => {
        debugLog('Script loaded successfully');
        resolve();
      };
      coreScript.onerror = (error) => {
        debugLog('Script load error:', error);
        reject(new Error('Failed to load automation-core.js'));
      };
      (document.head || document.documentElement).appendChild(coreScript);
    });
    
    sendLog('success', '✅ Automation core loaded');
    debugLog('Automation core script injected');
    
    // Wait for the ready signal (the script sends it automatically)
    debugLog('Waiting for core ready signal...');
    await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        reject(new Error('Automation core did not initialize'));
      }, 5000);
      
      const handler = (event) => {
        if (event.source !== window) return;
        if (event.data.type === 'MAMACAT_CORE_READY') {
          clearTimeout(timeout);
          window.removeEventListener('message', handler);
          debugLog('Core ready signal received');
          resolve();
        }
      };
      
      window.addEventListener('message', handler);
    });
    
    sendLog('success', '✅ Automation core initialized');
    debugLog('Automation core ready');
    
  } catch (error) {
    debugLog('Injection error:', error);
    console.error('Script injection error:', error);
    sendLog('error', `❌ Failed to load automation: ${error.message}`);
    throw error;
  }
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
