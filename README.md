# 🎬 MamaCat Video Generator - Chrome Extension

Automate Google Veo video generation with ingredients and prompts directly from your browser.

## Features

- ✅ **Hybrid Ingredient System**: Generate AI images + upload base cat photos
- ✅ **Excel Integration**: Upload prompts and ingredients from Excel files
- ✅ **Reverse Order Processing**: Process prompts 25→1 for optimal queue management
- ✅ **50% Wait Strategy**: Wait for previous prompt to reach 50% before next submission
- ✅ **Real-time Progress**: Live progress tracking and activity logs
- ✅ **Export Reports**: Generate comprehensive generation reports

## Installation

### Step 1: Download Required Library

1. Download `xlsx.full.min.js` from [SheetJS](https://cdn.sheetjs.com/xlsx-latest/package/dist/xlsx.full.min.js)
2. Save it to `chrome_extension/libs/xlsx.full.min.js`

### Step 2: Create Icons

Create icon files in `chrome_extension/icons/`:
- `icon16.png` (16x16)
- `icon48.png` (48x48)
- `icon128.png` (128x128)

### Step 3: Load Extension in Chrome

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `chrome_extension` folder
5. The extension should now appear in your extensions list

## Usage

### 1. Prepare Your Excel Files

#### Prompts Excel Format:
```
Worksheet: Story_Name
Columns:
- Prompt: Video generation prompt text
- Ingredients_No: Comma-separated ingredient numbers (e.g., "01,03,04")
```

#### Ingredients Excel Format:
```
Worksheet: Story_Name
Columns:
- Ingredient_No: Ingredient number (e.g., "03", "04", "05", "06")
- Title: Ingredient title
- Prompt: AI generation prompt for the ingredient
```

### 2. Navigate to Google Labs

1. Go to [Google Labs Flow](https://labs.google/fx/tools/flow)
2. Make sure you're logged in to your Google account

### 3. Start Generation

1. Click the extension icon in Chrome toolbar
2. Upload your Prompts Excel file
3. Upload your Ingredients Excel file
4. Configure settings:
   - Project Name
   - Max Concurrent (2, 4, 6, or 8)
   - Enable/disable reverse order
   - Enable/disable 50% wait strategy
5. Click "Start Generation"

### 4. Monitor Progress

- Watch real-time progress in the extension popup
- View activity logs for detailed information
- Export report when complete

## Excel File Examples

### Prompts Excel (MamaCat_Prompts.xlsx)

| Prompt | Ingredients_No |
|--------|----------------|
| A cat making juice at a colorful stand | 01,03 |
| A kitten playing with toys in the garden | 02,04 |
| Both cats enjoying juice together | 01,02,03 |

### Ingredients Excel (Story_Ingredients.xlsx)

| Ingredient_No | Title | Prompt |
|---------------|-------|--------|
| 03 | Juice Stand | A colorful juice stand with fruits |
| 04 | Garden Toys | Colorful toys scattered in a garden |
| 05 | Picnic Blanket | A red checkered picnic blanket |

## Ingredient System

### Base Ingredients (Pre-existing Photos)
- **01**: Mama Cat (adult cat photo)
- **02**: Kitten (baby cat photo)

### Story Ingredients (AI Generated)
- **03-06**: Story-specific items (max 4 per story)

### Usage Rules
- Use `01` for scenes with Mama Cat alone
- Use `02` for scenes with Kitten alone
- Use `01,02` for scenes with both cats
- Maximum 6 ingredients per scene (2 base + 4 story)

## Workflow

1. **Ingredient Generation Phase**:
   - Generates story ingredients (03-06) in reverse order
   - Uploads base cat photos (01-02) in reverse order
   - Creates ingredient mapping for selection

2. **Video Generation Phase**:
   - Processes prompts in reverse order (25→1)
   - Selects ingredients for each prompt
   - Waits for 50% completion before next prompt
   - Manages queue with even numbers (max 8 concurrent)

## Troubleshooting

### Extension Not Working
- Make sure you're on `labs.google/fx/tools/flow`
- Check browser console for errors (F12)
- Reload the extension from `chrome://extensions/`

### Excel Files Not Loading
- Ensure `xlsx.full.min.js` is in the `libs` folder
- Check file format (.xlsx or .xls)
- Verify column names match exactly

### Automation Stops
- Check if Google Labs page is still active
- Look for error messages in activity log
- Try restarting the extension

## Development

### File Structure
```
chrome_extension/
├── manifest.json          # Extension configuration
├── popup.html            # Extension popup UI
├── popup.css             # Popup styling
├── popup.js              # Popup logic
├── content.js            # Content script (page interaction)
├── injected.js           # Injected script (page context)
├── background.js         # Background service worker
├── libs/
│   └── xlsx.full.min.js  # Excel parsing library
└── icons/
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
```

### Key Technologies
- Chrome Extension Manifest V3
- SheetJS (xlsx) for Excel parsing
- Vanilla JavaScript (no frameworks)
- CSS Grid & Flexbox for layout

## License

MIT License - Feel free to modify and distribute

## Support

For issues or questions, please check the activity log in the extension for detailed error messages.

---

**Version**: 1.0.0  
**Author**: MamaCat Team  
**Last Updated**: 2024
