# Report format

The architecture review is a research report: `findings.md` as the source copy, one HTML fragment for each diagram, and `report.html` from the shared builder. The [research](../../research/SKILL.md) skill owns the folder, the builder, the template and the inline presentation. This file covers only what is specific to an architecture review.

## Structure of `findings.md`

1. A title with the repository name and the area reviewed.
2. A legend of one line: solid box = module, dashed line = seam, red arrow = leak, thick box = deep module.
3. One `##` section for each candidate. No introduction paragraph.
4. A final `## Top recommendation` section: the candidate name and one sentence on why.

## Candidate section

The diagram carries the weight. The prose is sparse and plain, and uses the Deep Modules terms.

- **Heading**: short, names the deepening (for example "Collapse the Order intake pipeline").
- **Strength and category**: `Strong`, `Worth exploring` or `Speculative`, and the dependency category (`in-process`, `local-substitutable`, `ports & adapters`, `mock`).
- **Files**: a list in code format.
- **Before / After diagram**: an `<!-- include: <candidate>.html -->` line.
- **Problem**: one sentence. What hurts.
- **Solution**: one sentence. What changes.
- **Wins**: bullets of six words or fewer, for example "Tests hit one interface", "Pricing logic stops leaking", "Delete 4 shallow wrappers".
- **ADR conflict**, if applicable: one line in a blockquote.

Write no paragraphs of explanation. If a diagram needs a paragraph to be understood, draw the diagram again.

## Diagram fragments

A fragment is a piece of HTML with inline styles and inline SVG. It has no `<html>` or `<body>` element, loads nothing from a network and needs no script. Use the theme variables of the report template with a fallback value, so that the diagram follows the host theme.

```html
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
  <figure style="margin:0">
    <figcaption style="font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted-foreground,#6b6b6b)">Before</figcaption>
    <svg viewBox="0 0 320 240" role="img" aria-label="Four shallow modules, pricing leaks across the seam">
      <rect x="10" y="20" width="120" height="40" rx="4" fill="none" stroke="var(--foreground,#1c1c1c)"/>
      <text x="70" y="45" text-anchor="middle" font-size="11" fill="var(--foreground,#1c1c1c)">OrderHandler</text>
      <line x1="130" y1="40" x2="190" y2="40" stroke="var(--destructive,#dc2626)" stroke-width="2"/>
    </svg>
  </figure>
  <figure style="margin:0">
    <figcaption style="font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted-foreground,#6b6b6b)">After</figcaption>
    <svg viewBox="0 0 320 240" role="img" aria-label="One deep Order intake module">
      <rect x="10" y="20" width="300" height="200" rx="4" fill="none" stroke="var(--foreground,#1c1c1c)" stroke-width="3"/>
      <text x="160" y="45" text-anchor="middle" font-size="11" fill="var(--foreground,#1c1c1c)">Order intake</text>
    </svg>
  </figure>
</div>
```

Give each `<svg>` an `aria-label` that states what the diagram shows. Keep each diagram about 240px tall, so that before and after sit side by side. Escape any source excerpt.

Choose the pattern that fits the candidate. Use different patterns for different candidates.

- **Boxes and arrows.** For dependencies and call flow. Draw modules as `<rect>` elements and arrows as `<line>` or `<path>` elements. Color the leak edges red. Draw a seam as a dashed line (`stroke-dasharray="4 4"`). In the "after" diagram, draw one thick-bordered deep module with its internals faded.
- **Cross-section.** For layered shallowness. Stack horizontal bands to show the layers a call passes through. Before: six thin layers that each do nothing. After: one thick band labeled with the consolidated responsibility.
- **Mass diagram.** For an interface as wide as its implementation. Draw two rectangles for each module: one for the interface, one for the implementation. Before: the interface rectangle is nearly as tall as the implementation rectangle. After: the interface rectangle is short and the implementation rectangle is tall.
- **Call-graph collapse.** Before: a tree of function calls drawn as nested boxes. After: the same tree inside one box, with the calls that are now internal shown faded.

When a diagram needs a style that several reports would reuse, add it to the shared template. Do not write a build script for one report.

## Tone

Plain English, concise. The architectural nouns and verbs come from [Deep Modules](../../forge/references/principles/deep-modules.md).

**Use exactly:** module, interface, implementation, depth, deep, shallow, seam, adapter, leverage, locality.

**Never substitute:** component, service or unit for module. API or signature for interface. Boundary for seam. Layer or wrapper when you mean module.

**Phrasings that fit:**

- "Order intake module is shallow: interface nearly matches the implementation."
- "Pricing leaks across the seam."
- "Deepen: one interface, one place to test."
- "Two adapters justify the seam: HTTP in prod, in-memory in tests."

**Wins bullets** name the gain in Deep Modules terms: "locality: bugs concentrate in one module", "leverage: one interface, N call sites". Do not write "easier to maintain" or "cleaner code".

No hedging and no preamble. If a sentence can be a bullet, make it a bullet. If a bullet can be cut, cut it.
