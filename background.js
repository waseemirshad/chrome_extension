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
  // Forward messages between sidebar and content script
  if (message.action === 'forwardToContent') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        chrome.tabs.sendMessage(tabs[0].id, message.data);
      }
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
