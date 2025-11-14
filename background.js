// Background service worker
console.log('🎬 MamaCat Video Generator - Background Script Loaded');

// Handle extension installation
chrome.runtime.onInstalled.addListener(() => {
  console.log('MamaCat Video Generator installed');
});

// Handle extension icon click - open sidebar
chrome.action.onClicked.addListener((tab) => {
  chrome.sidePanel.open({ windowId: tab.windowId });
});

// Handle messages from content scripts and sidebar
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('[BACKGROUND] Received message:', message.action);
  
  // Handle getActiveTab request from sidebar
  if (message.action === 'getActiveTab') {
    console.log('[BACKGROUND] Getting active tab for sidebar');
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs && tabs.length > 0) {
        console.log('[BACKGROUND] Found active tab:', tabs[0].id, tabs[0].url);
        sendResponse({ success: true, tab: tabs[0] });
      } else {
        console.log('[BACKGROUND] No active tab found');
        sendResponse({ success: false, error: 'No active tab' });
      }
    });
    return true; // Keep channel open for async response
  }
  
  // Handle start generation from sidebar
  if (message.action === 'startGenerationFromSidebar') {
    console.log('[BACKGROUND] Relaying start generation to tab:', message.tabId);
    
    const tabId = message.tabId;
    const config = message.config;
    
    // First inject content script
    chrome.scripting.executeScript({
      target: { tabId: tabId },
      files: ['content.js']
    }).then(() => {
      console.log('[BACKGROUND] Content script injected');
      
      // Wait a bit then send message
      setTimeout(() => {
        chrome.tabs.sendMessage(tabId, {
          action: 'startGeneration',
          config: config
        }).then((response) => {
          console.log('[BACKGROUND] Content script response:', response);
          sendResponse({ success: true, response: response });
        }).catch((error) => {
          console.error('[BACKGROUND] Error sending to content:', error);
          sendResponse({ success: false, error: error.message });
        });
      }, 1000);
      
    }).catch((injectError) => {
      console.log('[BACKGROUND] Injection error (might be already injected):', injectError);
      
      // Try sending anyway
      chrome.tabs.sendMessage(tabId, {
        action: 'startGeneration',
        config: config
      }).then((response) => {
        console.log('[BACKGROUND] Content script response:', response);
        sendResponse({ success: true, response: response });
      }).catch((error) => {
        console.error('[BACKGROUND] Error sending to content:', error);
        sendResponse({ success: false, error: error.message });
      });
    });
    
    return true; // Keep channel open for async response
  }
  
  // Forward other messages
  if (message.action === 'forwardToContent') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        chrome.tabs.sendMessage(tabs[0].id, message.data);
      }
    });
  }
  
  // Forward logs and updates to sidebar
  if (message.action === 'log' || message.action === 'updateProgress' || 
      message.action === 'updateTask' || message.action === 'generationComplete' || 
      message.action === 'generationError') {
    console.log('[BACKGROUND] Forwarding to sidebar:', message.action);
    // Broadcast to all extension contexts (including sidebar)
    chrome.runtime.sendMessage(message).catch(() => {
      // Sidebar might not be open, that's okay
    });
  }
  
  return true;
});

// Keep service worker alive
let keepAliveInterval;

function keepAlive() {
  keepAliveInterval = setInterval(() => {
    chrome.runtime.getPlatformInfo(() => {
      // Just to keep the service worker alive
    });
  }, 20000); // Every 20 seconds
}

keepAlive();
