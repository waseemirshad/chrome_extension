# 🎬 MamaCat Sidebar - Complete Usage Guide

## Overview

The MamaCat extension now uses a **sidebar interface** that stays open while you work, providing a streamlined workflow for generating videos.

---

## Step-by-Step Guide

### Step 1: Open the Sidebar

1. Navigate to: https://labs.google/fx/tools/flow
2. Click the **MamaCat extension icon** in Chrome toolbar
3. Sidebar opens on the right side of your browser
4. You should see: "✅ Connected to Google Labs"

---

### Step 2: Upload Files

Upload all required files in the sidebar:

#### 📝 Prompts Excel
- Click the "Prompts Excel" upload area
- Select your `MamaCat_Prompts.xlsx` file
- Wait for: "✅ Prompts file loaded"

#### 🎨 Ingredients Excel
- Click the "Ingredients Excel" upload area
- Select your `Story_Ingredients.xlsx` file
- Wait for: "✅ Ingredients file loaded"

#### 🐱 Base Cat 01 (Mama Cat)
- Click the "Base Cat 01" upload area
- Select your `01.jpeg` or `01.jpg` file
- Wait for: "✅ Base Cat 01 loaded"

#### 🐈 Base Cat 02 (Kitten)
- Click the "Base Cat 02" upload area
- Select your `02.jpeg` or `02.jpg` file
- Wait for: "✅ Base Cat 02 loaded"

**✅ When all 4 files are uploaded, the "Setup & Verify" button becomes active**

---

### Step 3: Setup & Verify

Click the **"🔍 Setup & Verify Files"** button

**What it does:**
- ✅ Checks that worksheet names match between Prompts and Ingredients files
- ✅ Validates each story has prompts and ingredients
- ✅ Confirms both base cat images are loaded
- ✅ Lists all available stories with prompt counts
- ✅ Prepares everything for generation

**Verification Results:**
```
✅ Found 5 matching stories
✅ Story 1: "Juice Stand Adventure" - 25 prompts, 4 ingredients
✅ Story 2: "Garden Party" - 20 prompts, 3 ingredients
✅ Story 3: "Beach Day" - 18 prompts, 4 ingredients
✅ Story 4: "Rainy Day Fun" - 22 prompts, 3 ingredients
✅ Story 5: "Birthday Surprise" - 25 prompts, 4 ingredients
✅ Both base cat images loaded
```

**If verification succeeds:**
- Stories list appears
- Configuration options appear
- "Start Generation" button appears

---

### Step 4: Select Stories

Choose which stories to process:

#### Option A: Type Selection
In the "Select Stories" input field, enter:

- **All stories**: `all`
- **Range**: `1-5` (processes stories 1 through 5)
- **Multiple ranges**: `1-3,5-7` (stories 1,2,3,5,6,7)
- **Individual**: `1,3,5` (only stories 1, 3, and 5)
- **Single**: `2` (only story 2)

#### Option B: Quick Select Buttons
- **All Stories**: Processes all available stories
- **First 5**: Processes stories 1-5
- **First 10**: Processes stories 1-10

**Examples:**
```
Input: "all"        → Processes all 5 stories
Input: "1-3"        → Processes stories 1, 2, 3
Input: "1,3,5"      → Processes stories 1, 3, 5
Input: "2"          → Processes only story 2
Input: "1-2,4-5"    → Processes stories 1, 2, 4, 5
```

---

### Step 5: Configure Settings

#### Max Concurrent Videos
Choose how many videos to generate simultaneously:
- **2**: Safest, slowest
- **4**: Recommended for testing
- **6**: Faster
- **8**: Fastest (if your account allows)

#### Process in Reverse Order
✅ **Keep checked** (recommended)
- Processes prompts 25→1 for better queue management
- Helps avoid Google Labs rate limits

#### Wait for 50% Before Next Prompt
✅ **Keep checked** (recommended)
- Waits for previous prompt to reach 50% completion
- Prevents overwhelming the system

---

### Step 6: Start Generation

Click the **"🚀 Start Generation"** button

**What happens:**

#### For Each Selected Story:

**Phase 1: Create Project**
```
1. Creates new project: "MamaCat - [Story Name]"
2. Switches to Ingredients mode
```

**Phase 2: Generate Story Ingredients (5-10 min each)**
```
Generates in reverse order:
  06.jpeg (if exists) → AI generates image
  05.jpeg (if exists) → AI generates image
  04.jpeg (if exists) → AI generates image
  03.jpeg (if exists) → AI generates image
```

**Phase 3: Upload Base Cats (2-3 min each)**
```
Uploads in reverse order:
  02.jpeg (Kitten) → Uploads photo
  01.jpeg (Mama Cat) → Uploads photo
```

**Phase 4: Process Prompts (3-5 min each)**
```
For each prompt (in reverse if enabled):
  1. Selects ingredients (e.g., 01,02,03)
  2. Enters prompt text
  3. Clicks generate
  4. Waits for 50% completion
  5. Moves to next prompt
```

---

### Step 7: Monitor Progress

#### Progress Stats
Watch real-time updates:
- **Stories**: 1/5 (current story / total stories)
- **Prompts**: 15/25 (prompts processed / total prompts)
- **Videos**: 30 (total videos queued)

#### Progress Bar
Visual indicator of overall completion

#### Current Task
Shows what's happening right now:
```
"Generating ingredient 04.jpeg..."
"Uploading base cat 01.jpeg..."
"Processing prompt 15/25..."
"Selecting ingredients: 01,02,03..."
```

#### Activity Log
Detailed real-time log with timestamps:
```
[14:30:15] 🎬 STARTING VIDEO GENERATION
[14:30:20] 📚 Processing 3 stories
[14:32:45] ✅ Ingredient 03 complete
[14:35:10] ✅ All ingredients ready!
[14:37:30] ✅ Prompt 1 submitted
```

**Log Colors:**
- 🟢 Green = Success
- 🔵 Blue = Information
- 🟡 Yellow = Warning
- 🔴 Red = Error

---

### Step 8: Stop if Needed

Click the **"⏹️ Stop"** button anytime to:
- Stop current processing
- Save progress
- Return to ready state

**Safe to stop:**
- Between prompts
- Between stories
- During ingredient generation

---

### Step 9: Export Report

After completion (or anytime during processing):

1. Click **"📄 Export Report"** button
2. Save the report file
3. Review statistics and logs

**Report includes:**
- Total stories processed
- Total prompts processed
- Total videos generated
- Processing time
- Complete activity log

---

## Sidebar Features

### Always Visible
- Sidebar stays open while you work
- No need to keep clicking extension icon
- Easy to monitor progress

### Real-Time Updates
- Live progress tracking
- Instant log updates
- Current task display

### Organized Workflow
- Clear step-by-step process
- Can't skip required steps
- Validation at each stage

### Smart Verification
- Checks file compatibility
- Validates worksheet names
- Confirms all requirements met

---

## Common Workflows

### Workflow 1: Process All Stories
```
1. Upload all 4 files
2. Click "Setup & Verify"
3. Type "all" in selection
4. Click "Start Generation"
5. Monitor progress
6. Export report when done
```

### Workflow 2: Test Single Story
```
1. Upload all 4 files
2. Click "Setup & Verify"
3. Type "1" in selection
4. Set Max Concurrent to 4
5. Click "Start Generation"
6. Watch first story complete
```

### Workflow 3: Process Specific Stories
```
1. Upload all 4 files
2. Click "Setup & Verify"
3. Type "1,3,5" in selection
4. Click "Start Generation"
5. Only stories 1, 3, and 5 process
```

### Workflow 4: Batch Processing
```
1. Upload all 4 files
2. Click "Setup & Verify"
3. Type "1-10" in selection
4. Set Max Concurrent to 8
5. Click "Start Generation"
6. Process first 10 stories
```

---

## Tips & Best Practices

### ✅ DO:
- Keep sidebar open during generation
- Monitor activity log for errors
- Start with 1-2 stories for testing
- Use Max Concurrent: 4 for first run
- Export report after each session
- Keep Google Labs tab active

### ❌ DON'T:
- Close sidebar during generation
- Navigate away from Google Labs
- Process too many stories at once initially
- Ignore error messages in log
- Skip the Setup & Verify step

---

## Troubleshooting

### Issue: Sidebar won't open

**Solution:**
1. Make sure you're on Google Labs page
2. Click extension icon again
3. Refresh the page if needed
4. Check extension is enabled in chrome://extensions/

### Issue: "Setup & Verify" button disabled

**Solution:**
- Check all 4 files are uploaded
- Look for green checkmarks on file displays
- Re-upload any missing files

### Issue: Verification fails

**Solution:**
- Check worksheet names match exactly
- Ensure both Excel files have same story names
- Verify files are .xlsx format
- Check for empty worksheets

### Issue: No stories appear after verification

**Solution:**
- Check Excel files have data
- Verify worksheet names are not empty
- Ensure Prompt column exists in prompts file
- Check Ingredient_No column exists in ingredients file

### Issue: Generation stops unexpectedly

**Solution:**
- Check activity log for errors
- Click Stop button
- Refresh Google Labs page
- Re-upload files and try again
- Try reducing Max Concurrent

### Issue: Can't select stories

**Solution:**
- Make sure Setup & Verify completed successfully
- Check stories list is visible
- Try typing "all" to select everything
- Use simple format: "1-5" or "1,2,3"

---

## Keyboard Shortcuts

While sidebar is focused:
- **Ctrl+L**: Focus on story selection input
- **Ctrl+Enter**: Start generation (if ready)
- **Esc**: Stop generation (if running)

---

## File Requirements Reminder

### Excel Files Must Have:

**Prompts Excel:**
- Worksheet name = Story name
- Column: `Prompt` (video prompt text)
- Column: `Ingredients_No` (e.g., "01,02,03")

**Ingredients Excel:**
- Worksheet name = SAME as prompts
- Column: `Ingredient_No` (e.g., "03", "04")
- Column: `Title` (short description)
- Column: `Prompt` (AI generation prompt)

### Image Files Must Be:
- **01.jpeg** or **01.jpg**: Mama Cat photo
- **02.jpeg** or **02.jpg**: Kitten photo
- Format: JPEG, PNG, or WebP
- Size: Under 10MB each
- Recommended: 1024x1024 pixels

---

## Example Session

```
[User opens Google Labs]
[User clicks MamaCat icon]
[Sidebar opens]

✅ Connected to Google Labs

[User uploads 4 files]
✅ Prompts file loaded: MamaCat_Prompts.xlsx
✅ Ingredients file loaded: Story_Ingredients.xlsx
✅ Base Cat 01 loaded: mama_cat.jpg
✅ Base Cat 02 loaded: kitten.jpg

[User clicks "Setup & Verify"]
🔍 SETUP & VERIFICATION STARTED
✅ Found 5 matching stories
✅ Story 1: "Juice Stand" - 25 prompts, 4 ingredients
✅ Story 2: "Garden Party" - 20 prompts, 3 ingredients
...
✅ Setup complete! Select stories to process

[User types "1-2" in selection]
[User clicks "Start Generation"]

🚀 STARTING VIDEO GENERATION
📚 Processing 2 stories
🔄 Story 1: Juice Stand
  🎨 Generating ingredient 04.jpeg...
  ✅ Ingredient 04 complete
  🎨 Generating ingredient 03.jpeg...
  ✅ Ingredient 03 complete
  🐱 Uploading base cat 02.jpeg...
  ✅ Base cat 02 uploaded
  🐱 Uploading base cat 01.jpeg...
  ✅ Base cat 01 uploaded
  🎬 Processing prompt 25/25...
  ✅ Prompt 25 submitted
  ...
  ✅ Story 1 complete!

🔄 Story 2: Garden Party
  ...
  ✅ Story 2 complete!

🎉 All videos generated successfully!

[User clicks "Export Report"]
📄 Report exported
```

---

## Need Help?

1. Check the activity log for detailed errors
2. Review verification results
3. Export report for debugging
4. Refer to other guides:
   - `QUICK_START.md`
   - `SETUP_GUIDE.md`
   - `BASE_CAT_IMAGES_GUIDE.md`

---

**Ready to use the sidebar?** Follow these steps and generate videos efficiently! 🎬🐱
