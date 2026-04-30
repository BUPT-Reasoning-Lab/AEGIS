---
### Image  [see below]
---

### Question 
**What is the forgery scope of this academic image)**
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
- Text is clear and carries explicit, verifiable semantic meaning, corresponding to well-defined variables, objects, or experimental conditions.

2. Realistic and Consistent Texture Characteristics  
- The image exhibits anatomically correct structures and conforms to physically valid X-ray imaging principles, with realistic anatomical layering and attenuation behavior and no non-physical soft-tissue visibility or glowing effects.

Output format:
Please output your answer in non-segmented text format, not Markdown format, as follows: "[Explanation of the realistic aspects found in the image, such as realistic structure and consistent textures, etc.]"

#### entirely AI-generated / partially AI-edited
If localized manipulation cues are present, the image should be classified as Partially AI-Edited, even if the overall style appears globally consistent or synthetic. Entirely AI-generated should only be selected when no meaningful localized manipulation can be identified.

1. Fundamental Physical Violations
- Anatomical inconsistencies: The image exhibits abnormal shapes of the cornea, organs, or skeletal structures, incorrect structural arrangements, or significantly distorted proportions, violating established human or animal anatomical principles.
- Violations of realistic X-ray imaging: The image contradicts attenuation-based X-ray imaging physics, such as incorrect superposition of anatomical layers, implausible visibility of soft tissues, or uniformly glowing structures that cannot occur in real X-ray acquisitions.

2. Textual Hallucination and Domain Violations  
- Text includes misspellings, inconsistent capitalization, or mixtures of real terms with fabricated or pseudo-technical fragments that violate disciplinary conventions.  
- Text may appear locally plausible but is globally inconsistent, contradictory, or unverifiable in context, such as numerical labels that do not follow a logical or sequential order.
- Text fails to form readable words or valid scientific annotations (e.g., pseudo-text, garbled characters, fragmented symbols).

3. Localized Anomalies or Edits (Partially AI-Edited Only)
- Partial AI-Edited refers to cases where part of an object or the background has been altered, a new object has been added, or an existing object has been removed, for example, regions that mimic structurally similar materials or molecules but exhibit inconsistent lighting or physical properties compared to real microscopy images.
- Visible manipulation boundaries may exist between edited and unedited regions, such as outline artifacts around tampered areas.  
- Edited regions where objects have been removed may appear as abrupt black or white patches, including within molecular structures or microscopy legend areas.

4. Localization Requirements (Partially AI-Edited Only)  
- Clearly identify the manipulated object or the specific part of the object that has been altered.  
- Supplement region identification with directional descriptors (e.g., center, upper-left, lower-right).

Output format:
Please output your answer in non-segmented text format, not Markdown format, as follows: "[Localization of the AI-generated region] (Partially AI-Edited only) [Explanation of the AI-generated clues found in the image, such as unrealistic physical structure, textual hallucination, etc.]"  