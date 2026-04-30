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
- "answer" must be exactly one of: "A", "B", "C", "D";
- Do NOT include XML, Markdown, or comments;
- Return ONLY a JSON object;
- "reason" should follow these aspects:

#### No Forgery
1. Consistent and Constrained Graphical Structure
- Line shapes are stable, with consistent thickness, direction, and connectivity throughout the figure.
- Polylines, trend curves, and comparison lines exhibit smooth and continuous transitions, without jitter, breaks, or ghosting.
- No redundant, meaningless overlapping lines or random distortions are present.

2. Semantically Complete and Self-Consistent Chart Representation
- All colors, symbols, and visual markers correspond to well-defined data semantics or legend entries.
- No decorative or non-functional visual elements are present that cannot be mapped to any variable, dimension, or visual encoding.

3. Standardized and Semantically Meaningful Text
- All characters have complete strokes and standard shapes, conforming to printed fonts or commonly used scientific visualization typography.
- All textual elements (axis labels, annotations, legends) are semantically meaningful and free from garbled, misspelled, or pseudo-text characters.

4. Globally Consistent Texture and Visual Clarity
- All regions of the image exhibit consistent sharpness, detail level, and noise distribution.
- No localized abnormal blurring, over-sharpening, or anomalous black/white artifacts are observed.

Output format:
Please output your answer in non-segmented text format, not Markdown format, as follows: "[Explanation of the realistic aspects found in the image, such as consistent textures, all readable texts etc.]" 

#### entirely AI-generated / partially AI-edited 

1. Line Anomalies
- Lines exhibit irregular jitter, breaks, or repeated overlaps, lacking geometric or data-driven constraints.
- Trend lines and grid lines appear discontinuous or structurally unstable, deviating from outputs produced by standard plotting or charting tools.

2. Visual Structures Without Semantic Support
- Regular color blocks, stripes, or grid-like regions appear but cannot be mapped to any coordinate axis, data series, or visual encoding rule.
- Scatter points are mechanically clustered in localized areas or unnaturally concentrated along boundaries, resulting in distributions that do not align with statistical or experimental logic.
- The image appears to have a chart-like structure, yet its visual elements fail to convey meaningful data semantics.

3. Textual Anomalies
- Character shapes are distorted, with missing strokes or invalid compositions that violate linguistic or typographic rules.
- Labels fail to form readable words or valid scientific annotations (e.g., pseudo-text, garbled characters, or fragmented text).

4. Localized Rendering Inconsistencies (Partially AI-Edited Only)
- Different regions exhibit significant variations in sharpness, noise patterns, or detail levels.
- Local areas appear abnormally blurred or over-smoothed, inconsistent with the overall rendering or plotting style.

5. Violations of Chart Semantics and Scientific Conventions
- While the overall chart structure may appear valid, key semantic elements are incorrect or missing.
- Axis scales are abnormal, inconsistent, or incomplete.
- Annotations, error bars, and symbolic notations do not conform to any standard data visualization conventions.
- Chemical structural formulas or schematic diagrams exhibit obvious misalignment or structural errors.

6. Localization Requirements (Partially AI-Edited Only)
- Clearly identify the tampered object or the specific part of the object that has been manipulated.
- Supplement the region indices with directional descriptors (e.g., center, upper-left, lower-right).

Output format:
Please output your answer in non-segmented text format, not Markdown format, as follows:
[Localization of the AI-generated region] (Partially AI-Edited only) [Explanation of the AI-generated clues found in the image, such as inconsistent textures, text errors, etc.]

