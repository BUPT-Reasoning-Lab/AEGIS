---
### Image  [see below]
---

### Question 
**What is the forgery scope of this academic image**
---
### Options (Single Choice)
{OPTIONS_BLOCK} 
---

### Output Format (Strict)
Return ONLY a JSON object in the following format:

{
  "answer": "A",
  "reason": "..."
}

### Rules:
- "answer" must be exactly one of: "A", "B", "C", "D".
- Do NOT include XML, Markdown, or comments.
- Output must be valid JSON.
- Do not classify an image as No Forgery based solely on global visual consistency or professional layout; explicitly verify semantic or system-level feasibility and check for tartgeted region restoration or editing before concluding.
- "reason" should consider these aspects:

#### No Forgery

1. Standardized and Semantically Meaningful Text  
- Data tables contain consistent and reasonable row/column structures, with data types matching their headers.  
- Text is clear and carries explicit, verifiable semantic meaning, corresponding to well-defined variables, objects, or experimental conditions.

2. All Visual Elements Carry Explicit Semantic Meaning  
- There is no excessive stacking of mathematical symbols, structural modules, or visual elements solely to enhance visual complexity.

3. Realistic and Consistent Texture Characteristics  
- Lines, markers, and color schemes remain consistent throughout the figure and serve information delivery rather than aesthetic or conceptual decoration.

4. Structurally Complete and Intact Composition
- No critical structural components are missing, removed, or replaced by blank, placeholder, or semantically empty regions that would undermine the intended informational or functional role of the figure. For example, a journal cover contains a full title, publisher information, and a central research illustration; a data table includes clear headers and all required non-empty data entries.

Output format:
Please output your answer in non-segmented text format, not Markdown format, as follows: "[Explanation of the realistic aspects found in the image, such as consistent texture, absence of meaningless visual elements, and semantically grounded content.]"

#### entirely AI-generated / partially AI-edited
If localized manipulation cues are present, the image should be classified as Partially AI-Edited, even if the overall style appears globally consistent or synthetic. Entirely AI-generated should only be selected when no meaningful localized manipulation can be identified.

1. Visually Plausible but Semantically Empty Modules  
- Variations in color, shape, or structure do not correspond to mechanistic or semantic differences and exist only for aesthetic complexity.  
- No interpretable functional partitions, hierarchies, or meaningful system logic can be identified upon decomposition.  
- Some elements are purely decorative and lack semantic or functional expression, such as cover-style imagery or dense stacking of formulas, charts, or visual components without analytical purpose.

2. Textual Hallucination and Domain Violations  
- Text includes misspellings, inconsistent capitalization, or mixtures of real terms with fabricated or pseudo-technical fragments that violate disciplinary conventions.  
- Text may appear locally plausible but is globally inconsistent, contradictory, or unverifiable in context, for example, table entries that do not conform to the defined row or column semantics, or values that differ in format or meaning from others in the same row or column.  
- Text fails to form readable words or valid scientific annotations (e.g., pseudo-text, garbled characters, fragmented symbols).

3. Localized Anomalies or Edits (Partially AI-Edited Only)
- Partial AI-Edited refers to cases where part of an object or the background has been altered, a new object has been added, or an existing object has been removed.
- Visible manipulation boundaries may exist between edited and unedited regions, such as outline artifacts around tampered areas.  
- Edited regions where an existing object has been removed, for example, an abrupt black or white area appears, or the central visual region of a journal cover lacks any interpretable scientific content and instead appears as a smooth, featureless placeholder rather than a meaningful illustration.

4. Localization Requirements (Partially AI-Edited Only)  
- Clearly identify the manipulated object or the specific part of the object that has been altered.  
- Supplement region identification with directional descriptors (e.g., center, upper-left, lower-right).

Output format:
Please output your answer in non-segmented text format, not Markdown format, as follows: "[Localization of the AI-generated region] (Partially AI-Edited only) [Explanation of the AI-generated clues found in the image, such as inconsistent textures, textual hallucination, unnatural outlines, etc.]" 