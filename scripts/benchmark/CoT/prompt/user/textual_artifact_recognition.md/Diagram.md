You are given a single academic / scientific image.
---
### Image  [see below]
---


### Question 
**Does the image contain any AI-generated or AI-edited text forgeries, based on visual artifacts, structural irregularities, or semantic mismatches between the embedded text and the scientific content?**

### Options
{OPTIONS_BLOCK}

### Output Format (Strict)
Return ONLY a JSON object in the following format:

{
  "answer": "{selected_letter}",
  "reason": "..."
}


### Output Examples:
{
  "answer": "A",
  "reason": "..."
}

{
  "answer": "B",
  "reason": "..."
}

**Important Notes:**
- Select ONLY one option letter (A/B)
- Return valid JSON with "answer" key
- Base your decision on the Test Image relative to the Reference Image

### Rules:
- "answer" must be exactly one of: "A", "B";
- Do NOT include XML, Markdown, or comments;
- Return ONLY a JSON object;
- "reason" should consider these aspects:

####  No
1. Typographic Integrity
- All characters have complete strokes and standard shapes, conforming to printed fonts or commonly used scientific visualization typography.
- Do not assume any character is correct based on semantic plausibility. Inspect each character purely as a visual glyph, including stroke continuity, closure, symmetry, curvature, and consistency with standard printed fonts.

2. Semantic and Scientific Validity of Text
- All textual elements (e.g., annotations and legends) are semantically meaningful and **free from garbled, misspelled, or pseudo-teSt characters**; for example, module names in a pipeline, place names, or relationship labels are valid, interpretable, and contextually appropriate. 
- Spelling errors should not occur in textual elements.

Output format:
Please output your answer in non-segmented text format, not Markdown format, as follows: "[Explanation of the realistic aspects found in the image, such as consistent textures, all readable texts etc.]" 

#### Yes
1. Typographic Deformation and Glyph Corruption
- Character shapes are distorted, with missing strokes or invalid compositions that violate linguistic or typographic rules.
- Inconsistent capitalization and glyph sizing, where uppercase and lowercase letters occupy uneven visual space, violating standard typographic conventions.
- Characters appear handwritten or cursive rather than rendered in standard printed or scientific typography, which is atypical for formal academic or technical figures.

2. Semantic Invalidity and Textual Halluciation
- Texts fail to form readable words or valid scientific annotations (e.g., pseudo-text, garbled or fragmented characters, overlapping text, or cluttered symbol stacking), such as numerical values that do not correspond to the depicted content or the use of non-existent or fabricated terms.
- Text remains seemingly valid even when detached from its context, relying on highly generic placeholder terms (e.g., “variable”, “analysis”) that do not refer to any specific discipline, experiment, or measurable entity.
- Scientific terms, taxonomic names, or entities are linguistically plausible but unverifiable, lacking correspondence to recognized domain databases, standards, or literature.
- An unusually high density of obscure yet plausible domain-specific names appears without sufficient contextual grounding, experimental linkage, or explanatory structure.
- Hierarchical systems are violated, with incompatible ranks mixed or unsupported groups invented.

3. Localization Requirements 
- Clearly identify the the specific part of the text that has been manipulated or added.
- Supplement the region indices with directional descriptors (e.g., center, upper-left, lower-right).


Output format:
Please output your answer in non-segmented text format, not Markdown format, as follows:
[Localization of the AI-generated text region] [Explanation of the AI-generated clues found in the image, such as inconsistent textures, text errors, etc.]
--
