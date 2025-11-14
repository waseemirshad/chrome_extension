# 🔄 Replace Automation Core - Instructions

## What to Do

The file `automation-core-updated.js` contains the CORRECT selectors extracted from your Python script (`c1_video_generator.py`).

### Step 1: Backup Current File

```bash
# Rename current file as backup
mv chrome_extension/automation-core.js chrome_extension/automation-core-OLD.js
```

### Step 2: Use Updated File

```bash
# Rename updated file to active
mv chrome_extension/automation-core-updated.js chrome_extension/automation-core.js
```

### Step 3: Reload Extension

1. Go to `chrome://extensions/`
2. Find "MamaCat Video Generator"
3. Click the reload icon (🔄)

### Step 4: Test

1. Navigate to Google Labs Flow
2. Open sidebar
3. Upload files
4. Click "Setup & Verify"
5. Select a story
6. Click "Start Generation"

## What Changed

### ✅ Fixed Selectors

1. **Textarea**: Now uses `textarea[data-testid="prompt-textarea"]`
2. **Generate Button**: Finds button with `arrow_forward` icon
3. **Save Button**: Finds "Save as New Ingredient" text
4. **Plus Button**: Uses `button.sc-74578dc8-1.hopAJY`
5. **Remove Button**: Finds `i[text()='close']` icon
6. **XPath**: Uses exact XPath from Python for ingredient selection
7. **Gallery**: Uses `div[data-testid="virtuoso-scroller"]`

### ✅ Fixed Workflow

1. **Create Project**: Added proper project creation
2. **Switch Mode**: Added ingredients mode switching
3. **Generate Dialog**: Opens generate image dialog
4. **Timing**: Uses exact timing from Python (3s, 8s, 20s, 100s)
5. **Button Strategy**: FIRST for plus/remove, LAST for file input
6. **Gallery Index**: Correct calculation (2 + num - 1)

### ✅ Fixed Logic

1. **Reverse Order**: Generates/uploads in reverse
2. **Remove Cycle**: Clicks remove after each upload/save
3. **Extended Wait**: 8s → 5s → 5s... up to 100s
4. **Error Handling**: Continues on non-critical errors

## If It Still Doesn't Work

### Option 1: Run Page Inspector

1. Open Google Labs
2. Press F12 (DevTools)
3. Go to Console tab
4. Copy content of `page-inspector.js`
5. Paste and press Enter
6. Share the output with me

### Option 2: Manual Test

Try these in browser console:

```javascript
// Test 1: Find textarea
document.querySelector('textarea[data-testid="prompt-textarea"]')

// Test 2: Find generate button
Array.from(document.querySelectorAll('button')).find(b => b.innerHTML.includes('arrow_forward'))

// Test 3: Find plus button
document.querySelectorAll('button.sc-74578dc8-1.hopAJY')

// Test 4: Test XPath
document.evaluate("//textarea[@id='PINHOLE_TEXT_AREA_ELEMENT_ID']/following-sibling::div[contains(@class, 'sc-408537d4-0')]//button[contains(@class, 'hopAJY') and .//i[text()='add']]", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null).snapshotLength
```

### Option 3: Check Page State

Make sure you're:
- On the correct page: `https://labs.google/fx/tools/flow`
- In a project (not just homepage)
- In Ingredients mode (if applicable)
- Dialog is open (for generation)

## Expected Behavior

After replacing the file:

1. ✅ No more "Element not found: textarea" errors
2. ✅ Can find generate button
3. ✅ Can find save button
4. ✅ Can upload images
5. ✅ Can select ingredients
6. ✅ Can generate videos

## Troubleshooting

### Error: "Textarea not found"
- Make sure you're in the right dialog
- Check if page is fully loaded
- Run page inspector to see actual elements

### Error: "Generate button not found"
- Check if button is enabled
- Look for `arrow_forward` icon in HTML
- Button might have different class

### Error: "Plus button not found"
- Check if class names changed
- Google might have updated UI
- Try alternative selector

### Error: "Gallery not found"
- Wait longer for gallery to load
- Check if `data-testid` attribute exists
- Gallery might use different selector

## Success Indicators

You'll know it's working when you see:

```
[12:07:13 AM] 🆕 Creating new project...
[12:07:15 AM] 🔄 Switching to ingredients mode...
[12:07:17 AM] 🎨 Processing ingredients...
[12:07:17 AM] [GENERATE 06] Entering prompt...
[12:07:20 AM] ✅ Prompt entered
[12:07:23 AM] ✅ Generation started
[12:07:43 AM] ✅ Generation complete after 20s
[12:07:45 AM] ✅ Save button clicked
[12:07:53 AM] ✅ Save complete after 8s
[12:07:54 AM] ✅ Remove button clicked
```

## Need More Help?

If it still doesn't work after replacing the file:

1. Share the output from `page-inspector.js`
2. Share screenshots of the Google Labs page
3. Share the error messages from activity log
4. I'll create custom selectors for your specific page

---

**Remember**: The updated file has the EXACT selectors from your working Python script!
