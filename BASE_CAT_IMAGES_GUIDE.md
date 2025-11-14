# 🐱 Base Cat Images - Complete Guide

## What Are Base Cat Images?

Base cat images are **pre-existing photos** of your cat characters that are used across all stories:

- **01.jpeg**: Mama Cat (adult cat)
- **02.jpeg**: Kitten (baby cat)

These are NOT AI-generated. They are real photos you upload once and reuse in every story.

## Why Base Cat Images?

### Consistency Across Stories
- Same cat characters appear in all videos
- Recognizable characters for your audience
- Professional, consistent branding

### Efficiency
- Upload once per project
- Reuse in multiple scenes
- No need to generate cat images each time

### Flexibility
- Use 01 for scenes with Mama Cat alone
- Use 02 for scenes with Kitten alone
- Use 01,02 for scenes with both cats together

## How the Extension Handles Base Cat Images

### 1. Upload Process

**In the Extension Popup**:
```
1. Click "Base Cat Images" file input
2. Select BOTH files: 01.jpeg AND 02.jpeg
3. Extension validates both files are present
4. Files are converted to base64 for transfer
5. Status shows: "✅ Both base cat images detected"
```

**Technical Details**:
- Files are read as base64 data URLs
- Stored in extension state
- Transferred to content script
- Converted back to File objects for upload

### 2. Automation Workflow

**Phase 1: Generate Story Ingredients (03-06)**
```
Generate 06.jpeg (if exists)
  ↓
Generate 05.jpeg (if exists)
  ↓
Generate 04.jpeg (if exists)
  ↓
Generate 03.jpeg (if exists)
```

**Phase 2: Upload Base Cat Images (01-02)**
```
Upload 02.jpeg (Kitten)
  ├─ Click + button
  ├─ Convert base64 to File object
  ├─ Attach to file input
  ├─ Wait for upload (up to 100s)
  ├─ Handle crop if needed
  └─ Click remove button
  
Upload 01.jpeg (Mama Cat)
  ├─ Click + button
  ├─ Convert base64 to File object
  ├─ Attach to file input
  ├─ Wait for upload (up to 100s)
  ├─ Handle crop if needed
  └─ Click remove button
```

**Result: Gallery Order**
```
Index 2: 01.jpeg (Mama Cat)
Index 3: 02.jpeg (Kitten)
Index 4: 03.jpeg (Story ingredient 1)
Index 5: 04.jpeg (Story ingredient 2)
Index 6: 05.jpeg (Story ingredient 3)
Index 7: 06.jpeg (Story ingredient 4)
```

### 3. Ingredient Selection

When processing prompts, the extension:

1. Reads `Ingredients_No` column from Excel (e.g., "01,02,03")
2. Maps ingredient numbers to gallery indices
3. Clicks + buttons dynamically
4. Selects from gallery using mapped indices

**Example**:
```
Prompt: "Both cats at juice stand"
Ingredients_No: "01,02,03"

Selection Process:
  ├─ Click + button → Select gallery index 2 (01.jpeg)
  ├─ Click + button → Select gallery index 3 (02.jpeg)
  └─ Click + button → Select gallery index 4 (03.jpeg)
```

## File Requirements

### Naming Convention

**MUST use these exact names**:
- `01.jpeg` or `01.jpg` - Mama Cat
- `02.jpeg` or `02.jpg` - Kitten

**Why?**
- Extension extracts number from filename
- Maps to gallery index automatically
- Ensures correct selection order

### File Format

**Supported formats**:
- JPEG (.jpeg, .jpg)
- PNG (.png)
- WebP (.webp)
- GIF (.gif)

**Recommended**:
- JPEG format for smaller file size
- 1024x1024 or larger resolution
- Square aspect ratio (1:1)
- Clear, well-lit photos

### File Size

**Limits**:
- Maximum: 10MB per file (Google Labs limit)
- Recommended: 1-3MB per file
- Compress if needed using online tools

## Preparing Your Base Cat Images

### Step 1: Take/Select Photos

**Mama Cat (01.jpeg)**:
- Clear photo of adult cat
- Good lighting
- Neutral background preferred
- Cat facing camera or slight angle
- Full body or upper body shot

**Kitten (02.jpeg)**:
- Clear photo of baby cat/kitten
- Same lighting style as Mama Cat
- Similar background style
- Kitten facing camera
- Full body or upper body shot

### Step 2: Edit Photos (Optional)

**Recommended edits**:
- Crop to square (1:1 aspect ratio)
- Remove distracting backgrounds
- Adjust brightness/contrast
- Resize to 1024x1024 pixels
- Save as JPEG with 80-90% quality

**Tools**:
- Photoshop, GIMP (desktop)
- Canva, Photopea (online)
- Phone photo editors

### Step 3: Name Files

```
Rename files to:
  your_cat_photo.jpg  →  01.jpeg
  your_kitten_photo.jpg  →  02.jpeg
```

### Step 4: Store Files

**Recommended folder structure**:
```
MamaCat_Project/
├── BASE_CAT_IMAGES/
│   ├── 01.jpeg  (Mama Cat)
│   └── 02.jpeg  (Kitten)
├── Excel_Files/
│   ├── MamaCat_Prompts.xlsx
│   └── Story_Ingredients.xlsx
└── Generated_Videos/
```

## Using Base Cat Images in Prompts

### Single Cat Scenes

**Mama Cat only**:
```
Ingredients_No: "01,03"
Prompt: "Mama Cat sets up a juice stand"
```

**Kitten only**:
```
Ingredients_No: "02,04"
Prompt: "The kitten plays with toys"
```

### Both Cats Scenes

**Both cats together**:
```
Ingredients_No: "01,02,03"
Prompt: "Both cats enjoy juice together"
```

**Both cats with multiple items**:
```
Ingredients_No: "01,02,03,05"
Prompt: "Cats share juice at the stand with glasses"
```

### Best Practices

✅ **DO**:
- Use 01 when Mama Cat is the focus
- Use 02 when Kitten is the focus
- Use 01,02 when both interact
- List base cats first (01,02,03 not 03,01,02)

❌ **DON'T**:
- Skip base cats in scenes with characters
- Use only story ingredients for character scenes
- Mix up the order randomly

## Troubleshooting

### Issue: "Missing base cat images" error

**Cause**: Files not uploaded or wrong names

**Solution**:
1. Check files are named exactly: 01.jpeg, 02.jpeg
2. Re-upload both files together
3. Look for "✅ Both base cat images detected" message

### Issue: Base cats not appearing in videos

**Cause**: Not included in Ingredients_No column

**Solution**:
1. Check Excel Ingredients_No column
2. Add "01" or "02" to the list
3. Example: Change "03,04" to "01,03,04"

### Issue: Wrong cat appears in scene

**Cause**: Incorrect ingredient number

**Solution**:
1. Verify: 01 = Mama Cat, 02 = Kitten
2. Check Ingredients_No in Excel
3. Update to correct number

### Issue: Upload fails or times out

**Cause**: File too large or network issue

**Solution**:
1. Check file size (should be < 10MB)
2. Compress images if needed
3. Check internet connection
4. Try uploading again

### Issue: Crop dialog appears

**Cause**: Image not square aspect ratio

**Solution**:
- Extension automatically handles crop
- Waits for crop button and clicks it
- If manual intervention needed, crop to square

## Advanced Tips

### Multiple Cat Characters

If you have more than 2 cats:

**Option 1: Rotate base cats**
- Use 01.jpeg for Cat A in Story 1
- Use 01.jpeg for Cat B in Story 2
- Re-upload different photos per project

**Option 2: Use story ingredients**
- Generate additional cats as story ingredients (03, 04)
- Use for supporting characters
- Less consistent but more variety

### Seasonal Variations

Create multiple sets:

```
BASE_CAT_IMAGES_SUMMER/
├── 01.jpeg  (Cat with summer background)
└── 02.jpeg  (Kitten with summer background)

BASE_CAT_IMAGES_WINTER/
├── 01.jpeg  (Cat with winter background)
└── 02.jpeg  (Kitten with winter background)
```

Upload appropriate set per season/theme.

### Quality Optimization

**For best results**:
1. Use high-resolution source photos (2000x2000+)
2. Downscale to 1024x1024 for upload
3. Use good lighting in original photos
4. Avoid busy backgrounds
5. Keep cat centered in frame

## Technical Details

### File Conversion Process

```javascript
// 1. User selects files
<input type="file" multiple accept="image/*">

// 2. Convert to base64
FileReader.readAsDataURL(file)
  ↓
"data:image/jpeg;base64,/9j/4AAQSkZJRg..."

// 3. Store in state
state.baseCatImages = [
  { name: "01.jpeg", data: "base64...", type: "image/jpeg" },
  { name: "02.jpeg", data: "base64...", type: "image/jpeg" }
]

// 4. Transfer to content script
chrome.tabs.sendMessage(tabId, { config: { baseCatImages: [...] } })

// 5. Convert back to File
atob(base64) → Uint8Array → File object

// 6. Attach to file input
DataTransfer.items.add(file)
fileInput.files = dataTransfer.files

// 7. Trigger upload
fileInput.dispatchEvent(new Event('change'))
```

### Upload Monitoring

```javascript
// Wait for upload completion
while (totalWaited < 100) {
  // Check for remove button (indicates upload complete)
  const removeButtons = document.querySelectorAll("button i[text='close']");
  
  if (removeButtons.length > 0) {
    // Upload complete!
    break;
  }
  
  await wait(5000); // Check every 5 seconds
  totalWaited += 5;
}

// Click remove button to clear slot
removeButtons[0].click();
```

### Gallery Mapping

```javascript
// Create mapping after uploads
ingredientMapping = {
  "01": 2,  // Gallery index 2
  "02": 3,  // Gallery index 3
  "03": 4,  // Gallery index 4
  "04": 5,  // Gallery index 5
  // ...
}

// Use for selection
const ingredientNum = "01";
const galleryIndex = ingredientMapping[ingredientNum]; // 2
const button = document.querySelector(`div[data-index="${galleryIndex}"] button`);
button.click();
```

## Summary

### Key Points

✅ Base cat images are pre-existing photos (not AI-generated)  
✅ Named 01.jpeg (Mama Cat) and 02.jpeg (Kitten)  
✅ Uploaded once per project, reused in all scenes  
✅ Uploaded AFTER story ingredients for correct gallery order  
✅ Selected dynamically based on Ingredients_No column  
✅ Provide character consistency across all videos  

### Workflow Recap

```
1. Prepare photos → Name as 01.jpeg, 02.jpeg
2. Upload in extension → Both files together
3. Extension validates → "✅ Both detected"
4. Automation runs → Generates story ingredients first
5. Then uploads base cats → In reverse order (02, 01)
6. Creates mapping → For ingredient selection
7. Processes prompts → Selects ingredients dynamically
8. Videos generated → With consistent cat characters!
```

---

**Ready to use base cat images?** Follow the QUICK_START.md guide!
