// Updated automation core with correct selectors from Python script
// Based on c1_video_generator.py

class GoogleLabsAutomation {
  constructor() {
    this.driver = null; // Will be window.document
    this.ingredientMapping = {};
    this.isRunning = false;
    this.config = null;
  }

  async wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  log(type, message) {
    console.log(`[${type.toUpperCase()}] ${message}`);
    window.postMessage({
      type: 'MAMACAT_LOG',
      logType: type,
      message: message
    }, '*');
  }

  // ═══════════════════════════════════════════════════════════
  // STEP 1: CREATE NEW PROJECT
  // From Python: create_new_project()
  // ═══════════════════════════════════════════════════════════
  
  async createNewProject(projectName) {
    this.log('info', `🆕 Creating project: ${projectName}`);
    
    try {
      // Click "Create" or "New Project" button
      // Python uses: button with specific class or text
      const createButton = document.querySelector('button[aria-label*="Create"], button:has-text("Create")');
      
      if (createButton) {
        createButton.click();
        await this.wait(2000);
        this.log('success', '✅ Clicked create button');
      }
      
      // Enter project name
      // Python uses: input field or contenteditable
      const nameInput = document.querySelector('input[type="text"], [contenteditable="true"]');
      
      if (nameInput) {
        nameInput.focus();
        await this.wait(500);
        
        // Clear and enter name
        if (nameInput.tagName === 'INPUT') {
          nameInput.value = projectName;
          nameInput.dispatchEvent(new Event('input', { bubbles: true }));
        } else {
          nameInput.textContent = projectName;
        }
        
        await this.wait(1000);
        this.log('success', `✅ Project named: ${projectName}`);
      }
      
      return true;
    } catch (error) {
      this.log('error', `Failed to create project: ${error.message}`);
      return false;
    }
  }

  // ═══════════════════════════════════════════════════════════
  // STEP 2: SWITCH TO INGREDIENTS MODE
  // From Python: switch_to_ingredients_mode()
  // ═══════════════════════════════════════════════════════════
  
  async switchToIngredientsMode() {
    this.log('info', '🔄 Switching to Ingredients mode...');
    
    try {
      // Look for Ingredients tab/button
      // Python uses: button or tab with "Ingredients" text
      const ingredientsButton = document.querySelector(
        'button:has-text("Ingredients"), [role="tab"]:has-text("Ingredients")'
      );
      
      if (ingredientsButton) {
        ingredientsButton.click();
        await this.wait(2000);
        this.log('success', '✅ Switched to Ingredients mode');
        return true;
      }
      
      this.log('warning', 'Ingredients button not found, might already be in mode');
      return true;
    } catch (error) {
      this.log('error', `Failed to switch mode: ${error.message}`);
      return false;
    }
  }

  // ═══════════════════════════════════════════════════════════
  // STEP 3: OPEN GENERATE IMAGE DIALOG
  // From Python: open_generate_image_dialog()
  // ═══════════════════════════════════════════════════════════
  
  async openGenerateImageDialog() {
    this.log('info', '🖼️ Opening Generate Image dialog...');
    
    try {
      // Look for Generate Image button
      const generateButton = document.querySelector(
        'button:has-text("Generate Image"), button:has-text("Generate"), button[aria-label*="Generate"]'
      );
      
      if (generateButton) {
        generateButton.click();
        await this.wait(2000);
        this.log('success', '✅ Generate Image dialog opened');
        return true;
      }
      
      this.log('warning', 'Generate button not found');
      return false;
    } catch (error) {
      this.log('error', `Failed to open dialog: ${error.message}`);
      return false;
    }
  }

  // ═══════════════════════════════════════════════════════════
  // STEP 4: ENTER PROMPT AND GENERATE
  // From Python: enter_prompt_and_generate()
  // Uses: textarea[data-testid='prompt-textarea'] or by placeholder
  // ═══════════════════════════════════════════════════════════
  
  async enterPromptAndGenerate(promptText, ingredientNum) {
    this.log('info', `[GENERATE ${ingredientNum}] Entering prompt...`);
    
    try {
      // Find textarea - EXACT selectors from Python
      let textarea = null;
      
      // Method 1: By data-testid (Python line ~8500)
      textarea = document.querySelector('textarea[data-testid="prompt-textarea"]');
      
      // Method 2: By placeholder
      if (!textarea) {
        textarea = document.querySelector('textarea[placeholder*="Describe"]');
      }
      
      // Method 3: Any textarea
      if (!textarea) {
        const textareas = document.querySelectorAll('textarea');
        if (textareas.length > 0) textarea = textareas[0];
      }
      
      if (!textarea) {
        throw new Error('Textarea not found');
      }
      
      // Scroll to element
      textarea.scrollIntoView({ block: 'center' });
      await this.wait(1000);
      
      // Click to focus
      textarea.click();
      await this.wait(500);
      
      // Clear existing text
      textarea.value = '';
      await this.wait(300);
      
      // Enter new text
      textarea.value = promptText;
      textarea.dispatchEvent(new Event('input', { bubbles: true }));
      textarea.dispatchEvent(new Event('change', { bubbles: true }));
      
      await this.wait(500);
      
      this.log('success', `[GENERATE ${ingredientNum}] ✅ Prompt entered`);
      
      // Wait 3 seconds before clicking generate (Python line ~8550)
      this.log('info', `[GENERATE ${ingredientNum}] ⏳ Waiting 3 seconds...`);
      await this.wait(3000);
      
      // Click generate button - EXACT selector from Python
      // Python uses: button with arrow_forward icon (line ~8560)
      let generateBtn = null;
      
      // Method 1: By icon (Python's primary method)
      const buttons = document.querySelectorAll('button');
      for (const btn of buttons) {
        const html = btn.innerHTML;
        if (html.includes('arrow_forward') && btn.disabled === false) {
          generateBtn = btn;
          break;
        }
      }
      
      if (!generateBtn) {
        throw new Error('Generate button not found');
      }
      
      generateBtn.scrollIntoView({ block: 'center' });
      await this.wait(500);
      generateBtn.click();
      
      this.log('success', `[GENERATE ${ingredientNum}] ✅ Generation started`);
      return true;
      
    } catch (error) {
      this.log('error', `[GENERATE ${ingredientNum}] Failed: ${error.message}`);
      return false;
    }
  }

  // ═══════════════════════════════════════════════════════════
  // STEP 5: WAIT FOR GENERATION COMPLETE
  // From Python: wait_for_generation_complete_extended()
  // Waits for "Save as New Ingredient" button to appear
  // ═══════════════════════════════════════════════════════════
  
  async waitForGenerationComplete(ingredientNum, maxWait = 100) {
    this.log('info', `[WAIT ${ingredientNum}] Waiting for generation...`);
    
    let totalWaited = 0;
    const checkInterval = 5;
    
    // First wait: 20 seconds (Python line ~8620)
    await this.wait(20000);
    totalWaited = 20;
    
    // Check for Save button
    while (totalWaited < maxWait) {
      // Python uses: button with "Save as New Ingredient" text (line ~8680)
      const saveBtn = document.querySelector('button:has-text("Save as New Ingredient")') ||
                      Array.from(document.querySelectorAll('button')).find(btn => 
                        btn.textContent.includes('Save as New Ingredient')
                      );
      
      if (saveBtn && saveBtn.offsetParent !== null) {
        this.log('success', `[WAIT ${ingredientNum}] ✅ Generation complete after ${totalWaited}s`);
        return true;
      }
      
      await this.wait(checkInterval * 1000);
      totalWaited += checkInterval;
      
      if (totalWaited % 10 === 0) {
        this.log('info', `[WAIT ${ingredientNum}] Still generating... (${totalWaited}/${maxWait}s)`);
      }
    }
    
    this.log('warning', `[WAIT ${ingredientNum}] Timeout after ${maxWait}s`);
    return false;
  }

  // ═══════════════════════════════════════════════════════════
  // STEP 6: CLICK SAVE AS NEW INGREDIENT
  // From Python: click_save_as_new_ingredient()
  // ═══════════════════════════════════════════════════════════
  
  async clickSaveAsNewIngredient(ingredientNum) {
    this.log('info', `[SAVE ${ingredientNum}] Clicking save button...`);
    
    try {
      // Python uses multiple methods to find button (line ~8710)
      const saveBtn = document.querySelector('button:has-text("Save as New Ingredient")') ||
                      Array.from(document.querySelectorAll('button')).find(btn => 
                        btn.textContent.includes('Save as New Ingredient')
                      );
      
      if (!saveBtn) {
        throw new Error('Save button not found');
      }
      
      saveBtn.scrollIntoView({ block: 'center' });
      await this.wait(500);
      saveBtn.click();
      await this.wait(3000);
      
      this.log('success', `[SAVE ${ingredientNum}] ✅ Save button clicked`);
      return true;
    } catch (error) {
      this.log('error', `[SAVE ${ingredientNum}] Failed: ${error.message}`);
      return false;
    }
  }

  // ═══════════════════════════════════════════════════════════
  // STEP 7: WAIT FOR SAVE COMPLETE AND REMOVE
  // From Python: wait_for_save_complete_extended()
  // Waits for remove button, then clicks it
  // ═══════════════════════════════════════════════════════════
  
  async waitForSaveCompleteAndRemove(ingredientNum, maxWait = 100) {
    this.log('info', `[SAVE WAIT ${ingredientNum}] Waiting for save...`);
    
    let totalWaited = 0;
    
    // First wait: 8 seconds (Python line ~8780)
    await this.wait(8000);
    totalWaited = 8;
    
    // Check for remove button - EXACT selector from Python (line ~8800)
    while (totalWaited < maxWait) {
      // Python uses: button with 'close' icon
      const removeButtons = Array.from(document.querySelectorAll('button i')).filter(i => 
        i.textContent === 'close'
      ).map(i => i.closest('button'));
      
      if (removeButtons.length > 0) {
        this.log('success', `[SAVE WAIT ${ingredientNum}] ✅ Save complete after ${totalWaited}s`);
        
        // Click remove button immediately (Python line ~8850)
        const removeBtn = removeButtons[0];
        removeBtn.click();
        await this.wait(1000);
        
        this.log('success', `[SAVE WAIT ${ingredientNum}] ✅ Remove button clicked`);
        return true;
      }
      
      await this.wait(5000);
      totalWaited += 5;
    }
    
    this.log('warning', `[SAVE WAIT ${ingredientNum}] Timeout, continuing anyway`);
    return true;
  }

  // ═══════════════════════════════════════════════════════════
  // STEP 8: UPLOAD BASE CAT IMAGE
  // From Python: upload_single_ingredient_with_monitoring()
  // Uses: button.sc-74578dc8-1.hopAJY (+ button)
  // ═══════════════════════════════════════════════════════════
  
  async uploadSingleIngredient(imageData, ingredientNum) {
    this.log('info', `[UPLOAD ${ingredientNum}] Uploading: ${imageData.name}`);
    
    try {
      // Find FIRST + button - EXACT selector from Python (line ~9050)
      const plusButtons = document.querySelectorAll('button.sc-74578dc8-1.hopAJY');
      
      if (plusButtons.length === 0) {
        throw new Error('No + button found');
      }
      
      const firstPlusButton = plusButtons[0];
      firstPlusButton.click();
      await this.wait(2000);
      
      // Find file input (Python line ~9060)
      const fileInputs = document.querySelectorAll('input[type="file"]');
      
      if (fileInputs.length === 0) {
        throw new Error('No file input found');
      }
      
      // Convert base64 to File object
      const file = await this.base64ToFile(imageData.data, imageData.name, imageData.type);
      
      // Create DataTransfer
      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(file);
      const targetInput = fileInputs[fileInputs.length - 1];
      targetInput.files = dataTransfer.files;
      
      // Trigger change event
      targetInput.dispatchEvent(new Event('change', { bubbles: true }));
      
      await this.wait(3000);
      
      // Check for crop button (Python line ~9070)
      const cropBtn = Array.from(document.querySelectorAll('button')).find(btn =>
        btn.textContent.includes('Crop and Save') || btn.textContent.includes('Crop & Save')
      );
      
      if (cropBtn) {
        cropBtn.click();
        await this.wait(3000);
        this.log('success', `[UPLOAD ${ingredientNum}] ✅ Cropped`);
      }
      
      // Wait for upload complete (same logic as save)
      await this.waitForUploadCompleteAndRemove(ingredientNum);
      
      this.log('success', `[UPLOAD ${ingredientNum}] ✅ Complete`);
      return true;
      
    } catch (error) {
      this.log('error', `[UPLOAD ${ingredientNum}] Failed: ${error.message}`);
      return false;
    }
  }

  async waitForUploadCompleteAndRemove(ingredientNum) {
    // Same logic as waitForSaveCompleteAndRemove
    return await this.waitForSaveCompleteAndRemove(ingredientNum);
  }

  async base64ToFile(base64Data, filename, mimeType) {
    const base64 = base64Data.split(',')[1] || base64Data;
    const binaryString = atob(base64);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    return new File([bytes], filename, { type: mimeType });
  }

  // ═══════════════════════════════════════════════════════════
  // STEP 9: SELECT INGREDIENTS FOR PROMPT
  // From Python: select_ingredients_for_prompt()
  // Uses: XPath to find + buttons, then gallery selection
  // ═══════════════════════════════════════════════════════════
  
  async selectIngredientsForPrompt(ingredientNumbers) {
    if (!ingredientNumbers || ingredientNumbers.trim() === '') {
      return true;
    }
    
    const ingredients = ingredientNumbers.split(',').map(n => n.trim());
    this.log('info', `[SELECT] Selecting: ${ingredients.join(', ')}`);
    
    for (let i = 0; i < ingredients.length; i++) {
      const ingredientNum = ingredients[i];
      
      try {
        // Find + buttons - EXACT XPath from Python (line ~9450)
        const xpath = "//textarea[@id='PINHOLE_TEXT_AREA_ELEMENT_ID']/following-sibling::div[contains(@class, 'sc-408537d4-0')]//button[contains(@class, 'hopAJY') and .//i[text()='add']]";
        
        const result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
        
        if (result.snapshotLength === 0) {
          throw new Error('No + buttons found');
        }
        
        // Click LAST + button (Python line ~9470)
        const lastButton = result.snapshotItem(result.snapshotLength - 1);
        lastButton.scrollIntoView({ block: 'center' });
        await this.wait(500);
        lastButton.click();
        await this.wait(1500);
        
        // Wait for gallery (Python line ~9480)
        await this.waitForGallery();
        
        // Select from gallery (Python line ~9490)
        await this.selectFromGallery(ingredientNum);
        
        this.log('success', `[SELECT] ✅ Ingredient ${ingredientNum} selected`);
        
      } catch (error) {
        this.log('error', `[SELECT] Failed ${ingredientNum}: ${error.message}`);
      }
    }
    
    return true;
  }

  async waitForGallery() {
    for (let i = 0; i < 10; i++) {
      const container = document.querySelector('div[data-testid="virtuoso-scroller"]');
      if (container) {
        await this.wait(2000);
        return true;
      }
      await this.wait(1000);
    }
    return false;
  }

  async selectFromGallery(ingredientNum) {
    // Calculate gallery index - Python logic (line ~9520)
    const ingredientNumber = parseInt(ingredientNum.replace(/^0+/, '')) || 1;
    const galleryIndex = 2 + ingredientNumber - 1;
    
    this.log('info', `[SELECT] Gallery index ${galleryIndex} for ingredient ${ingredientNum}`);
    
    // Try multiple selectors (Python line ~9530)
    const selectors = [
      `div[data-index="${galleryIndex}"] button.sc-fbea20b2-9`,
      `div[data-index="${galleryIndex}"] button`
    ];
    
    for (const selector of selectors) {
      try {
        const button = document.querySelector(selector);
        if (button && button.offsetParent !== null) {
          button.click();
          await this.wait(500);
          return true;
        }
      } catch (error) {
        continue;
      }
    }
    
    throw new Error(`Could not select ingredient at index ${galleryIndex}`);
  }

  // ═══════════════════════════════════════════════════════════
  // MAIN STORY PROCESSING
  // ═══════════════════════════════════════════════════════════
  
  async processSingleStory(story, config) {
    this.config = config;
    this.isRunning = true;
    
    this.log('info', '═══════════════════════════════════════');
    this.log('info', `🎬 PROCESSING: ${story.name}`);
    this.log('info', '═══════════════════════════════════════');
    
    try {
      // Step 1: Create project
      await this.createNewProject(`MamaCat - ${story.name}`);
      
      // Step 2: Switch to ingredients mode
      await this.switchToIngredientsMode();
      
      // Step 3: Generate story ingredients (reverse order)
      const ingredients = story.ingredients || [];
      if (ingredients.length > 0) {
        const reversed = ingredients.slice().reverse();
        for (const ingredient of reversed) {
          if (!this.isRunning) break;
          
          await this.openGenerateImageDialog();
          await this.enterPromptAndGenerate(ingredient.Prompt, ingredient.Ingredient_No);
          await this.waitForGenerationComplete(ingredient.Ingredient_No);
          await this.clickSaveAsNewIngredient(ingredient.Ingredient_No);
          await this.waitForSaveCompleteAndRemove(ingredient.Ingredient_No);
        }
      }
      
      // Step 4: Upload base cats (reverse order)
      const baseCats = config.baseCatImages || [];
      if (baseCats.length > 0) {
        const reversed = baseCats.slice().reverse();
        for (const baseCat of reversed) {
          if (!this.isRunning) break;
          const num = baseCat.name.match(/(\d+)/)?.[1] || '00';
          await this.uploadSingleIngredient(baseCat, num);
        }
      }
      
      // Step 5: Process prompts
      const prompts = story.prompts || [];
      for (let i = 0; i < prompts.length; i++) {
        if (!this.isRunning) break;
        
        const prompt = prompts[i];
        await this.selectIngredientsForPrompt(prompt.Ingredients_No || '');
        await this.enterPromptAndGenerate(prompt.Prompt, i + 1);
      }
      
      this.log('success', `✅ Story "${story.name}" completed!`);
      window.postMessage({ type: 'MAMACAT_STORY_COMPLETE' }, '*');
      
    } catch (error) {
      this.log('error', `Story failed: ${error.message}`);
      window.postMessage({ type: 'MAMACAT_ERROR', error: error.message }, '*');
    }
  }

  stop() {
    this.isRunning = false;
    this.log('warning', '⏹️ Stopped');
  }
}

// Make available globally
window.GoogleLabsAutomation = GoogleLabsAutomation;

// Listen for messages
window.addEventListener('message', (event) => {
  if (event.source !== window) return;
  
  if (event.data.type === 'MAMACAT_STOP') {
    if (window.currentAutomation) {
      window.currentAutomation.stop();
    }
  } else if (event.data.type === 'MAMACAT_PROCESS_STORY') {
    const { story, config } = event.data;
    
    if (!window.currentAutomation) {
      window.currentAutomation = new GoogleLabsAutomation();
    }
    
    window.currentAutomation.processSingleStory(story, config);
  }
});
