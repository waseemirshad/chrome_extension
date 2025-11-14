# 📖 Complete Example Workflow

## Story: "Juice Stand Adventure"

This example shows a complete MamaCat story from Excel files to generated videos.

## Excel Files Setup

### 1. Prompts Excel (`MamaCat_Prompts.xlsx`)

**Worksheet Name**: `Juice Stand Adventure`

| Row | Prompt | Ingredients_No |
|-----|--------|----------------|
| 1 | Mama Cat sets up a colorful juice stand in the sunny garden | 01,03 |
| 2 | The kitten discovers the juice stand and gets excited | 02,03 |
| 3 | Mama Cat squeezes fresh oranges to make juice | 01,03,04 |
| 4 | The kitten helps by arranging the juice glasses | 02,03,05 |
| 5 | Both cats enjoy fresh juice together at the stand | 01,02,03,05 |
| 6 | Mama Cat teaches the kitten how to serve customers | 01,02,03 |
| 7 | The kitten proudly serves juice to imaginary customers | 02,03,05 |
| 8 | Mama Cat and kitten take a break on the picnic blanket | 01,02,06 |
| 9 | They watch the sunset while sipping juice | 01,02,05,06 |
| 10 | Both cats clean up the juice stand together | 01,02,03 |

### 2. Ingredients Excel (`Story_Ingredients.xlsx`)

**Worksheet Name**: `Juice Stand Adventure`

| Ingredient_No | Title | Prompt |
|---------------|-------|--------|
| 03 | Juice Stand | A colorful wooden juice stand with a striped awning, decorated with fruit illustrations, standing in a sunny garden |
| 04 | Fresh Oranges | A basket full of bright orange citrus fruits, some cut in half showing juicy segments |
| 05 | Juice Glasses | Tall clear glasses filled with golden orange juice, with colorful straws and fruit garnishes |
| 06 | Picnic Blanket | A red and white checkered picnic blanket spread on green grass with dappled sunlight |

### 3. Base Cat Images (Pre-existing)

**Folder**: `BASE_CAT_IMAGES/`

- `01.jpeg` - Photo of adult orange tabby cat (Mama Cat)
- `02.jpeg` - Photo of small orange kitten

## Automation Workflow

### Phase 1: Ingredient Processing

**Step 1: Generate Story Ingredients (Reverse Order)**
```
Generating 06.jpeg (Picnic Blanket)
  ├─ Enter prompt: "A red and white checkered picnic blanket..."
  ├─ Wait for generation (up to 100s)
  ├─ Click "Save as New Ingredient"
  ├─ Wait for save complete
  └─ Click remove button

Generating 05.jpeg (Juice Glasses)
  ├─ Enter prompt: "Tall clear glasses filled with..."
  ├─ Wait for generation
  ├─ Save as ingredient
  └─ Remove

Generating 04.jpeg (Fresh Oranges)
  ├─ Enter prompt: "A basket full of bright orange..."
  ├─ Wait for generation
  ├─ Save as ingredient
  └─ Remove

Generating 03.jpeg (Juice Stand)
  ├─ Enter prompt: "A colorful wooden juice stand..."
  ├─ Wait for generation
  ├─ Save as ingredient
  └─ Remove
```

**Step 2: Upload Base Cat Images (Reverse Order)**
```
Uploading 02.jpeg (Kitten)
  ├─ Click + button
  ├─ Upload file
  ├─ Wait for upload complete
  └─ Click remove button

Uploading 01.jpeg (Mama Cat)
  ├─ Click + button
  ├─ Upload file
  ├─ Wait for upload complete
  └─ Click remove button
```

**Result**: Gallery now contains (in order):
```
Index 2: 01.jpeg (Mama Cat)
Index 3: 02.jpeg (Kitten)
Index 4: 03.jpeg (Juice Stand)
Index 5: 04.jpeg (Fresh Oranges)
Index 6: 05.jpeg (Juice Glasses)
Index 7: 06.jpeg (Picnic Blanket)
```

### Phase 2: Video Generation (Reverse Order)

**Prompt 10 → Prompt 1**

```
Processing Prompt 10 (first in reverse order):
  ├─ Select ingredients: 01, 02, 03
  │   ├─ Click + button → Select 01 from gallery
  │   ├─ Click + button → Select 02 from gallery
  │   └─ Click + button → Select 03 from gallery
  ├─ Enter prompt: "Both cats clean up the juice stand together"
  ├─ Click generate
  └─ Wait for 50% completion

Processing Prompt 9:
  ├─ Select ingredients: 01, 02, 05, 06
  ├─ Enter prompt: "They watch the sunset while sipping juice"
  ├─ Click generate
  └─ Wait for 50% completion

... (continues for all prompts)

Processing Prompt 1 (last in reverse order):
  ├─ Select ingredients: 01, 03
  ├─ Enter prompt: "Mama Cat sets up a colorful juice stand..."
  ├─ Click generate
  └─ Complete!
```

## Expected Output

### Statistics
- **Total Prompts**: 10
- **Total Ingredients**: 6 (2 base + 4 story)
- **Expected Videos**: 20 (2 per prompt)
- **Processing Time**: ~45-60 minutes
- **Max Concurrent**: 8 videos

### Generated Videos

Each prompt generates 2 video variations:

**Prompt 1**: "Mama Cat sets up a colorful juice stand..."
- Video 1A: Mama Cat arranging items on stand
- Video 1B: Mama Cat opening the stand

**Prompt 2**: "The kitten discovers the juice stand..."
- Video 2A: Kitten approaching curiously
- Video 2B: Kitten jumping excitedly

... (20 videos total)

### Activity Log Sample

```
[14:30:15] [INFO] ═══════════════════════════════════════
[14:30:15] [INFO] 🎬 STARTING VIDEO GENERATION
[14:30:15] [INFO] 📁 Project: Juice Stand Adventure
[14:30:15] [INFO] ⚙️ Max Concurrent: 8
[14:30:15] [INFO] ═══════════════════════════════════════
[14:30:20] [INFO] 🔄 PHASE 1: Generating story ingredients
[14:30:25] [INFO] [GENERATE 06] Entering prompt...
[14:30:28] [SUCCESS] [GENERATE 06] Generation started
[14:32:15] [SUCCESS] [GENERATE 06] Complete after 107s
[14:32:20] [INFO] [GENERATE 05] Entering prompt...
... (continues)
[14:45:30] [SUCCESS] 🎉 All ingredients ready!
[14:45:35] [INFO] 🚀 PHASE 2: Processing prompts
[14:45:40] [INFO] [PROMPT 10] Selecting ingredients: 01,02,03
[14:45:45] [SUCCESS] [SELECT] Ingredient 01 selected
[14:45:48] [SUCCESS] [SELECT] Ingredient 02 selected
[14:45:51] [SUCCESS] [SELECT] Ingredient 03 selected
[14:45:55] [SUCCESS] [PROMPT 10] Submitted
... (continues)
[15:30:00] [SUCCESS] 🎉 All videos generated successfully!
```

### Final Report

```
╔═══════════════════════════════════════════════════════════╗
║         MAMACAT VIDEO GENERATION REPORT                   ║
╚═══════════════════════════════════════════════════════════╝

📅 Date: 2024-01-15 15:30:00
📁 Project: Juice Stand Adventure

📊 STATISTICS
─────────────────────────────────────────────────────────
Prompts Processed: 10/10
Ingredients Used: 6/6
Videos Generated: 20
Processing Time: 59 minutes 45 seconds
Average per Prompt: 5 minutes 58 seconds

🎯 PERFORMANCE
─────────────────────────────────────────────────────────
Success Rate: 100%
Prompts per Hour: 10.04
Videos per Hour: 20.08
Queue Efficiency: 95%

📋 INGREDIENT BREAKDOWN
─────────────────────────────────────────────────────────
01 (Mama Cat): Used in 8 prompts
02 (Kitten): Used in 8 prompts
03 (Juice Stand): Used in 7 prompts
04 (Fresh Oranges): Used in 1 prompt
05 (Juice Glasses): Used in 3 prompts
06 (Picnic Blanket): Used in 2 prompts

✅ COMPLETION STATUS
─────────────────────────────────────────────────────────
All prompts processed successfully
All ingredients generated successfully
All videos queued for generation
No errors encountered

╚═══════════════════════════════════════════════════════════╝
```

## Tips for This Story

### Ingredient Selection Strategy

**Scenes with Mama Cat alone**: Use `01,03` or `01,03,04`
**Scenes with Kitten alone**: Use `02,03` or `02,03,05`
**Scenes with both cats**: Use `01,02,03` or `01,02,03,05`
**Rest/break scenes**: Use `01,02,06` (picnic blanket)

### Prompt Writing Tips

✅ **Good Prompts**:
- "Mama Cat squeezes fresh oranges to make juice"
- "The kitten helps by arranging the juice glasses"
- "Both cats enjoy fresh juice together at the stand"

❌ **Avoid**:
- Too vague: "Cat does something"
- Too complex: "Cat makes juice while teaching kitten about business"
- Too long: Prompts over 200 characters

### Common Issues & Solutions

**Issue**: Ingredient 03 not selecting
**Solution**: Check gallery mapping, may need to adjust index

**Issue**: Videos not generating
**Solution**: Verify Google Labs quota, try reducing concurrent

**Issue**: Prompt text too long
**Solution**: Split into multiple shorter prompts

## Scaling Up

Once this example works, you can:

1. **Add More Scenes**: Expand to 25 prompts per story
2. **Create More Stories**: Add new worksheets to Excel files
3. **Batch Process**: Run multiple stories sequentially
4. **Optimize Settings**: Increase Max Concurrent to 8

## Success Checklist

✅ All 6 ingredients generated successfully  
✅ All 10 prompts processed  
✅ 20 videos queued for generation  
✅ No errors in activity log  
✅ Report exported successfully  
✅ Ready for next story!  

---

**Next**: Try creating your own story following this template!
