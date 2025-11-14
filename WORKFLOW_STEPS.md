# 🎯 Google Labs Flow - Exact Workflow Steps

## What We Need to Know

To make the automation work, I need to understand the exact steps you take manually on Google Labs. Please help me understand:

---

## Step 1: Creating a New Project

**Question:** When you're on https://labs.google/fx/tools/flow, what do you click to create a new project?

- [ ] A "New Project" button?
- [ ] A "Create" button?
- [ ] A "+" button?
- [ ] Something else?

**Please describe:**
- What button do you click?
- What text is on the button?
- What happens after you click it?

---

## Step 2: Naming the Project

**Question:** After creating a project, how do you set the name?

- [ ] A text input appears?
- [ ] A dialog/modal opens?
- [ ] You click on "Untitled" to rename?
- [ ] Something else?

**Please describe:**
- Where do you type the project name?
- Do you need to click "Save" or "OK"?
- Or does it auto-save?

---

## Step 3: Switching to Ingredients Mode

**Question:** How do you switch from regular mode to "Ingredients" mode?

- [ ] Click a tab at the top?
- [ ] Click a dropdown menu?
- [ ] Click a toggle/switch?
- [ ] It's automatic?
- [ ] Something else?

**Please describe:**
- What do you click?
- What text/icon is on it?
- How do you know you're in Ingredients mode?

---

## Step 4: Opening Generate Image Dialog

**Question:** To generate an ingredient image, what do you click?

- [ ] A "Generate Image" button?
- [ ] A "+" button?
- [ ] A "Create" button?
- [ ] Something else?

**Please describe:**
- What button opens the image generation?
- Where is it located on the page?
- What happens when you click it?

---

## Step 5: Entering Prompt for Ingredient

**Question:** Where do you type the prompt for generating an ingredient?

- [ ] In a textarea that's always visible?
- [ ] In a dialog/modal that opens?
- [ ] In a sidebar panel?
- [ ] Something else?

**Please describe:**
- Is there a placeholder text in the textarea?
- What does it say? (e.g., "Describe your image...")
- Are there any labels near it?

---

## Step 6: Generating the Ingredient

**Question:** After typing the prompt, what do you click to generate?

- [ ] A "Generate" button?
- [ ] An arrow button (→)?
- [ ] A "Create" button?
- [ ] Something else?

**Please describe:**
- What button do you click?
- What icon/text is on it?
- Where is it located?

---

## Step 7: Saving as Ingredient

**Question:** After the image generates, how do you save it as an ingredient?

- [ ] Click "Save as New Ingredient" button?
- [ ] Click "Add to Library" button?
- [ ] Click a "+" button on the image?
- [ ] Something else?

**Please describe:**
- What button do you click?
- What text is on it exactly?
- Where is it located?

---

## Step 8: Uploading Base Cat Images

**Question:** How do you upload the base cat photos (01.jpeg, 02.jpeg)?

- [ ] Click a "+" button in the ingredients panel?
- [ ] Click "Upload" button?
- [ ] Drag and drop?
- [ ] Something else?

**Please describe:**
- What do you click to start upload?
- Does a file picker open?
- Do you need to crop the image?

---

## Step 9: Selecting Ingredients for Prompt

**Question:** When creating a video, how do you select which ingredients to use?

- [ ] Click "+" buttons below the prompt?
- [ ] Click on ingredient thumbnails?
- [ ] Drag ingredients to the prompt?
- [ ] Something else?

**Please describe:**
- How many "+" buttons appear?
- Do they appear one at a time or all at once?
- What happens when you click a "+" button?

---

## Step 10: Selecting from Gallery

**Question:** After clicking "+", how do you select an ingredient from the gallery?

- [ ] Click on the ingredient thumbnail?
- [ ] Click a button on the ingredient?
- [ ] Double-click the ingredient?
- [ ] Something else?

**Please describe:**
- Does a gallery/modal open?
- How are ingredients displayed?
- What do you click to select one?

---

## Alternative: Share HTML

If it's easier, you can:

1. Open Google Labs Flow
2. Press F12 to open DevTools
3. Go to Console tab
4. Copy and paste the content of `page-inspector.js`
5. Press Enter
6. Copy all the output
7. Share it with me

Or:

1. Right-click on the page
2. Select "Inspect" or "Inspect Element"
3. Find the Elements tab
4. Take screenshots of:
   - The main page structure
   - The textarea where you type prompts
   - The buttons you click
   - The ingredients panel

---

## What I Need Most

The most critical things I need to know:

1. **Textarea selector** - How to find where to type prompts
2. **Generate button selector** - How to find the button to click
3. **Plus button selector** - How to find buttons to add ingredients
4. **Save ingredient button** - How to find the save button

With this information, I can update the automation to work perfectly!

---

## Current Assumptions (Please Verify)

Based on the Python script, I'm assuming:

- Textarea has id: `PINHOLE_TEXT_AREA_ELEMENT_ID` ❓
- Plus buttons have class: `hopAJY` ❓
- Generate button has icon with text: `arrow_forward` ❓
- Save button has text: `Save as New Ingredient` ❓

**Are these correct?** If not, what are the actual selectors?
