# ⚡ Quick Start Guide - 5 Minutes to First Video

## 1. Install Extension (2 minutes)

```bash
# Download SheetJS library
curl -o chrome_extension/libs/xlsx.full.min.js https://cdn.sheetjs.com/xlsx-latest/package/dist/xlsx.full.min.js

# Create placeholder icons (or use your own)
mkdir -p chrome_extension/icons
# Add your icon files: icon16.png, icon48.png, icon128.png
```

**Load in Chrome**:
1. Go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select `chrome_extension` folder

## 2. Prepare Excel Files (1 minute)

### Prompts File: `test_prompts.xlsx`

Create a worksheet named "Test Story" with:

| Prompt | Ingredients_No |
|--------|----------------|
| A cat sitting in a sunny garden | 01 |
| A kitten playing with a ball | 02 |
| Both cats relaxing together | 01,02 |

### Ingredients File: `test_ingredients.xlsx`

Create a worksheet named "Test Story" with:

| Ingredient_No | Title | Prompt |
|---------------|-------|--------|
| 03 | Garden | A beautiful sunny garden with flowers |
| 04 | Ball | A colorful ball toy |

## 3. Run First Generation (2 minutes)

1. **Open Google Labs**: https://labs.google/fx/tools/flow
2. **Click Extension Icon** in Chrome toolbar
3. **Upload Files**:
   - Prompts: `test_prompts.xlsx`
   - Ingredients: `test_ingredients.xlsx`
4. **Configure**:
   - Project Name: "Test Run"
   - Max Concurrent: 4
   - Keep checkboxes enabled
5. **Click "Start Generation"**
6. **Watch Progress** in real-time

## Expected Results

✅ 3 prompts processed  
✅ 2 ingredients generated  
✅ 6 videos created (2 per prompt)  
✅ Report exported  

## Next Steps

- Review activity log for any issues
- Export and save the report
- Try with your full story data
- Adjust settings based on results

## Troubleshooting

**Issue**: Extension not loading  
**Fix**: Check that `xlsx.full.min.js` is in `libs/` folder

**Issue**: Files won't upload  
**Fix**: Ensure Excel files are .xlsx format with correct column names

**Issue**: Not on Google Labs  
**Fix**: Navigate to https://labs.google/fx/tools/flow first

## Tips for Success

💡 Start with 3-5 prompts for testing  
💡 Use Max Concurrent: 4 for first run  
💡 Keep browser window active during generation  
💡 Export report after each run  

---

**Ready to scale up?** See SETUP_GUIDE.md for advanced features!
