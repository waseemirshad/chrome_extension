# 🔍 DEBUG INSTRUCTIONS

## The extension now has COMPREHENSIVE debugging at every step!

### Step 1: Reload the Extension
1. Go to `chrome://extensions/`
2. Find "MamaCat Video Generator"
3. Click the **Reload** button (circular arrow icon)

### Step 2: Run the Test Page First
1. Right-click the extension icon
2. Click "Options" (this opens the test page)
3. Navigate to Google Labs Flow in another tab: https://labs.google/fx/tools/flow
4. Go back to the test page
5. Click each test button in order:
   - **1. Test Chrome APIs** - Should show all ✅
   - **2. Test Tab Query** - Should find your Google Labs tab
   - **3. Test Content Script** - Should inject and get response
   - **4. Test Full Flow** - Should pass all 5 steps

### Step 3: If Tests Pass, Use the Main Sidebar
1. Open Google Labs Flow: https://labs.google/fx/tools/flow
2. Click the extension icon to open sidebar
3. Select your files
4. Click "Setup & Verify"
5. Select stories (e.g., type "1")
6. Click "Start Generation"

### Step 4: Watch the Logs
**Open Browser Console (F12)** and look for:

#### In Console Tab:
- `🔍 [DEBUG-CORE]` - Shows every single step
- `[SIDEBAR]` - Shows sidebar actions
- `[MAMACAT DEBUG]` - Shows content script actions

#### In Sidebar Activity Log:
- Every button click is logged
- Every element search is logged
- Every verification is logged

### What You'll See:

```
🔍 [DEBUG-CORE] CREATE NEW PROJECT
🔍 [DEBUG-CORE] [STEP 1/6] Searching for New project button
🔍 [DEBUG-CORE] Method 1: Trying class selector...
✅ [DEBUG-CORE] Found via class selector
✅ [DEBUG-CORE] VERIFIED: "New project" button (via Class selector)
🔍 [DEBUG-CORE] [STEP 2/6] Clicking button
🖱️ [DEBUG-CORE] CLICKING: "New project" button
✅ [DEBUG-CORE] CLICKED: "New project" button
🔍 [DEBUG-CORE] [STEP 3/6] Waiting 3 seconds
... and so on for every single step
```

### If Something Fails:

The logs will show EXACTLY where it failed:
```
❌ [DEBUG-CORE] NOT FOUND: "New project" button
❌ [DEBUG-CORE] CLICK FAILED: Edit button - Element is null
```

### Export Logs:

1. In the sidebar, click "Copy Log" to copy all logs
2. Or in console, right-click and "Save as..."
3. Send me the logs and I can see exactly what happened!

## Current Debug Features:

✅ Every button search logged (3 methods tried)
✅ Every button click verified
✅ Every element found/not found logged
✅ Every wait period logged
✅ Every error with full stack trace
✅ Step-by-step progress (1/6, 2/6, etc.)
✅ Method used to find elements logged
✅ All button text content logged
✅ All HTML snippets logged

## The debug version only does project creation for now
Once we verify that works, we'll add the rest of the steps!
