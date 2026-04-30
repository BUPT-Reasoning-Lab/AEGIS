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

2. Global Visual and Imaging Consistency
- The background and foreground objects exhibit consistent spatial resolution, sharpness, and noise characteristics, without artificial separation between focal planes.

3. Realistic Biological and Structural Validity
- Human, animal, or organ structures follow real anatomical rules in shape, proportion, and composition.

Output format:
Please output your answer in non-segmented text format, not Markdown format, as follows: "[Explanation of the realistic aspects found in the image, such as consistent textures, accurate proportions, natural color, etc.]" 

#### entirely AI-generated / partially AI-edited  
If localized manipulation cues are present, the image should be classified as Partially AI-Edited, even if the overall style appears globally consistent or synthetic. Entirely AI-generated should only be selected when no meaningful localized manipulation can be identified.

1. Inconsistencies in Imaging or Visual Formation
- Inconsistencies between foreground objects and background, such as AI-simulated focus or depth-of-field, where the object and background exhibit mismatched resolution, sharpness, or noise characteristics.
- Composition and lighting appear aesthetically optimized rather than observational, with overly smooth gradients, high color saturation, or stylized illumination that resemble artistic rendering instead of natural capture or scientific imaging.

2. Violations of Biological or Physical Structure
- Depicted biological or material structures violate real-world physical constraints, appearing overly idealized, stylized, or artifact-like (e.g., liquid droplets with uniform spherical geometry, glass-like texture), which is inconsistent with realistic experimental or natural samples.
- Structural anatomy is implausible or internally inconsistent, such as human hands with incorrect finger count, abnormal joint structure, or impossible skeletal configuration.

3. Textual Hallucination and Domain Violations  
- Text includes misspellings, inconsistent capitalization, or mixtures of real terms with fabricated or pseudo-technical fragments that violate disciplinary conventions.  
- Text may appear locally plausible but is globally inconsistent, contradictory, or unverifiable in context, such as numerical labels that do not follow a logical or sequential order.
- Text fails to form readable words or valid scientific annotations (e.g., pseudo-text, garbled characters, fragmented symbols).

4. Localized Anomalies or Edits (Partially AI-Edited Only)
- Partial AI-Edited refers to cases where part of an object or the background has been altered, a new object has been added, or an existing object has been removed.
- Visible manipulation boundaries may exist between edited and unedited regions, such as outline artifacts around tampered areas.  
- Edited regions where an existing object has been removed, for example, Existing objects are partially removed by background-colored overlays, producing flat regions that overwrite original structure and create unnatural object boundaries.

5. Localization Requirements (Partially AI-Edited Only)  
- Clearly identify the manipulated object or the specific part of the object that has been altered.  
- Supplement region identification with directional descriptors (e.g., center, upper-left, lower-right).

Output format:
Please output your answer in non-segmented text format, not Markdown format, as follows: "[Localization of the AI-generated region] (Partially AI-Edited only) [Explanation of the AI-generated clues found in the image, such as inconsistent textures, unrealistic physical structure, etc.]" 