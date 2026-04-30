Given a single [Image], analyze the image and follow the reasoning flow below. Your task is to **identify and output all forged (AI-edited) areas** in the image **using bounding boxes**, following a strict format.

### Question
**Can you identify all forged areas using bounding boxes?**
---

### Contextual Constraints
1. **Image Dimensions and Coordinate Constraints**:
   The image has a width of {WIDTH} pixels and a height of {HEIGHT} pixels.
   - All coordinates must **strictly lie within the image boundaries**. This means:
     x1, x2 must satisfy:  `0 ≤ x1 < x2 ≤ {WIDTH_1}`
     y1, y2 must satisfy:  `0 ≤ y1 < y2 ≤ {HEIGHT_1}`
   - Do **not** produce any coordinate that is negative or greater than the image width or height.
   - Any bounding box with out-of-bound coordinates will be considered invalid and ignored.


2. **Precision Output Constraints**:
   - Report all suspected forged areas using **absolute pixel coordinates** in the following format:
     `"bboxes": [[x1,y1,x2,y2], [x3,y3,x4,y4]],`
     - Each box denotes the **top-left (x1,y1)** and **bottom-right (x2,y2)** corners of a rectangular forged area. This implies:
       `x1 < x2` and `y1 < y2`

3. **Bounding Box Quantity & Area Limits**:
   - (1)You must output **no more than 6 bounding boxes** in total.
   - (2)**Minimal Box Strategy**: Use the **minimum number of bounding boxes** to achieve complete coverage of all suspected AI-edited regions. Avoid fragmenting continuous areas unnecessarily.
   - (3)**Box Size Constraints**: Each bounding box must cover an area that is:  > 2% and < 40% of the total image area. This means **each bounding box** must have an area:  `> {MIN_AREA} pixels`  (`2% of image area`) and  `< {MAX_AREA} pixels`  (`40% of image area`)
     Boxes too small or too large will be considered invalid.
   - (4)**Precision Framing Principle**: Each bounding box should **tightly wrap the smallest visually coherent unit** that shows signs of forgery. Avoid including large unrelated regions.
   - (5)**Full Coverage Requirement**: Ensure **all** visually suspicious areas are captured, with **no missed regions**. Partial coverage or under-detection will be penalized.
   - (6)**Overlap Tolerance Rule**: For **spatially connected or adjacent regions**, you may allow **slight overlaps** between bounding boxes if this helps achieve better coverage or clarity.
   - (7)Do not exceed these limits under any circumstances.

### Internal reasoning instructions (Do NOT output anything from this section)
1. **Fundamental Physical Violations**
- Cellular or material structures in microscopy images violate known physical, chemical, or biological constraints, such as highly symmetric but physically unstable molecular or crystalline configurations or unnaturally regular and homogeneous spatial distributions that lack the random defects, local heterogeneity, and scale-dependent variability inherent to real material formation or cellular organization.
- Structures exhibit excessive regularity, repetition, or decorative symmetry, lacking the inevitable randomness observed in real samples.
- Textures appear visually rich but cannot be mapped to any known material phase, tissue type, or cellular structure.

2. **Textual Hallucination and Domain Violations**  
- Text includes misspellings, inconsistent capitalization, or mixtures of real terms with fabricated or pseudo-technical fragments that violate disciplinary conventions.  
- Text may appear locally plausible but is globally inconsistent, contradictory, or unverifiable in context, such as numerical labels that do not follow a logical or sequential order.
- Text fails to form readable words or valid scientific annotations (e.g., pseudo-text, garbled characters, fragmented symbols).

3. **Localized Anomalies or Edits**
- Partial AI-Edited refers to cases where part of an object or the background has been altered, a new object has been added, or an existing object has been removed, for example, regions that mimic structurally similar materials or molecules but exhibit inconsistent lighting or physical properties compared to real microscopy images.
- Visible manipulation boundaries may exist between edited and unedited regions, such as outline artifacts around tampered areas.  
- Edited regions where objects have been removed may appear as abrupt black or white patches, including within molecular structures or microscopy legend areas.

Output Format (Strict)

Return ONLY a JSON object in the following format:
```json
{
   "bboxes": [[x1,y1,x2,y2], [x3,y3,x4,y4]],
   "reason": "..."
}
```
Strict Rules

"bboxes" must be a list of lists, and each list must follow the exact format:
[x1,y1,x2,y2]
with **four** integers and commas, no spaces.

Coordinates must satisfy:
0 ≤ x1 < x2 ≤ {WIDTH_1}
0 ≤ y1 < y2 ≤ {HEIGHT_1}

Maximum number of bounding boxes: 6.

Use bounding boxes only for visually suspicious or forged regions.
If no tampered region is found, return:
"bboxes": []

"reason" must be 1–2 concise sentences explaining why these boxes were selected.
Do NOT describe the entire image.

Do NOT output HTML/XML-style tags such as <...>

The entire response must contain ONLY the JSON object and nothing else.

Do NOT mention or reference the task instructions or constraints.

Examples

{
   "bboxes": [[120,45,230,160], [320,300,400,410]],
   "reason": "Two regions show boundary inconsistencies and texture artifacts that differ from the surrounding image."
}
