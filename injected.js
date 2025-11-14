// Injected script - has access to page context
(function() {
  'use strict';
  
  console.log('🎬 MamaCat Automation - Injected Script Loaded');
  
  // Automation class
  class MamaCatAutomation {
    constructor() {
      this.ingredientMapping = {};
      this.isRunning = false;
    }
    
    // Wait helper
    async wait(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    // Find element with retry
    async findElement(selector, maxAttempts = 10) {
      for (let i = 0; i < maxAttempts; i++) {
        const element = document.querySelector(selector);
        if (element) return element;
        await this.wait(500);
      }
      throw new Error(`Element not found: ${selector}`);
    }
    
    // Find elements
    findElements(selector) {
      return Array.from(document.querySelectorAll(selector));
    }
    
    // Click element safely
    async clickElement(element) {
      element.scrollIntoView({ block: 'center' });
      await this.wait(300);
      element.click();
      await this.wait(500);
    }
    
    // Enter text in textarea
    async enterText(textarea, text) {
      textarea.scrollIntoView({ block: 'center' });
      await this.wait(500);
      
      textarea.focus();
      textarea.value = '';
      await this.wait(300);
      
      // Simulate typing
      textarea.value = text;
      textarea.dispatchEvent(new Event('input', { bubbles: true }));
      textarea.dispatchEvent(new Event('change', { bubbles: true }));
      await this.wait(500);
    }
  }
  
  // Make available globally
  window.MamaCatAutomation = MamaCatAutomation;
  
})();
