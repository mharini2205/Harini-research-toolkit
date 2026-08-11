#!/usr/bin/env node
/*
 * build_dossier.js — render a researcher dossier DOCX from a JSON spec.
 *
 * Why this exists: every dossier shares the same house styling (blue headings,
 * bold "Bottom line", bulleted classification, dated verification note). Rather
 * than hand-writing a docx-js builder each time, fill a JSON spec and run this.
 *
 * Usage:
 *   npm install docx        # once, in a writable dir
 *   node build_dossier.js <spec.json>
 *
 * The spec's "output" path is where the .docx is written (e.g. /profiles/Surname_Inst.docx).
 * See references/dossier_spec.example.json for the schema. Blocks render in order:
 *   {"type":"bottomline","text":"...","links":[...]}   bold "Bottom line:" lead-in
 *   {"type":"h1"|"h2","text":"..."}
 *   {"type":"p","label":"Why it matters: ","text":"...","links":[{"text":"","url":""}]}
 *   {"type":"bullet","label":"Classification: ","text":"..."}
 *   {"type":"sources","items":[{"text":"","url":""}]}
 * Any block may include "links" (rendered inline after the text, " · " separated).
 */
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  ExternalHyperlink, BorderStyle, LevelFormat
} = require("docx");

const BLUE = "2E75B6", GRAY = "555555";
const specPath = process.argv[2];
if (!specPath) { console.error("usage: node build_dossier.js <spec.json>"); process.exit(1); }
const spec = JSON.parse(fs.readFileSync(specPath, "utf8"));

function linkRuns(links) {
  const out = [];
  (links || []).forEach((l, i) => {
    if (i) out.push(new TextRun("  ·  "));
    out.push(new ExternalHyperlink({
      children: [new TextRun({ text: l.text, style: "Hyperlink" })], link: l.url }));
  });
  return out;
}
function textRuns(block) {
  const runs = [];
  if (block.label) runs.push(new TextRun({ text: block.label, bold: true }));
  if (block.text) runs.push(new TextRun(block.text));
  if (block.links && block.links.length) { runs.push(new TextRun("  ")); runs.push(...linkRuns(block.links)); }
  return runs;
}

const children = [];
children.push(new Paragraph({ spacing: { after: 60 },
  children: [new TextRun({ text: spec.title || "Researcher Dossier", bold: true, size: 34, font: "Arial" })] }));
if (spec.subtitle) children.push(new Paragraph({ spacing: { after: 40 },
  children: [new TextRun({ text: spec.subtitle, italics: true, color: GRAY, size: 22 })] }));
children.push(new Paragraph({
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BLUE, space: 1 } },
  spacing: { after: 160 },
  children: [new TextRun({ text: spec.footer || "Confidential — internal IP/competitive intelligence", color: GRAY, size: 18 })] }));

for (const block of (spec.blocks || [])) {
  switch (block.type) {
    case "h1": children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(block.text)] })); break;
    case "h2": children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(block.text)] })); break;
    case "bottomline":
      children.push(new Paragraph({ spacing: { after: 140 },
        children: [new TextRun({ text: "Bottom line: ", bold: true }), new TextRun(block.text), ...(block.links ? [new TextRun("  "), ...linkRuns(block.links)] : [])] }));
      break;
    case "bullet":
      children.push(new Paragraph({ numbering: { reference: "b", level: 0 }, spacing: { after: 80 }, children: textRuns(block) })); break;
    case "sources":
      children.push(new Paragraph({ spacing: { before: 120 }, children: [new TextRun({ text: "Sources: ", bold: true }), ...linkRuns(block.items)] })); break;
    case "p":
    default:
      children.push(new Paragraph({ spacing: { after: 120 }, children: textRuns(block) }));
  }
}

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: BLUE }, paragraph: { spacing: { before: 260, after: 140 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 23, bold: true, font: "Arial" }, paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 1 } },
    ]
  },
  numbering: { config: [ { reference: "b", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 540, hanging: 260 } } } }] } ] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } }, children }]
});

Packer.toBuffer(doc).then(buffer => {
  const out = spec.output || "dossier.docx";
  fs.mkdirSync(require("path").dirname(out), { recursive: true });
  fs.writeFileSync(out, buffer);
  console.log("written: " + out);
});
