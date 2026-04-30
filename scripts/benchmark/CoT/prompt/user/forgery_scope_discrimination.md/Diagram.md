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
- Do not classify an image as No Forgery based solely on global visual consistency or professional layout; explicitly verify semantic or system-level feasibility and check for tartgeted region restoration or editing before concluding.
- "reason" should follow these aspects:

#### No Forgery
1. Consistent and Mechanism-Constrained Structural Topology  
- Nodes, connections, and arrows form a stable, well-constrained topology with consistent line thickness and connection styles.  
- Arrow directions convey clear causal or procedural meanings (e.g., activation, inhibition, transport, step order), and the overall topology can be plausibly mapped to a real mechanism or workflow rather than a purely schematic composition.

2. Semantically Grounded Visual Elements  
- All visual elements correspond to explicit semantic roles, such as molecules, organelles, functional modules, or process stages, with each element serving a necessary functional purpose.
- No elements are purely decorative; each shape or color has a consistent, reusable meaning that can be explained by the caption or context and is meaningful within the depicted scientific or engineering system.

3. Domain-Valid and Self-Consistent Textual Annotations  
- All labels are verifiable, domain-valid terms, following disciplinary conventions for naming, capitalization, and indexing (e.g., gene/protein names, pathway abbreviations, step numbers).  
- No spelling errors, pseudo-terms, or unverifiable “professional-looking” text.  
- Identical concepts are labeled consistently throughout the figure, and the labeled entities and relations are plausibly grounded in established domain knowledge.

4. Globally Coherent Rendering Style and Visual Fidelity  
- Uniform clarity, line sharpness, texture detail, and noise distribution, with no anomalous local blur, oversmoothing, or over-sharpening.  
- The style aligns with standard academic diagramming tools and conventions rather than illustrative or artistic rendering, and visual coherence is accompanied by scientifically meaningful content rather than surface-level polish alone.

Output format:
Please output your answer in non-segmented text format, not Markdown format, as follows: "[Explanation of the realistic aspects found in the image, such as consistent textures, all readable texts etc.]" 

#### entirely AI-generated / partially AI-edited
1. Structural Anomalies Without Mechanistic Constraints
- Connections and arrows bend arbitrarily, break, or intersect unreasonably
- Layouts are overly symmetric or radial without corresponding to any real mechanism or process.  
- Arrow directions lack clear semantics, favoring visual composition over mechanistic expression.

2. Visually Plausible but Semantically Empty Modules
- Nodes are highly similar in shape and texture, repeatedly appearing without distinct functional roles or necessity within the system.
- Variations in color or shape do not map to mechanistic differences and serve only aesthetic complexity.
- No interpretable functional partitions, hierarchies, or meaningful system logic emerge upon decomposition.

3. Textual Hallucination and Domain Violations
- Labels include misspellings, inconsistent capitalization, or mixtures of real terms with fabricated, pseudo-technical fragments that violate disciplinary norms.
- Text may appear locally plausible but is globally inconsistent, contradictory, or unverifiable when considered in the full scientific or engineering context.

4. Violations of Diagram Semantics and Scientific Conventions
- Missing or incorrect key semantics, such as non-closed process flows, incomplete input–output relations, missing intermediary steps, or implausible system-level organization.
- Structural errors in molecular diagrams, schematic links, or functional relations that do not correspond to any known scientific or engineering model, even if the figure appears visually clean and well-formatted.

5. Localized Rendering Inconsistencies (Partially AI-Edited Only)
- Noticeable regional differences in sharpness, noise patterns, or line precision; some areas appear overly smooth, blurred, or over-sharpened, suggesting post-generation edits or local replacements.  
- Edited regions fail to blend naturally with the original style, often manifested as unnatural contours or visible outline artifacts around objects.

6. Localization Requirements (Partially AI-Edited Only)
- Clearly identify the tampered object or the specific part of the object that has been manipulated.
- Supplement the region indices with directional descriptors (e.g., center, upper-left, lower-right).

Output format:
Please output your answer in non-segmented text format, not Markdown format, as follows:
[Localization of the AI-generated region] (Partially AI-Edited only) [Explanation of the AI-generated clues found in the image, such as inconsistent textures, semantic inconsistencies, or violations of scientific conventions.]