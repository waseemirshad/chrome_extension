# 🎬 MamaCat Video Generator - Chrome Extension

## Project Overview

A Chrome extension that automates Google Veo video generation using a hybrid ingredient system. Replicates the functionality of the Python `c1_video_generator.py` script directly in the browser.

## Key Features

### ✅ Core Functionality
- **Excel Integration**: Upload prompts and ingredients from Excel files
- **Hybrid Ingredient System**: Generate AI images + upload base photos
- **Reverse Order Processing**: Process prompts 25→1 for optimal queue management
- **Smart Waiting**: Wait for 50% completion before next prompt
- **Real-time Progress**: Live tracking of prompts, ingredients, and videos
- **Activity Logging**: Detailed logs of all operations
- **Report Export**: Generate comprehensive reports

### ✅ Automation Features
- Automatic ingredient generation (03-06)
- Automatic base image upload (01-02)
- Dynamic ingredient selection
- Queue management (max 8 concurrent)
- Error handling and recovery
- Progress persistence

## File Structure

```
chrome_extension/
├── manifest.json              # Extension configuration (Manifest V3)
├── popup.html                 # Main UI interface
├── popup.css                  # Styling for popup
├── popup.js                   # Popup logic and state management
├── content.js                 # Content script (page interaction)
├── injected.js                # Injected script (page context access)
├── automation-core.js         # Core automation logic
├── background.js              # Background service worker
├── libs/
│   └── xlsx.full.min.js      # Excel parsing library (SheetJS)
├── icons/
│   ├── icon16.png            # 16x16 icon
│   ├── icon48.png            # 48x48 icon
│   └── icon128.png           # 128x128 icon
├── README.md                  # Main documentation
├── SETUP_GUIDE.md            # Detailed setup instructions
├── QUICK_START.md            # 5-minute quick start
├── EXAMPLE_WORKFLOW.md       # Complete example story
└── PROJECT_SUMMARY.md        # This file
```

## Technology Stack

- **Chrome Extension API**: Manifest V3
- **SheetJS (xlsx)**: Excel file parsing
- **Vanilla JavaScript**: No frameworks, pure JS
- **CSS Grid & Flexbox**: Responsive layout
- **Chrome Storage API**: State persistence
- **Chrome Messaging API**: Component communication

## Architecture

### Component Communication Flow

```
┌─────────────┐
│   Popup     │ ← User Interface
│  (popup.js) │
└──────┬──────┘
       │
       ↓ chrome.runtime.sendMessage
┌─────────────┐
│ Background  │ ← Message Router
│(background.js)
└──────┬──────┘
       │
       ↓ chrome.tabs.sendMessage
┌─────────────┐
│  Content    │ ← Page Interaction
│ (content.js)│
└──────┬──────┘
       │
       ↓ window.postMessage
┌─────────────┐
│  Injected   │ ← Page Context Access
│(injected.js)│
└──────┬──────┘
       │
       ↓ Direct DOM manipulation
┌─────────────┐
│ Google Labs │ ← Target Website
│    Page     │
└─────────────┘
```

### Data Flow

```
Excel Files
    ↓
SheetJS Parser
    ↓
State Management (popup.js)
    ↓
Configuration Object
    ↓
Content Script (content.js)
    ↓
Automation Core (automation-core.js)
    ↓
DOM Manipulation
    ↓
Google Labs API
    ↓
Video Generation
```

## Workflow Comparison

### Python Script vs Chrome Extension

| Feature | Python Script | Chrome Extension |
|---------|--------------|------------------|
| **Platform** | Desktop (Windows) | Browser (Cross-platform) |
| **Browser** | Selenium + Edge | Native Chrome |
| **Session** | Edge profile folder | Chrome extension storage |
| **Excel** | pandas + openpyxl | SheetJS (xlsx) |
| **UI** | Terminal output | Popup interface |
| **Logs** | Text file | In-browser + export |
| **Installation** | Python + dependencies | Load unpacked |
| **Updates** | Manual script edit | Reload extension |

### Advantages of Extension

✅ **No Python installation required**  
✅ **Cross-platform (Windows, Mac, Linux)**  
✅ **Better UI with real-time updates**  
✅ **Easier to distribute and update**  
✅ **Native browser integration**  
✅ **Lower resource usage**  
✅ **Faster startup time**  

## Excel File Format

### Prompts Excel

**Required Columns**:
- `Prompt`: Video generation prompt text
- `Ingredients_No`: Comma-separated ingredient numbers

**Example**:
```
Worksheet: "Story Name"
Row 1: "A cat making juice" | "01,03"
Row 2: "A kitten playing" | "02,04"
```

### Ingredients Excel

**Required Columns**:
- `Ingredient_No`: Ingredient number (03-06)
- `Title`: Short description
- `Prompt`: AI generation prompt

**Example**:
```
Worksheet: "Story Name"
Row 1: "03" | "Juice Stand" | "A colorful juice stand..."
Row 2: "04" | "Garden" | "A sunny garden with flowers..."
```

## Ingredient System

### Base Ingredients (Pre-existing Photos)
- **01**: Mama Cat (adult cat)
- **02**: Kitten (baby cat)

### Story Ingredients (AI Generated)
- **03-06**: Story-specific items (max 4)

### Selection Rules
- Use `01` for Mama Cat alone
- Use `02` for Kitten alone
- Use `01,02` for both cats
- Maximum 6 ingredients per scene

### Gallery Mapping
```
Upload Order (Reverse):  06 → 05 → 04 → 03 → 02 → 01
Gallery Order (Correct): 01 → 02 → 03 → 04 → 05 → 06
Gallery Index:           2     3     4     5     6     7
```

## Automation Strategy

### Phase 1: Ingredient Processing

1. **Generate Story Ingredients** (Reverse: 06→03)
   - Enter prompt
   - Wait for generation (up to 100s)
   - Click "Save as New Ingredient"
   - Wait for save complete
   - Click remove button

2. **Upload Base Cats** (Reverse: 02→01)
   - Click + button
   - Upload file
   - Wait for upload (up to 100s)
   - Click remove button

### Phase 2: Video Generation

1. **Process Prompts** (Reverse: 25→1)
   - Select ingredients dynamically
   - Enter prompt text
   - Click generate
   - Wait for 50% completion
   - Move to next prompt

### Queue Management

- **Max Concurrent**: 8 (even numbers only)
- **Strategy**: Reverse order for better queue position
- **Wait Logic**: 50% completion before next submission
- **Error Handling**: Continue on failure, log errors

## Performance Metrics

### Expected Performance
- **Prompts per Hour**: 10-12
- **Videos per Hour**: 20-24 (2 per prompt)
- **Ingredient Generation**: 5-10 minutes each
- **Total Time (25 prompts)**: 2-3 hours

### Optimization Tips
- Use Max Concurrent: 8 for speed
- Enable reverse order processing
- Enable 50% wait strategy
- Keep browser window active
- Close unnecessary tabs

## Installation Requirements

### Minimum Requirements
- Chrome 120+ (or Chromium-based browser)
- 4GB RAM
- Stable internet connection
- Google account with Labs access

### File Requirements
- `xlsx.full.min.js` (SheetJS library)
- Icon files (16x16, 48x48, 128x128)
- Excel files with correct format

## Security & Privacy

### Permissions Used
- `activeTab`: Access current tab
- `storage`: Save configuration
- `scripting`: Inject scripts

### Host Permissions
- `https://labs.google/*`: Only Google Labs

### Data Handling
- Excel data processed locally
- No data sent to external servers
- Configuration saved in Chrome storage
- Logs kept in memory only

## Limitations

### Current Limitations
- File upload requires manual intervention (Chrome security)
- Limited to Google Labs interface
- Depends on Google Labs availability
- Subject to Google's rate limits

### Known Issues
- File upload automation restricted by browser security
- May need updates if Google Labs UI changes
- Large Excel files may slow down parsing
- Browser must stay active during generation

## Future Enhancements

### Planned Features
- [ ] Automatic file upload handling
- [ ] Multiple project support
- [ ] Template library
- [ ] Batch processing
- [ ] Cloud sync
- [ ] Mobile support

### Possible Improvements
- [ ] Video download automation
- [ ] Progress notifications
- [ ] Scheduling support
- [ ] Team collaboration
- [ ] Analytics dashboard
- [ ] API integration

## Troubleshooting

### Common Issues

**Extension won't load**
- Check `xlsx.full.min.js` is present
- Verify manifest.json is valid
- Check icon files exist

**Excel files won't upload**
- Ensure .xlsx format
- Check column names match
- Verify worksheet names

**Automation stops**
- Check Google Labs is active
- Verify not hitting rate limits
- Review activity log for errors

**Ingredients not selecting**
- Verify gallery mapping
- Check ingredient numbers
- Test manual selection first

## Documentation

### Available Guides
1. **README.md**: Main documentation
2. **SETUP_GUIDE.md**: Detailed installation
3. **QUICK_START.md**: 5-minute guide
4. **EXAMPLE_WORKFLOW.md**: Complete example
5. **PROJECT_SUMMARY.md**: This overview

### Getting Started
1. Read QUICK_START.md for fastest setup
2. Follow SETUP_GUIDE.md for detailed instructions
3. Review EXAMPLE_WORKFLOW.md for complete example
4. Refer to README.md for reference

## Support

### Resources
- Browser console (F12) for technical errors
- Activity log in extension for operation details
- Export report for debugging
- Documentation files for guidance

### Debugging
1. Check activity log first
2. Review browser console
3. Export report for analysis
4. Test with small dataset

## Version History

### v1.0.0 (Current)
- Initial release
- Excel integration
- Hybrid ingredient system
- Reverse order processing
- Real-time progress tracking
- Activity logging
- Report export

## License

MIT License - Free to use and modify

## Credits

- **Original Python Script**: c1_video_generator.py
- **Excel Library**: SheetJS (xlsx)
- **Target Platform**: Google Labs Flow
- **Automation Strategy**: Hybrid ingredient system

---

**Status**: Production Ready  
**Version**: 1.0.0  
**Last Updated**: 2024  
**Compatibility**: Chrome 120+, Google Labs Flow
