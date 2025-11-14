# 🎯 Selector Reference - From Python Script

This document maps the exact selectors used in `c1_video_generator.py` to the Chrome extension.

## Key Selectors from Python Script

### 1. Textarea (Prompt Input)
**Python Line ~8500:**
```python
textarea = self.driver.find_element(By.CSS_SELECTOR, "textarea[data-testid='prompt-textarea']")
# Fallback: textarea[placeholder*="Describe"]
# Fallback: Any textarea
```

**Chrome Extension:**
```javascript
textarea = document.querySelector('textarea[data-testid="prompt-textarea"]');
```

### 2. Generate Button
**Python Line ~8560:**
```python
# Finds button with arrow_forward icon
buttons = self.driver.find_elements(By.TAG_NAME, "button")
for btn in buttons:
    if "arrow_forward" in btn.get_attribute("innerHTML"):
        if btn.is_enabled():
            generate_btn = btn
```

**Chrome Extension:**
```javascript
const buttons = document.querySelectorAll('button');
for (const btn of buttons) {
  if (btn.innerHTML.includes('arrow_forward') && !btn.disabled) {
    generateBtn = btn;
    break;
  }
}
```

### 3. Save as New Ingredient Button
**Python Line ~8710:**
```python
save_btn = self.driver.find_element(
    By.XPATH,
    "//button[contains(., 'Save as New Ingredient')]"
)
```

**Chrome Extension:**
```javascript
const saveBtn = Array.from(document.querySelectorAll('button')).find(btn => 
  btn.textContent.includes('Save as New Ingredient')
);
```

### 4. Plus Button (Add Ingredient)
**Python Line ~9050:**
```python
plus_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.sc-74578dc8-1.hopAJY")
first_plus_button = plus_buttons[0]  # Always use FIRST
```

**Chrome Extension:**
```javascript
const plusButtons = document.querySelectorAll('button.sc-74578dc8-1.hopAJY');
const firstPlusButton = plusButtons[0];
```

### 5. Remove Button (Close Icon)
**Python Line ~8850:**
```python
remove_buttons = self.driver.find_elements(
    By.XPATH, 
    "//button//i[text()='close']/.."
)
first_remove_button = remove_buttons[0]
```

**Chrome Extension:**
```javascript
const removeButtons = Array.from(document.querySelectorAll('button i'))
  .filter(i => i.textContent === 'close')
  .map(i => i.closest('button'));
const firstRemoveButton = removeButtons[0];
```

### 6. File Input
**Python Line ~9060:**
```python
file_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
file_inputs[-1].send_keys(ingredient_path)  # Use LAST file input
```

**Chrome Extension:**
```javascript
const fileInputs = document.querySelectorAll('input[type="file"]');
const targetInput = fileInputs[fileInputs.length - 1]; // Last one
```

### 7. Crop Button
**Python Line ~9070:**
```python
crop_btn = self.driver.find_element(
    By.XPATH,
    "//button[contains(., 'Crop and Save')]"
)
```

**Chrome Extension:**
```javascript
const cropBtn = Array.from(document.querySelectorAll('button')).find(btn =>
  btn.textContent.includes('Crop and Save')
);
```

### 8. Ingredient Selection XPath
**Python Line ~9450:**
```python
xpath = (
    "//textarea[@id='PINHOLE_TEXT_AREA_ELEMENT_ID']"
    "/following-sibling::div[contains(@class, 'sc-408537d4-0')]"
    "//button[contains(@class, 'hopAJY') and .//i[text()='add']]"
)
plus_buttons = document.evaluate(xpath, ...)
last_button = plus_buttons.snapshotItem(plus_buttons.snapshotLength - 1)
```

**Chrome Extension:**
```javascript
const xpath = "//textarea[@id='PINHOLE_TEXT_AREA_ELEMENT_ID']/following-sibling::div[contains(@class, 'sc-408537d4-0')]//button[contains(@class, 'hopAJY') and .//i[text()='add']]";
const result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
const lastButton = result.snapshotItem(result.snapshotLength - 1);
```

### 9. Gallery Container
**Python Line ~9480:**
```python
container = self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="virtuoso-scroller"]')
```

**Chrome Extension:**
```javascript
const container = document.querySelector('div[data-testid="virtuoso-scroller"]');
```

### 10. Gallery Item Selection
**Python Line ~9530:**
```python
# Calculate gallery index
ingredient_number = int(ingredient_num.lstrip('0')) or 1
gallery_index = 2 + ingredient_number - 1

# Select from gallery
btn = self.driver.find_element(By.CSS_SELECTOR, f'div[data-index="{gallery_index}"] button.sc-fbea20b2-9')
```

**Chrome Extension:**
```javascript
const ingredientNumber = parseInt(ingredientNum.replace(/^0+/, '')) || 1;
const galleryIndex = 2 + ingredientNumber - 1;
const button = document.querySelector(`div[data-index="${galleryIndex}"] button.sc-fbea20b2-9`);
```

## Workflow Steps

### Step 1: Create Project
1. Click create button
2. Enter project name
3. Wait for project to load

### Step 2: Switch to Ingredients Mode
1. Click "Ingredients" tab/button
2. Wait for mode switch

### Step 3: Generate Story Ingredient
1. Open "Generate Image" dialog
2. Find textarea by `data-testid="prompt-textarea"`
3. Enter prompt text
4. Wait 3 seconds
5. Click button with `arrow_forward` icon
6. Wait for "Save as New Ingredient" button (up to 100s)
7. Click "Save as New Ingredient"
8. Wait for remove button with `close` icon (up to 100s)
9. Click remove button
10. Repeat for each ingredient (in reverse order: 06→05→04→03)

### Step 4: Upload Base Cat Image
1. Find FIRST + button: `button.sc-74578dc8-1.hopAJY`
2. Click it
3. Find LAST file input: `input[type="file"]`
4. Convert base64 to File object
5. Attach file to input
6. Check for "Crop and Save" button
7. Click if present
8. Wait for remove button (up to 100s)
9. Click remove button
10. Repeat for each base cat (in reverse order: 02→01)

### Step 5: Select Ingredients for Prompt
1. Use XPath to find + buttons below textarea
2. Click LAST + button
3. Wait for gallery: `div[data-testid="virtuoso-scroller"]`
4. Calculate gallery index: `2 + ingredientNumber - 1`
5. Click button at that index
6. Repeat for each ingredient in prompt

### Step 6: Generate Video
1. Enter prompt in textarea
2. Click generate button
3. Wait for generation to complete

## Important Notes

### Timing (from Python)
- Wait 3 seconds before clicking generate
- Wait 20 seconds initially for generation
- Check every 5 seconds after that
- Maximum 100 seconds wait time
- Wait 8 seconds initially for upload/save
- Check every 5 seconds after that

### Button Selection Strategy
- **Plus buttons**: Always use FIRST one
- **Remove buttons**: Always use FIRST one
- **File inputs**: Always use LAST one
- **Ingredient + buttons**: Always use LAST one

### Gallery Index Calculation
```
Ingredient Number: 01, 02, 03, 04, 05, 06
Gallery Index:     2,  3,  4,  5,  6,  7

Formula: gallery_index = 2 + parseInt(ingredientNum) - 1
```

### Reverse Order Upload
- Story ingredients: 06 → 05 → 04 → 03
- Base cats: 02 → 01
- Result in gallery: 01, 02, 03, 04, 05, 06

## Testing Checklist

To verify selectors work:

- [ ] Can find textarea by `data-testid="prompt-textarea"`
- [ ] Can find generate button with `arrow_forward` icon
- [ ] Can find "Save as New Ingredient" button
- [ ] Can find + button with class `hopAJY`
- [ ] Can find remove button with `close` icon
- [ ] Can find file input
- [ ] Can find crop button
- [ ] Can use XPath for ingredient + buttons
- [ ] Can find gallery container
- [ ] Can select from gallery by index

## Next Steps

1. Replace `automation-core.js` with `automation-core-updated.js`
2. Test on Google Labs page
3. Use `page-inspector.js` to verify selectors if issues occur
4. Report any selector mismatches

---

**All selectors extracted from**: `c1_video_generator.py`  
**Last verified**: 2024
