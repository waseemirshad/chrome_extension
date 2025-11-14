// Page Inspector - Run this in browser console to see available elements
// Copy and paste this into the browser console (F12) on Google Labs page

console.log('🔍 MamaCat Page Inspector');
console.log('═══════════════════════════════════════');

// Check for textareas
console.log('\n📝 TEXTAREAS:');
const textareas = document.querySelectorAll('textarea');
console.log(`Found ${textareas.length} textarea(s)`);
textareas.forEach((ta, i) => {
  console.log(`Textarea ${i + 1}:`, {
    id: ta.id,
    placeholder: ta.placeholder,
    className: ta.className,
    visible: ta.offsetParent !== null
  });
});

// Check for buttons
console.log('\n🔘 BUTTONS:');
const buttons = document.querySelectorAll('button');
console.log(`Found ${buttons.length} button(s)`);
buttons.forEach((btn, i) => {
  const text = btn.textContent?.trim().substring(0, 50);
  if (text && text.length > 0) {
    console.log(`Button ${i + 1}:`, {
      text: text,
      className: btn.className,
      ariaLabel: btn.getAttribute('aria-label'),
      visible: btn.offsetParent !== null
    });
  }
});

// Check for + buttons specifically
console.log('\n➕ PLUS BUTTONS:');
const plusButtons = Array.from(document.querySelectorAll('button')).filter(btn => {
  const html = btn.innerHTML;
  const text = btn.textContent;
  return html.includes('add') || text.includes('+') || text.includes('add');
});
console.log(`Found ${plusButtons.length} plus button(s)`);
plusButtons.forEach((btn, i) => {
  console.log(`Plus Button ${i + 1}:`, {
    innerHTML: btn.innerHTML.substring(0, 100),
    className: btn.className,
    visible: btn.offsetParent !== null
  });
});

// Check for file inputs
console.log('\n📁 FILE INPUTS:');
const fileInputs = document.querySelectorAll('input[type="file"]');
console.log(`Found ${fileInputs.length} file input(s)`);
fileInputs.forEach((input, i) => {
  console.log(`File Input ${i + 1}:`, {
    id: input.id,
    className: input.className,
    accept: input.accept
  });
});

// Check for icons
console.log('\n🎨 ICONS WITH "add":');
const addIcons = Array.from(document.querySelectorAll('i, span[class*="icon"]')).filter(el => {
  return el.textContent?.includes('add') || el.className?.includes('add');
});
console.log(`Found ${addIcons.length} add icon(s)`);
addIcons.forEach((icon, i) => {
  console.log(`Add Icon ${i + 1}:`, {
    tagName: icon.tagName,
    textContent: icon.textContent,
    className: icon.className
  });
});

// Check current URL and page state
console.log('\n🌐 PAGE INFO:');
console.log('URL:', window.location.href);
console.log('Title:', document.title);

// Check for specific Google Labs elements
console.log('\n🔍 GOOGLE LABS SPECIFIC:');
const flowElements = document.querySelectorAll('[class*="flow"], [class*="Flow"]');
console.log(`Found ${flowElements.length} flow-related elements`);

const ingredientElements = document.querySelectorAll('[class*="ingredient"], [class*="Ingredient"]');
console.log(`Found ${ingredientElements.length} ingredient-related elements`);

// Check for modals/dialogs
console.log('\n💬 DIALOGS/MODALS:');
const dialogs = document.querySelectorAll('dialog, [role="dialog"], [class*="modal"], [class*="Modal"]');
console.log(`Found ${dialogs.length} dialog(s)`);
dialogs.forEach((dialog, i) => {
  console.log(`Dialog ${i + 1}:`, {
    tagName: dialog.tagName,
    className: dialog.className,
    visible: dialog.offsetParent !== null,
    open: dialog.hasAttribute('open')
  });
});

console.log('\n═══════════════════════════════════════');
console.log('✅ Inspection complete!');
console.log('💡 Copy the output above and share it');
