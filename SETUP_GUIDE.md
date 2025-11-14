# 🚀 MamaCat Video Generator - Complete Setup Guide

## Prerequisites

- Google Chrome browser (latest version)
- Google account with access to Google Labs
- Excel files with prompts and ingredients data

## Step-by-Step Installation

### 1. Download SheetJS Library

The extension needs the SheetJS library to parse Excel files.

**Option A: Download from CDN**
```bash
# Create libs folder
mkdir chrome_extension/libs

# Download xlsx library
curl -o chrome_extension/libs/xlsx.full.min.js https://cdn.sheetjs.com/xlsx-latest/package/dist/xlsx.full.min.js
```

**Option B: Manual Download**
1. Visit: https://cdn.sheetjs.com/xlsx-latest/package/dist/xlsx.full.min.js
2. Save the file as `xlsx.full.min.js`
3. Place it in `chrome_extension/libs/` folder

### 2. Create Extension Icons

Create three icon files in `chrome_extension/icons/`:

**Quick Method (Using Online Tool):**
1. Go to https://www.favicon-generator.org/
2. Upload any cat/video related image
3. Generate icons in sizes: 16x16, 48x48, 128x128
4. Save as:
   - `icon16.png`
   - `icon48.png`
   - `icon128.png`

**Manual Method:**
- Use any image editor (Photoshop, GIMP, etc.)
- Create square images in the required sizes
- Save as PNG format

### 3. Load Extension in Chrome

1. Open Chrome browser
2. Navigate to `chrome://extensions/`
3. Enable "Developer mode" (toggle switch in top-right corner)
4. Click "Load unpacked" button
5. Select the `chrome_extension` folder
6. Extension should now appear with your icon

### 4. Verify Installation

✅ Extension icon appears in Chrome toolbar  
✅ Clicking icon opens the popup interface  
✅ No errors in `chrome://extensions/` page  

## Preparing Your Excel Files

### Prompts Excel File Structure

**File Name**: `MamaCat_Prompts.xlsx`

**Worksheet Name**: Story name (e.g., "Juice Stand Adventure")

**Required Columns**:
| Column Name | Description | Example |
|-------------|-------------|---------|
| Prompt | Video generation prompt | "A cat making fresh juice at a colorful stand" |
| Ingredients_No | Comma-separated ingredient numbers | "01,03" |

**Example Data**:
```
Prompt                                          | Ingredients_No
------------------------------------------------|---------------
A cat making fresh juice at a colorful stand    | 01,03
A kitten playing with toys in the garden        | 02,04
Both cats enjoying juice together               | 01,02,03
The cat cleaning up the juice stand             | 01,03
```

### Ingredients Excel File Structure

**File Name**: `Story_Ingredients.xlsx`

**Worksheet Name**: Same as prompts (e.g., "Juice Stand Adventure")

**Required Columns**:
| Column Name | Description | Example |
|-------------|-------------|---------|
| Ingredient_No | Ingredient number (03-06) | "03" |
| Title | Short description | "Juice Stand" |
| Prompt | AI generation prompt | "A colorful juice stand with fresh fruits" |

**Example Data**:
```
Ingredient_No | Title          | Prompt
--------------|----------------|------------------------------------------
03            | Juice Stand    | A colorful juice stand with fresh fruits
04            | Garden Toys    | Colorful toys scattered in a garden
05            | Picnic Blanket | A red checkered picnic blanket
06            | Juice Glasses  | Colorful glasses filled with juice
```

### Base Ingredients (Pre-existing)

These are NOT in the Excel file - they are photos you upload manually:

- **01.jpeg**: Mama Cat (adult cat photo)
- **02.jpeg**: Kitten (baby cat photo)

Place these in a folder called `BASE_CAT_IMAGES/`

## First-Time Usage

### 1. Navigate to Google Labs

1. Open Chrome
2. Go to: https://labs.google/fx/tools/flow
3. Sign in with your Google account
4. Wait for the page to fully load

### 2. Open Extension

1. Click the MamaCat extension icon in toolbar
2. You should see: "Connected to Google Labs" in the log

### 3. Upload Excel Files

1. Click "Prompts Excel" file input
2. Select your `MamaCat_Prompts.xlsx` file
3. Wait for "Prompts file loaded" message
4. Click "Ingredients Excel" file input
5. Select your `Story_Ingredients.xlsx` file
6. Wait for "Ingredients file loaded" message

### 4. Configure Settings

**Project Name**: Enter a descriptive name (e.g., "MamaCat - Juice Stand")

**Max Concurrent**: Choose 2, 4, 6, or 8
- Start with 4 for testing
- Use 8 for maximum speed (if your account allows)

**Reverse Order**: ✅ Keep checked
- Processes prompts 25→1 for better queue management

**Wait for 50%**: ✅ Keep checked
- Waits for previous prompt to reach 50% before next

### 5. Start Generation

1. Click "🚀 Start Generation" button
2. Watch the progress section appear
3. Monitor activity log for detailed status
4. Wait for completion message

### 6. Export Report

1. Click "📄 Export Report" when done
2. Save the report file for your records
3. Review statistics and logs

## Troubleshooting

### Extension Won't Load

**Problem**: Extension shows errors in chrome://extensions/

**Solutions**:
- Check that all files are in correct locations
- Verify `xlsx.full.min.js` is in `libs/` folder
- Ensure `manifest.json` is valid JSON
- Try removing and re-adding the extension

### Excel Files Won't Upload

**Problem**: "Failed to read file" error

**Solutions**:
- Ensure file is .xlsx or .xls format
- Check that column names match exactly
- Verify worksheet names are correct
- Try opening file in Excel to check for corruption

### Not Connected to Google Labs

**Problem**: "Not on Google Labs" warning

**Solutions**:
- Navigate to https://labs.google/fx/tools/flow
- Refresh the page
- Check that you're signed in to Google
- Try reloading the extension

### Automation Stops Unexpectedly

**Problem**: Generation stops mid-process

**Solutions**:
- Check activity log for error messages
- Ensure Google Labs page is still active
- Verify you haven't hit daily generation limits
- Try reducing Max Concurrent setting

### Ingredients Not Selecting

**Problem**: Ingredients don't get selected for prompts

**Solutions**:
- Verify Ingredients_No column format (comma-separated)
- Check that ingredient numbers exist in gallery
- Ensure ingredients were uploaded successfully
- Try manual selection to test

## Advanced Configuration

### Custom Ingredient Mapping

If your ingredients are in different positions:

1. Open browser console (F12)
2. Type: `console.log(window.ingredientMapping)`
3. Adjust ingredient numbers in Excel accordingly

### Batch Processing Multiple Stories

To process multiple stories:

1. Create multiple worksheets in Excel files
2. Each worksheet = one story
3. Extension will process all worksheets sequentially

### Performance Optimization

**For Faster Generation**:
- Use Max Concurrent: 8
- Enable Reverse Order
- Enable 50% Wait
- Close unnecessary browser tabs

**For Stability**:
- Use Max Concurrent: 4
- Add delays between prompts
- Monitor system resources

## Best Practices

### Excel File Organization

✅ **DO**:
- Use clear, descriptive worksheet names
- Keep prompts concise and specific
- Test with small batches first
- Back up your Excel files

❌ **DON'T**:
- Use special characters in worksheet names
- Leave empty rows in data
- Mix different stories in one worksheet
- Exceed 6 ingredients per scene

### Ingredient Management

✅ **DO**:
- Generate story ingredients (03-06) first
- Upload base cats (01-02) last
- Use consistent naming (01.jpeg, 02.jpeg, etc.)
- Test ingredient selection manually first

❌ **DON'T**:
- Skip ingredient numbers (e.g., 03, 05 without 04)
- Use more than 4 story ingredients
- Forget to include base cats when needed

### Generation Strategy

✅ **DO**:
- Start with reverse order enabled
- Monitor first few prompts closely
- Export reports regularly
- Keep browser window active

❌ **DON'T**:
- Navigate away from Google Labs during generation
- Close browser while running
- Exceed Google's rate limits
- Run multiple instances simultaneously

## Support & Resources

### Getting Help

1. Check activity log in extension for errors
2. Review this guide for solutions
3. Check browser console (F12) for technical errors
4. Export report for debugging

### Useful Links

- Google Labs Flow: https://labs.google/fx/tools/flow
- SheetJS Documentation: https://docs.sheetjs.com/
- Chrome Extensions: https://developer.chrome.com/docs/extensions/

### Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "Element not found" | Page structure changed | Update selectors in code |
| "Upload timeout" | Ingredient took too long | Increase wait time |
| "Gallery not loaded" | Selection failed | Refresh page and retry |
| "Generate button not found" | UI not ready | Wait longer before clicking |

## Updates & Maintenance

### Checking for Updates

The extension may need updates if Google Labs changes their interface.

**Signs you need an update**:
- Buttons not clicking
- Elements not found
- Automation stops immediately
- New UI elements appear

### Manual Updates

1. Download updated extension files
2. Go to chrome://extensions/
3. Click "Remove" on old version
4. Click "Load unpacked" for new version

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Compatibility**: Chrome 120+, Google Labs Flow
