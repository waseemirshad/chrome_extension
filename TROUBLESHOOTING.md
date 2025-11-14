# 🔧 Troubleshooting Guide

## Common Issues & Solutions

### Issue: "Could not establish connection. Receiving end does not exist"

This error means the content script isn't loaded on the Google Labs page.

**Solutions:**

#### Solution 1: Refresh the Page (Recommended)
1. Refresh the Google Labs page (F5 or Ctrl+R)
2. Wait for page to fully load
3. Click the MamaCat extension icon again
4. Sidebar should open
5. Try starting generation again

#### Solution 2: Reload the Extension
1. Go to `chrome://extensions/`
2. Find "MamaCat Video Generator"
3. Click the reload icon (🔄)
4. Go back to Google Labs
5. Refresh the page
6. Open sidebar and try again

#### Solution 3: Check Extension Permissions
1. Go to `chrome://extensions/`
2. Find "MamaCat Video Generator"
3. Click "Details"
4. Scroll to "Site access"
5. Make sure it says "On specific sites" or "On all sites"
6. Add `https://labs.google/*` if needed

#### Solution 4: Reinstall Extension
1. Go to `chrome://extensions/`
2. Remove "MamaCat Video Generator"
3. Click "Load unpacked" again
4. Select the `chrome_extension` folder
5. Navigate to Google Labs
6. Open sidebar

---

### Issue: Upload panel doesn't hide after verification

**Solution:**
- This is fixed in the latest version
- After clicking "Setup & Verify", the upload panel should automatically hide
- If it doesn't, reload the extension

---

### Issue: Stories list takes too much space

**Solution:**
- This is fixed in the latest version
- Stories list now has a maximum height of 150px
- Scrollable if you have many stories
- Compact design with smaller text

---

### Issue: Verification fails

**Possible causes:**

1. **Worksheet names don't match**
   - Check that story names are identical in both Excel files
   - Case-sensitive: "Story 1" ≠ "story 1"

2. **Missing columns**
   - Prompts file needs: `Prompt`, `Ingredients_No`
   - Ingredients file needs: `Ingredient_No`, `Title`, `Prompt`

3. **Empty worksheets**
   - Make sure worksheets have data
   - At least one prompt per story

**Solution:**
- Check verification results in the sidebar
- Fix the issues mentioned
- Re-upload the corrected files
- Click "Setup & Verify" again

---

### Issue: Generation starts but nothing happens

**Possible causes:**

1. **Not on Google Labs page**
   - Make sure you're on: https://labs.google/fx/tools/flow
   - Not just labs.google homepage

2. **Page not fully loaded**
   - Wait for Google Labs to fully load
   - Look for the "Create" or "New Project" button

3. **Content script not injected**
   - See "Connection error" solutions above

**Solution:**
- Refresh Google Labs page
- Wait for full load
- Reopen sidebar
- Try again

---

### Issue: Automation stops unexpectedly

**Check the activity log for:**

1. **Rate limit errors**
   - Google Labs has rate limits
   - Reduce "Max Concurrent" to 2 or 4
   - Wait a few minutes before retrying

2. **Element not found errors**
   - Google Labs UI might have changed
   - Extension needs updating
   - Report the issue

3. **Timeout errors**
   - Network might be slow
   - Increase timeout in settings
   - Try again with fewer stories

**Solution:**
- Check activity log for specific error
- Export report for detailed debugging
- Try with single story first
- Reduce concurrent videos

---

### Issue: Can't select stories

**Possible causes:**

1. **Verification not complete**
   - Make sure "Setup & Verify" succeeded
   - Look for green checkmarks

2. **Invalid selection format**
   - Use: `all`, `1-5`, `1,3,5`, or `2`
   - No spaces: `1-5` not `1 - 5`

**Solution:**
- Complete verification first
- Use correct format
- Try "all" to select everything
- Use quick select buttons

---

### Issue: Base cat images not uploading

**Possible causes:**

1. **File too large**
   - Maximum 10MB per file
   - Compress images if needed

2. **Wrong format**
   - Use JPEG, PNG, or WebP
   - Not GIF or other formats

3. **Upload timeout**
   - Network might be slow
   - Try smaller images

**Solution:**
- Compress images to under 3MB
- Use JPEG format
- Ensure good internet connection
- Try uploading again

---

### Issue: Ingredients not generating

**Possible causes:**

1. **Missing prompt in Excel**
   - Check Ingredients Excel has `Prompt` column
   - Make sure prompts are not empty

2. **Google Labs quota exceeded**
   - You might have hit daily limit
   - Wait 24 hours
   - Try with fewer ingredients

3. **Generation timeout**
   - Some images take longer
   - Extension waits up to 100 seconds
   - Might need to retry

**Solution:**
- Check Excel file format
- Verify prompts are present
- Check Google Labs quota
- Try again later if quota exceeded

---

### Issue: Prompts not submitting

**Possible causes:**

1. **Ingredients not selected**
   - Check `Ingredients_No` column in Excel
   - Make sure format is correct: "01,02,03"

2. **Text area not found**
   - Google Labs UI might have changed
   - Extension needs updating

3. **Generate button disabled**
   - Prompt might be too long
   - Or missing required fields

**Solution:**
- Verify Excel format
- Check prompt length (under 500 chars)
- Try manual generation first
- Report if UI changed

---

## Best Practices to Avoid Issues

### ✅ DO:

1. **Always refresh Google Labs page before starting**
   - Ensures clean state
   - Content script loads properly

2. **Start with 1-2 stories for testing**
   - Verify everything works
   - Then scale up

3. **Use Max Concurrent: 4 initially**
   - Safer than 8
   - Less likely to hit rate limits

4. **Keep sidebar open during generation**
   - Monitor progress
   - See errors immediately

5. **Export report after each session**
   - Helps with debugging
   - Track what worked

### ❌ DON'T:

1. **Don't navigate away from Google Labs**
   - Breaks the automation
   - Have to restart

2. **Don't close sidebar during generation**
   - Might lose connection
   - Can't monitor progress

3. **Don't process too many stories at once**
   - Start small
   - Scale up gradually

4. **Don't ignore error messages**
   - Check activity log
   - Fix issues before continuing

5. **Don't skip verification step**
   - Catches problems early
   - Saves time later

---

## Debug Checklist

If something isn't working, check:

- [ ] On Google Labs page: https://labs.google/fx/tools/flow
- [ ] Page fully loaded (can see UI elements)
- [ ] Extension enabled in chrome://extensions/
- [ ] All 4 files uploaded successfully
- [ ] Setup & Verify completed successfully
- [ ] Stories selected (not empty)
- [ ] Sidebar still open
- [ ] Activity log shows no errors
- [ ] Internet connection stable

---

## Getting More Help

### Check Activity Log
- Most errors show in the log
- Look for red error messages
- Note the timestamp

### Export Report
- Click "Export Report" button
- Save the file
- Review for patterns

### Browser Console
- Press F12 to open DevTools
- Go to Console tab
- Look for errors (red text)
- Take screenshot if needed

### Extension Console
- Go to chrome://extensions/
- Find MamaCat extension
- Click "Inspect views: service worker"
- Check for errors

---

## Quick Fixes Summary

| Problem | Quick Fix |
|---------|-----------|
| Connection error | Refresh page + reopen sidebar |
| Upload panel visible | Fixed in latest version |
| Stories list too big | Fixed in latest version |
| Verification fails | Check Excel worksheet names |
| Nothing happens | Refresh page, wait for load |
| Stops unexpectedly | Check log, reduce concurrent |
| Can't select stories | Complete verification first |
| Images won't upload | Compress to under 3MB |
| Ingredients fail | Check Excel prompts column |
| Prompts don't submit | Verify Ingredients_No format |

---

## Still Having Issues?

1. Try the "Nuclear Option":
   - Close all Chrome windows
   - Reopen Chrome
   - Go to chrome://extensions/
   - Reload MamaCat extension
   - Navigate to Google Labs
   - Start fresh

2. Check for updates:
   - Extension might need updating
   - Google Labs UI might have changed
   - Check for new version

3. Test with minimal data:
   - 1 story
   - 3 prompts
   - 1 ingredient
   - Verify basic functionality

---

**Remember:** Most issues are solved by refreshing the Google Labs page and reopening the sidebar! 🔄
