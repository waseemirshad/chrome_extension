// DEBUG VERSION - Comprehensive logging at every step
console.log('🔴🔴🔴 [DEBUG-CORE] FILE LOADING STARTED 🔴🔴🔴');
console.log('🔍 [DEBUG-CORE] Loading automation-core-debug.js');

class GoogleLabsAutomationDebug {
  constructor() {
    this.driver = null;
    this.ingredientMapping = {};
    this.isRunning = false;
    this.config = null;
    this.stepLog = [];
    
    console.log('🔍 [DEBUG-CORE] GoogleLabsAutomationDebug instance created');
  }

  async wait(ms) {
    console.log(`🔍 [DEBUG-CORE] Waiting ${ms}ms...`);
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  log(type, message) {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = `[${timestamp}] [${type.toUpperCase()}] ${message}`;
    
    console.log(`🔍 [DEBUG-CORE] ${logEntry}`);
    this.stepLog.push(logEntry);
    
    window.postMessage({
      type: 'MAMACAT_LOG',
      logType: type,
      message: message
    }, '*');
  }

  verifyElement(element, description) {
    if (element) {
      console.log(`✅ [DEBUG-CORE] VERIFIED: ${description}`);
      this.log('success', `✅ VERIFIED: ${description}`);
      return true;
    } else {
      console.error(`❌ [DEBUG-CORE] NOT FOUND: ${description}`);
      this.log('error', `❌ NOT FOUND: ${description}`);
      return false;
    }
  }

  verifyClick(element, description) {
    try {
      if (!element) {
        console.error(`❌ [DEBUG-CORE] CLICK FAILED: ${description} - Element is null`);
        this.log('error', `❌ CLICK FAILED: ${description} - Element is null`);
        return false;
      }
      
      console.log(`🖱️ [DEBUG-CORE] CLICKING: ${description}`);
      this.log('info', `🖱️ CLICKING: ${description}`);
      
      element.click();
      
      console.log(`✅ [DEBUG-CORE] CLICKED: ${description}`);
      this.log('success', `✅ CLICKED: ${description}`);
      return true;
    } catch (error) {
      console.error(`❌ [DEBUG-CORE] CLICK ERROR: ${description}`, error);
      this.log('error', `❌ CLICK ERROR: ${description} - ${error.message}`);
      return false;
    }
  }

  getElementByXPath(xpath) {
    console.log(`🔍 [DEBUG-CORE] XPath query: ${xpath}`);
    const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    console.log(`🔍 [DEBUG-CORE] XPath result:`, result ? 'Found' : 'Not found');
    return result;
  }

  getElementsByXPath(xpath) {
    console.log(`🔍 [DEBUG-CORE] XPath query (multiple): ${xpath}`);
    const result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
    const nodes = [];
    for (let i = 0; i < result.snapshotLength; i++) {
      nodes.push(result.snapshotItem(i));
    }
    console.log(`🔍 [DEBUG-CORE] XPath results: ${nodes.length} elements found`);
    return nodes;
  }

  async createNewProject(projectName) {
    console.log('═══════════════════════════════════════');
    console.log('🔍 [DEBUG-CORE] CREATE NEW PROJECT');
    console.log('═══════════════════════════════════════');
    
    this.log('info', '═══════════════════════════════════════');
    this.log('info', `🆕 CREATE PROJECT: ${projectName}`);
    this.log('info', '═══════════════════════════════════════');
    
    try {
      // STEP 1: Find "New project" button
      this.log('info', '[STEP 1/6] Looking for "New project" button...');
      console.log('🔍 [DEBUG-CORE] [STEP 1/6] Searching for New project button');
      
      let newProjectBtn = null;
      let methodUsed = null;
      
      // Method 1: By class
      console.log('🔍 [DEBUG-CORE] Method 1: Trying class selector...');
      newProjectBtn = document.querySelector('button.sc-c177465c-1.hVamcH.sc-a38764c7-0.fXsrxE');
      if (newProjectBtn) {
        methodUsed = 'Class selector';
        console.log('✅ [DEBUG-CORE] Found via class selector');
      }
      
      // Method 2: By text content
      if (!newProjectBtn) {
        console.log('🔍 [DEBUG-CORE] Method 2: Trying text search...');
        const buttons = document.querySelectorAll('button');
        console.log(`🔍 [DEBUG-CORE] Found ${buttons.length} buttons on page`);
        
        for (let i = 0; i < buttons.length; i++) {
          const btn = buttons[i];
          const text = btn.textContent.toLowerCase();
          console.log(`🔍 [DEBUG-CORE] Button ${i}: "${text}"`);
          
          if (text.includes('new project')) {
            newProjectBtn = btn;
            methodUsed = 'Text search';
            console.log(`✅ [DEBUG-CORE] Found via text search at index ${i}`);
            break;
          }
        }
      }
      
      // Method 3: XPath
      if (!newProjectBtn) {
        console.log('🔍 [DEBUG-CORE] Method 3: Trying XPath...');
        newProjectBtn = this.getElementByXPath("//button[contains(., 'New project')]");
        if (newProjectBtn) {
          methodUsed = 'XPath';
          console.log('✅ [DEBUG-CORE] Found via XPath');
        }
      }
      
      if (!this.verifyElement(newProjectBtn, `"New project" button (via ${methodUsed})`)) {
        throw new Error('New project button not found');
      }
      
      // STEP 2: Click "New project" button
      this.log('info', '[STEP 2/6] Clicking "New project" button...');
      console.log('🔍 [DEBUG-CORE] [STEP 2/6] Clicking button');
      
      if (!this.verifyClick(newProjectBtn, '"New project" button')) {
        throw new Error('Failed to click New project button');
      }
      
      // STEP 3: Wait for project creation
      this.log('info', '[STEP 3/6] Waiting for project to be created...');
      console.log('🔍 [DEBUG-CORE] [STEP 3/6] Waiting 3 seconds');
      await this.wait(3000);
      this.log('success', '[STEP 3/6] ✅ Wait complete');
      
      // STEP 4: Find edit button (pencil icon)
      this.log('info', '[STEP 4/6] Looking for edit button (pencil icon)...');
      console.log('🔍 [DEBUG-CORE] [STEP 4/6] Searching for edit button');
      
      await this.wait(2000);
      
      let editBtn = null;
      methodUsed = null;
      
      // Method 1: XPath with google-symbols
      console.log('🔍 [DEBUG-CORE] Method 1: XPath with google-symbols...');
      editBtn = this.getElementByXPath("//button[.//i[contains(@class, 'google-symbols') and contains(., 'edit')]]");
      if (editBtn) {
        methodUsed = 'XPath google-symbols';
        console.log('✅ [DEBUG-CORE] Found via XPath');
      }
      
      // Method 2: Search all buttons
      if (!editBtn) {
        console.log('🔍 [DEBUG-CORE] Method 2: Searching all buttons...');
        const buttons = document.querySelectorAll('button');
        console.log(`🔍 [DEBUG-CORE] Found ${buttons.length} buttons`);
        
        for (let i = 0; i < buttons.length; i++) {
          const btn = buttons[i];
          const html = btn.innerHTML.toLowerCase();
          
          if (html.includes('edit')) {
            editBtn = btn;
            methodUsed = 'Button search';
            console.log(`✅ [DEBUG-CORE] Found edit button at index ${i}`);
            console.log(`🔍 [DEBUG-CORE] Button HTML: ${btn.innerHTML.substring(0, 100)}`);
            break;
          }
        }
      }
      
      if (!this.verifyElement(editBtn, `Edit button (via ${methodUsed})`)) {
        throw new Error('Edit button not found');
      }
      
      // STEP 5: Click edit button
      this.log('info', '[STEP 5/6] Clicking edit button...');
      console.log('🔍 [DEBUG-CORE] [STEP 5/6] Clicking edit button');
      
      if (!this.verifyClick(editBtn, 'Edit button')) {
        throw new Error('Failed to click edit button');
      }
      
      await this.wait(1000);
      
      // STEP 6: Find and fill input field
      this.log('info', '[STEP 6/6] Finding input field...');
      console.log('🔍 [DEBUG-CORE] [STEP 6/6] Searching for input field');
      
      const inputs = document.querySelectorAll('input[type="text"]');
      console.log(`🔍 [DEBUG-CORE] Found ${inputs.length} text inputs`);
      
      if (inputs.length === 0) {
        throw new Error('No input field found');
      }
      
      const nameInput = inputs[0];
      this.verifyElement(nameInput, 'Name input field');
      
      // Click input
      console.log('🔍 [DEBUG-CORE] Clicking input field');
      nameInput.click();
      await this.wait(500);
      
      // Clear input
      console.log('🔍 [DEBUG-CORE] Clearing input field');
      this.log('info', 'Clearing existing text...');
      nameInput.select();
      await this.wait(300);
      nameInput.value = '';
      await this.wait(300);
      
      // Enter name
      console.log(`🔍 [DEBUG-CORE] Entering project name: ${projectName}`);
      this.log('info', `Entering name: ${projectName}`);
      nameInput.value = projectName;
      nameInput.dispatchEvent(new Event('input', { bubbles: true }));
      nameInput.dispatchEvent(new Event('change', { bubbles: true }));
      await this.wait(500);
      
      // Verify the value was set
      const actualValue = nameInput.value;
      console.log(`🔍 [DEBUG-CORE] Input value after setting: "${actualValue}"`);
      
      if (actualValue === projectName) {
        this.log('success', `✅ Name entered: ${projectName}`);
      } else {
        this.log('warning', `⚠️ Name might not be set correctly. Expected: "${projectName}", Got: "${actualValue}"`);
      }
      
      // Save - using multiple methods to find the correct button
      console.log('🔍 [DEBUG-CORE] Looking for save button');
      this.log('info', 'Looking for save button...');
      
      let saveBtn = null;
      
      // Method 1: By type="submit" and check icon (most specific)
      console.log('🔍 [DEBUG-CORE] Method 1: Looking for submit button with check icon...');
      saveBtn = document.querySelector('button[type="submit"][color="BLURPLE"] i.google-symbols');
      if (saveBtn) {
        saveBtn = saveBtn.closest('button');
        console.log('✅ [DEBUG-CORE] Found save button via submit type');
      }
      
      // Method 2: By XPath with check icon and "Save edit" text
      if (!saveBtn) {
        console.log('🔍 [DEBUG-CORE] Method 2: XPath with Save edit...');
        saveBtn = this.getElementByXPath("//button[@type='submit' and .//span[contains(., 'Save edit')]]");
        if (saveBtn) {
          console.log('✅ [DEBUG-CORE] Found save button via Save edit text');
        }
      }
      
      // Method 3: Original XPath method
      if (!saveBtn) {
        console.log('🔍 [DEBUG-CORE] Method 3: XPath with check icon...');
        saveBtn = this.getElementByXPath("//button[@type='submit' and .//i[contains(@class, 'google-symbols') and contains(., 'check')]]");
        if (saveBtn) {
          console.log('✅ [DEBUG-CORE] Found save button via XPath');
        }
      }
      
      if (saveBtn) {
        console.log('✅ [DEBUG-CORE] Found save button');
        console.log('🔍 [DEBUG-CORE] Button HTML:', saveBtn.outerHTML.substring(0, 200));
        this.verifyClick(saveBtn, 'Save button (check icon)');
      } else {
        console.log('🔍 [DEBUG-CORE] No save button found, pressing Enter');
        this.log('info', 'Pressing Enter to save...');
        nameInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true }));
      }
      
      await this.wait(2000);
      
      // Verify the project name is visible
      console.log('🔍 [DEBUG-CORE] Verifying project name...');
      try {
        // Look for the project name in the UI
        const projectNameElements = document.querySelectorAll('button, div, span');
        let foundName = false;
        
        for (const el of projectNameElements) {
          if (el.textContent.includes(projectName)) {
            foundName = true;
            console.log('✅ [DEBUG-CORE] Found project name in UI:', el.textContent);
            this.log('success', `✅ Verified project name: ${el.textContent.substring(0, 50)}`);
            break;
          }
        }
        
        if (!foundName) {
          console.log('⚠️ [DEBUG-CORE] Could not find project name in UI');
          this.log('warning', '⚠️ Project name not found in UI - might not have been saved');
        }
      } catch (error) {
        console.log('⚠️ [DEBUG-CORE] Error verifying name:', error);
      }
      
      console.log('✅ [DEBUG-CORE] Project creation complete');
      this.log('success', '✅ PROJECT CREATED SUCCESSFULLY');
      this.log('info', '═══════════════════════════════════════');
      
      return true;
      
    } catch (error) {
      console.error('❌ [DEBUG-CORE] Project creation failed:', error);
      this.log('error', `❌ PROJECT CREATION FAILED: ${error.message}`);
      this.log('error', `Stack: ${error.stack}`);
      return false;
    }
  }

  async processSingleStory(story, config) {
    console.log('═══════════════════════════════════════');
    console.log('🔍 [DEBUG-CORE] PROCESS STORY');
    console.log('═══════════════════════════════════════');
    console.log('Story:', story);
    console.log('Config:', config);
    
    this.config = config;
    this.isRunning = true;
    
    this.log('info', '═══════════════════════════════════════');
    this.log('info', `🎬 PROCESSING: ${story.name}`);
    this.log('info', '═══════════════════════════════════════');
    
    try {
      // Create project
      const projectCreated = await this.createNewProject(`MamaCat - ${story.name}`);
      
      if (!projectCreated) {
        throw new Error('Failed to create project');
      }
      
      this.log('success', '✅ Story processing complete');
      window.postMessage({ type: 'MAMACAT_STORY_COMPLETE' }, '*');
      
    } catch (error) {
      console.error('❌ [DEBUG-CORE] Story processing failed:', error);
      this.log('error', `❌ Story failed: ${error.message}`);
      window.postMessage({ type: 'MAMACAT_ERROR', error: error.message }, '*');
    }
  }

  stop() {
    this.isRunning = false;
    this.log('warning', '⏹️ Stopped');
  }

  getStepLog() {
    return this.stepLog.join('\n');
  }
}

// Make available globally
window.GoogleLabsAutomation = GoogleLabsAutomationDebug;

console.log('✅ [DEBUG-CORE] GoogleLabsAutomationDebug class loaded');
window.postMessage({ type: 'MAMACAT_CORE_READY' }, '*');

// Listen for messages
window.addEventListener('message', (event) => {
  if (event.source !== window) return;
  
  console.log('🔍 [DEBUG-CORE] Received message:', event.data.type);
  
  if (event.data.type === 'MAMACAT_STOP') {
    console.log('🔍 [DEBUG-CORE] Stop signal received');
    if (window.currentAutomation) {
      window.currentAutomation.stop();
    }
  } else if (event.data.type === 'MAMACAT_PROCESS_STORY') {
    console.log('🔍 [DEBUG-CORE] Process story signal received');
    const { story, config } = event.data;
    
    console.log('🔍 [DEBUG-CORE] Story:', story.name);
    console.log('🔍 [DEBUG-CORE] Config:', config);
    
    if (!window.currentAutomation) {
      console.log('🔍 [DEBUG-CORE] Creating new automation instance');
      window.currentAutomation = new GoogleLabsAutomationDebug();
    }
    
    console.log('🔍 [DEBUG-CORE] Starting story processing...');
    window.currentAutomation.processSingleStory(story, config);
  } else if (event.data.type === 'MAMACAT_GET_LOG') {
    console.log('🔍 [DEBUG-CORE] Log requested');
    if (window.currentAutomation) {
      const log = window.currentAutomation.getStepLog();
      window.postMessage({ type: 'MAMACAT_LOG_DATA', log: log }, '*');
    }
  }
});
