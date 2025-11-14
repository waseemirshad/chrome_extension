// Automation core with correct selectors from Python script
// Based on c1_video_generator.py

class GoogleLabsAutomation {
  constructor() {
    this.driver = null;
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

  // Helper to find element by XPath
  getElementByXPath(xpath) {
    return document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
  }

  getElementsByXPath(xpath) {
    const result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
    const nodes = [];
    for (let i = 0; i < result.snapshotLength; i++) {
      nodes.push(result.snapshotItem(i));
    }
    return nodes;
  }

  // ═══════════════════════════════════════════════════════════
  // STEP 1: CREATE NEW PROJECT
  // Based on Python: create_new_project() and rename_project()
  // Clicks: button with "New project" text
  // Then: Edit button (pencil icon), input field, save
  // ═══════════════════════════════════════════════════════════
  
  async createNewProject(projectName) {
    this.log('info', `🆕 Creating project: ${projectName}`);
    
    try {
      // Step 1: Click "New project" button - EXACT from Python (line 2533-2543)
      // Selector from user: button.sc-c177465c-1.hVamcH.sc-a38764c7-0.fXsrxE
      this.log('info', '[PROJECT] Looking for New Project button...');
      
      let newProjectBtn = null;
      
      // Method 1: By class (from user's HTML)
      newProjectBtn = document.querySelector('button.sc-c177465c-1.hVamcH.sc-a38764c7-0.fXsrxE');
      
      // Method 2: By text content (Python's method)
      if (!newProjectBtn) {
        const buttons = document.querySelectorAll('button');
        for (const btn of buttons) {
          if (btn.textContent.toLowerCase().includes('new project')) {
            newProjectBtn = btn;
            break;
          }
        }
      }
      
      // Method 3: XPath
      if (!newProjectBtn) {
        newProjectBtn = this.getElementByXPath("//button[contains(., 'New project')]");
      }
      
      if (!newProjectBtn) {
        throw new Error('New Project button not found');
      }
      
      this.log('success', '[PROJECT] ✅ Found New Project button');
      newProjectBtn.click();
      await this.wait(3000);
      this.log('success', '[PROJECT] ✅ Clicked New Project button');
      
      // Step 2: Rename project - EXACT from Python (line 2564-2615)
      await this.renameProject(projectName);
      
      return true;
    } catch (error) {
      this.log('error', `[PROJECT] Failed to create: ${error.message}`);
      console.error('Create project error:', error);
      return false;
    }
  }
  
  async renameProject(projectName) {
    this.log('info', `[RENAME] Renaming to: ${projectName}`);
    
    try {
      await this.wait(2000);
      
      // Find edit button (pencil icon) - EXACT from Python (line 2575-2583)
      // User's selector: button with i.google-symbols containing "edit"
      let editBtn = null;
      
      // Method 1: By XPath (Python's primary method)
      editBtn = this.getElementByXPath("//button[.//i[contains(@class, 'google-symbols') and contains(., 'edit')]]");
      
      // Method 2: By searching buttons (Python's fallback)
      if (!editBtn) {
        const buttons = document.querySelectorAll('button');
        for (const btn of buttons) {
          if (btn.innerHTML.toLowerCase().includes('edit')) {
            editBtn = btn;
            break;
          }
        }
      }
      
      if (!editBtn) {
        throw new Error('Edit button (pencil icon) not found');
      }
      
      this.log('success', '[RENAME] ✅ Found edit button');
      editBtn.click();
      await this.wait(1000);
      this.log('success', '[RENAME] ✅ Clicked edit button');
      
      // Find input field - EXACT from Python (line 2587-2589)
      const inputs = document.querySelectorAll('input[type="text"]');
      
      if (inputs.length === 0) {
        throw new Error('Name input field not found');
      }
      
      const nameInput = inputs[0];
      this.log('success', '[RENAME] ✅ Found input field');
      
      // Clear and enter name - EXACT from Python (line 2590-2597)
      nameInput.click();
      await this.wait(500);
      
      // Select all and delete
      nameInput.select();
      await this.wait(300);
      nameInput.value = '';
      await this.wait(300);
      
      // Enter new name
      nameInput.value = projectName;
      nameInput.dispatchEvent(new Event('input', { bubbles: true }));
      await this.wait(500);
      
      this.log('success', `[RENAME] ✅ Entered name: ${projectName}`);
      
      // Save - EXACT from Python (line 2600-2607)
      // Look for check icon button
      let saveBtn = this.getElementByXPath("//button[.//i[contains(@class, 'google-symbols') and contains(., 'check')]]");
      
      if (saveBtn) {
        saveBtn.click();
        this.log('success', '[RENAME] ✅ Clicked save button');
      } else {
        // Fallback: Press Enter
        nameInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true }));
        this.log('success', '[RENAME] ✅ Pressed Enter to save');
      }
      
      await this.wait(2000);
      this.log('success', `[RENAME] ✅ Project renamed to: ${projectName}`);
      
      return true;
    } catch (error) {
      this.log('error', `[RENAME] Failed: ${error.message}`);
      console.error('Rename error:', error);
      return false;
    }
  }

  // ═══════════════════════════════════════════════════════════
  // STEP 2: SWITCH TO INGREDIENTS MODE
  // ═══════════════════════════════════════════════════════════
  
  async switchToIngredientsMode() {
    this.log('info', '🔄 Switching to Ingredients mode...');
    
    try {
      // Look for Ingredients tab/button
      const ingredientsButton = Array.from(document.querySelectorAll('button, [role="tab"]')).find(btn =>
        btn.textContent.includes('Ingredients')
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
  // ═══════════════════════════════════════════════════════════
  
  async openGenerateImageDialog() {
    this.log('info', '🖼️ Opening Generate Image dialog...');
    
    try {
      const generateButton = Array.from(document.querySelectorAll('button')).find(btn =>
        btn.textContent.includes('Generate Image') || btn.textContent.includes('Generate')
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
  // From Python: Uses textarea[data-testid='prompt-textarea']
  // ═══════════════════════════════════════════════════════════
  
  async enterPromptAndGenerate(promptText, ingredientNum) {
    this.log('info', `[GENERATE ${ingredientNum}] Entering prompt...`);
    
    try {
      // Find textarea - EXACT methods from Python
      let textarea = null;
      
      // Method 1: By data-testid (Python line 817)
      textarea = document.querySelector('textarea[data-testid="prompt-textarea"]');
      
      // Method 2: By placeholder (Python line 824)
      if (!textarea) {
        textarea = this.getElementByXPath("//textarea[contains(@placeholder, 'Describe')]");
      }
      
      // Method 3: Any textarea (Python line 831)
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
      
      // Clear existing text (Python line 854-859)
      textarea.click();
      await this.wait(300);
      textarea.value = '';
      await this.wait(300);
      
      // Enter new text (Python line 862-863)
      textarea.value = promptText;
      textarea.dispatchEvent(new Event('input', { bubbles: true }));
      textarea.dispatchEvent(new Event('change', { bubbles: true }));
      
      await this.wait(500);
      
      this.log('success', `[GENERATE ${ingredientNum}] ✅ Prompt entered`);
      
      // Wait 3 seconds before clicking generate (Python line 880-884)
      this.log('info', `[GENERATE ${ingredientNum}] ⏳ Waiting 3 seconds...`);
      await this.wait(3000);
      
      // Click generate button - EXACT selector from Python (line 892-895)
      let generateBtn = null;
      
      // Method 1: By icon (Python's primary method)
      generateBtn = this.getElementByXPath("//button[.//i[contains(@class, 'google-symbols') and contains(., 'arrow_forward')]]");
      
      // Method 2: Find all buttons and check innerHTML (Python line 901-907)
      if (!generateBtn) {
        const buttons = document.querySelectorAll('button');
        for (const btn of buttons) {
          if (btn.innerHTML.includes('arrow_forward') && !btn.disabled) {
            generateBtn = btn;
            break;
          }
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
    
    // Check for Save button (Python line 996-1010)
    while (totalWaited < maxWait) {
      // Method 1: By icon and text (Python line 996-999)
      let saveBtn = this.getElementByXPath("//button[.//i[contains(text(), 'add_photo_alternate')] and contains(., 'Save as New Ingredient')]");
      
      // Method 2: Simple text search (Python line 1007-1010)
      if (!saveBtn) {
        saveBtn = this.getElementByXPath("//button[contains(., 'Save as New Ingredient')]");
      }
      
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
      let saveBtn = null;
      
      // Method 1: By icon and text (Python line 1031-1035)
      saveBtn = this.getElementByXPath("//button[.//i[contains(text(), 'add_photo_alternate')] and contains(., 'Save as New Ingredient')]");
      
      // Method 2: By class and text (Python line 1042-1046)
      if (!saveBtn) {
        saveBtn = this.getElementByXPath("//button[contains(@class, 'sc-c177465c-1') and contains(., 'Save as New Ingredient')]");
      }
      
      // Method 3: Simple text search (Python line 1053-1057)
      if (!saveBtn) {
        saveBtn = this.getElementByXPath("//button[contains(., 'Save as New Ingredient')]");
      }
      
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
    
    // Check for remove button - EXACT selector from Python (line 1102, 1108)
    while (totalWaited < maxWait) {
      // Method 1: Full selector (Python line 1102)
      let removeButtons = this.getElementsByXPath("//button[contains(@class, 'sc-c177465c-1') and contains(@class, 'hVamcH') and contains(@class, 'sc-74578dc8-1')]//i[text()='close']/..");
      
      // Method 2: Alternative selector (Python line 1108)
      if (removeButtons.length === 0) {
        removeButtons = this.getElementsByXPath("//button//i[text()='close']/..");
      }
      
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
      // Find FIRST + button - EXACT selector from Python (line 529)
      const plusButtons = document.querySelectorAll('button.sc-74578dc8-1.hopAJY');
      
      if (plusButtons.length === 0) {
        throw new Error('No + button found');
      }
      
      const firstPlusButton = plusButtons[0];
      firstPlusButton.click();
      await this.wait(2000);
      
      // Find file input (Python line 544)
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
      
      // Check for crop button (Python line 551-554)
      const cropBtn = this.getElementByXPath("//button[contains(., 'Crop and Save') or contains(., 'Crop & Save') or contains(., 'Crop and save')]");
      
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
        
        const plusButtons = this.getElementsByXPath(xpath);
        
        if (plusButtons.length === 0) {
          throw new Error('No + buttons found');
        }
        
        // Click LAST + button (Python line ~9470)
        const lastButton = plusButtons[plusButtons.length - 1];
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
    
    console.log('[AUTOMATION] Starting processSingleStory');
    console.log('[AUTOMATION] Story:', story);
    console.log('[AUTOMATION] Config:', config);
    
    this.log('info', '═══════════════════════════════════════');
    this.log('info', `🎬 PROCESSING: ${story.name}`);
    this.log('info', '═══════════════════════════════════════');
    
    try {
      // Step 1: Create project
      this.log('info', '[STEP 1] Creating new project...');
      console.log('[AUTOMATION] Step 1: Creating project');
      const projectCreated = await this.createNewProject(`MamaCat - ${story.name}`);
      
      if (!projectCreated) {
        throw new Error('Failed to create project');
      }
      
      this.log('success', '[STEP 1] ✅ Project created');
      
      // Step 2: Switch to ingredients mode
      this.log('info', '[STEP 2] Switching to ingredients mode...');
      console.log('[AUTOMATION] Step 2: Switching mode');
      const modeSwitched = await this.switchToIngredientsMode();
      
      if (!modeSwitched) {
        this.log('warning', '[STEP 2] ⚠️ Could not switch mode, continuing anyway');
      } else {
        this.log('success', '[STEP 2] ✅ Mode switched');
      }
      
      // Step 3: Generate story ingredients (reverse order)
      const ingredients = story.ingredients || [];
      if (ingredients.length > 0) {
        this.log('info', `[STEP 3] Generating ${ingredients.length} story ingredients...`);
        console.log('[AUTOMATION] Step 3: Generating ingredients');
        
        const reversed = ingredients.slice().reverse();
        for (let i = 0; i < reversed.length; i++) {
          if (!this.isRunning) {
            this.log('warning', '⏹️ Stopped by user');
            break;
          }
          
          const ingredient = reversed[i];
          this.log('info', `[INGREDIENT ${i + 1}/${reversed.length}] ${ingredient.Ingredient_No}`);
          
          await this.openGenerateImageDialog();
          await this.enterPromptAndGenerate(ingredient.Prompt, ingredient.Ingredient_No);
          await this.waitForGenerationComplete(ingredient.Ingredient_No);
          await this.clickSaveAsNewIngredient(ingredient.Ingredient_No);
          await this.waitForSaveCompleteAndRemove(ingredient.Ingredient_No);
        }
        
        this.log('success', '[STEP 3] ✅ All ingredients generated');
      } else {
        this.log('info', '[STEP 3] No story ingredients to generate');
      }
      
      // Step 4: Upload base cats (reverse order)
      const baseCats = config.baseCatImages || [];
      if (baseCats.length > 0) {
        this.log('info', `[STEP 4] Uploading ${baseCats.length} base cat images...`);
        console.log('[AUTOMATION] Step 4: Uploading base cats');
        
        const reversed = baseCats.slice().reverse();
        for (let i = 0; i < reversed.length; i++) {
          if (!this.isRunning) {
            this.log('warning', '⏹️ Stopped by user');
            break;
          }
          
          const baseCat = reversed[i];
          const num = baseCat.name.match(/(\d+)/)?.[1] || '00';
          this.log('info', `[BASE CAT ${i + 1}/${reversed.length}] ${baseCat.name}`);
          
          await this.uploadSingleIngredient(baseCat, num);
        }
        
        this.log('success', '[STEP 4] ✅ Base cats uploaded');
      } else {
        this.log('info', '[STEP 4] No base cat images to upload');
      }
      
      // Step 5: Process prompts
      const prompts = story.prompts || [];
      if (prompts.length > 0) {
        this.log('info', `[STEP 5] Processing ${prompts.length} prompts...`);
        console.log('[AUTOMATION] Step 5: Processing prompts');
        
        for (let i = 0; i < prompts.length; i++) {
          if (!this.isRunning) {
            this.log('warning', '⏹️ Stopped by user');
            break;
          }
          
          const prompt = prompts[i];
          this.log('info', `[PROMPT ${i + 1}/${prompts.length}] Processing...`);
          
          await this.selectIngredientsForPrompt(prompt.Ingredients_No || '');
          await this.enterPromptAndGenerate(prompt.Prompt, i + 1);
        }
        
        this.log('success', '[STEP 5] ✅ All prompts processed');
      } else {
        this.log('info', '[STEP 5] No prompts to process');
      }
      
      this.log('success', `✅ Story "${story.name}" completed!`);
      console.log('[AUTOMATION] Story completed successfully');
      window.postMessage({ type: 'MAMACAT_STORY_COMPLETE' }, '*');
      
    } catch (error) {
      console.error('[AUTOMATION] Story processing error:', error);
      this.log('error', `❌ Story failed: ${error.message}`);
      this.log('error', `💡 Error details: ${error.stack || 'No stack trace'}`);
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

// Signal that the core is ready
console.log('🎬 GoogleLabsAutomation class loaded and ready');
window.postMessage({ type: 'MAMACAT_CORE_READY' }, '*');

// Listen for messages
window.addEventListener('message', (event) => {
  if (event.source !== window) return;
  
  console.log('[AUTOMATION-CORE] Received message:', event.data.type);
  
  if (event.data.type === 'MAMACAT_STOP') {
    console.log('[AUTOMATION-CORE] Stop signal received');
    if (window.currentAutomation) {
      window.currentAutomation.stop();
    }
  } else if (event.data.type === 'MAMACAT_PROCESS_STORY') {
    console.log('[AUTOMATION-CORE] Process story signal received');
    const { story, config } = event.data;
    
    console.log('[AUTOMATION-CORE] Story:', story.name);
    console.log('[AUTOMATION-CORE] Config:', config);
    
    if (!window.currentAutomation) {
      console.log('[AUTOMATION-CORE] Creating new automation instance');
      window.currentAutomation = new GoogleLabsAutomation();
    }
    
    console.log('[AUTOMATION-CORE] Starting story processing...');
    window.currentAutomation.processSingleStory(story, config);
  }
});
