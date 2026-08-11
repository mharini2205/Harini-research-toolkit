#!/usr/bin/env python3
"""Render a research-paper brief (JSON) into a self-contained visual one-pager HTML.

Usage:
    python build_brief.py brief.json output_onepager.html

The JSON schema is documented in ../references/brief_schema.json. Every field is
optional except that missing content is rendered as a clear "Not reported" note
rather than being dropped, so the seven-section shape is always visible.
"""
import json
import sys
import html


def esc(x):
    return html.escape(str(x)) if x is not None else ""


def section_block(label, content, empty="Not reported in the paper."):
    body = esc(content).strip() if content else ""
    if not body:
        body = f'<span class="empty">{empty}</span>'
    return f"""
    <section class="block">
      <div class="block-label">{esc(label)}</div>
      <div class="block-body">{body}</div>
    </section>"""


def workflow_html(steps):
    if not steps:
        return '<span class="empty">Workflow not reported.</span>'
    cards = []
    for i, s in enumerate(steps, 1):
        title = esc(s.get("title", f"Step {i}"))
        detail = esc(s.get("detail", ""))
        cards.append(f"""
        <div class="step">
          <div class="step-num">{i}</div>
          <div class="step-title">{title}</div>
          <div class="step-detail">{detail}</div>
        </div>""")
    arrow = '<div class="arrow">&#8594;</div>'
    return '<div class="flow">' + arrow.join(cards) + '</div>'


def procedure_html(steps):
    """Plain-words walkthrough of the method — the narrative companion to the
    compact workflow blocks. Renders as a numbered list a non-specialist can
    follow. Optional; omitted entirely if not supplied."""
    if not steps:
        return ""
    items = []
    for s in steps:
        if isinstance(s, dict):
            title = s.get("title", "")
            detail = s.get("detail", "")
            text = f'<strong>{esc(title)}.</strong> {esc(detail)}' if title else esc(detail)
        else:
            text = esc(s)
        items.append(f"<li>{text}</li>")
    return ('<div class="procedure">'
            '<div class="proc-label">Step-by-step, in plain words</div>'
            '<ol class="proc-list">' + "".join(items) + "</ol></div>")


def authors_html(authors):
    if not authors:
        return '<span class="empty">Authors not reported.</span>'
    chips = []
    for a in authors:
        if isinstance(a, dict):
            name = esc(a.get("name", ""))
            role = a.get("role", "")
            role_html = f'<span class="role">{esc(role)}</span>' if role else ""
            chips.append(f'<span class="chip">{name}{role_html}</span>')
        else:
            chips.append(f'<span class="chip">{esc(a)}</span>')
    return '<div class="chips">' + "".join(chips) + "</div>"


def institutes_html(insts):
    if not insts:
        return '<span class="empty">Institutes not reported.</span>'
    chips = "".join(f'<span class="chip inst">{esc(i)}</span>' for i in insts)
    return '<div class="chips">' + chips + "</div>"


def note_html(note):
    """Optional 'Why it matters' callout. Renders only if present, so the
    one-pager stays clean for papers with no relevance. This is your own
    interpretation, not content from the paper, which is why it sits apart
    from the seven sections."""
    if not note:
        return ""
    return f"""
    <section class="block note">
      <div class="block-label">Why It Matters</div>
      <div class="block-body">{esc(note)}</div>
    </section>"""


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  :root {{
    --ink: #1a1d24; --muted: #6b7280; --line: #e3e6ec;
    --accent: #2f5fe0; --accent-soft: #eef2fe; --bg: #ffffff;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; background: #f4f5f8; color: var(--ink);
    font: 15px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    padding: 28px 16px;
  }}
  .page {{
    max-width: 900px; margin: 0 auto; background: var(--bg);
    border: 1px solid var(--line); border-radius: 14px; padding: 34px 38px;
    box-shadow: 0 1px 3px rgba(0,0,0,.05);
  }}
  header {{ border-bottom: 2px solid var(--accent); padding-bottom: 14px; margin-bottom: 22px; }}
  .kicker {{ font-size: 11px; letter-spacing: .12em; text-transform: uppercase; color: var(--accent); font-weight: 700; }}
  h1 {{ font-size: 22px; line-height: 1.25; margin: 6px 0 4px; }}
  .citation {{ color: var(--muted); font-size: 13px; }}
  .block {{ margin-bottom: 20px; }}
  .block-label {{
    font-size: 11px; letter-spacing: .1em; text-transform: uppercase;
    color: var(--accent); font-weight: 700; margin-bottom: 6px;
  }}
  .block-body {{ font-size: 14.5px; }}
  .empty {{ color: var(--muted); font-style: italic; }}
  .flow {{ display: flex; flex-wrap: wrap; align-items: stretch; gap: 4px; }}
  .step {{
    flex: 1 1 150px; min-width: 140px; background: var(--accent-soft);
    border: 1px solid #d5ddf8; border-radius: 10px; padding: 10px 12px; position: relative;
  }}
  .step-num {{
    position: absolute; top: -9px; left: -9px; width: 22px; height: 22px;
    background: var(--accent); color: #fff; border-radius: 50%;
    font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center;
  }}
  .step-title {{ font-weight: 700; font-size: 13.5px; margin-bottom: 3px; }}
  .step-detail {{ font-size: 12.5px; color: #40454f; line-height: 1.4; }}
  .arrow {{ display: flex; align-items: center; color: var(--accent); font-size: 20px; padding: 0 2px; }}
  .procedure {{ margin-top: 16px; }}
  .proc-label {{ font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); font-weight: 700; margin-bottom: 6px; }}
  .proc-list {{ margin: 0; padding-left: 20px; }}
  .proc-list li {{ font-size: 13.5px; line-height: 1.5; margin-bottom: 6px; }}
  .proc-list li strong {{ color: var(--ink); }}
  .chips {{ display: flex; flex-wrap: wrap; gap: 7px; }}
  .chip {{
    background: #f1f3f7; border: 1px solid var(--line); border-radius: 20px;
    padding: 4px 12px; font-size: 13px;
  }}
  .chip.inst {{ background: var(--accent-soft); border-color: #d5ddf8; }}
  .chip .role {{ color: var(--accent); font-size: 11px; margin-left: 6px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }}
  .note {{ margin-top: 22px; background: #fff8ec; border: 1px solid #f0d9a8; border-left: 4px solid #d98a1f; border-radius: 10px; padding: 14px 16px; }}
  .note .block-label {{ color: #b56b12; }}
  .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
  @media (max-width: 620px) {{ .two-col {{ grid-template-columns: 1fr; }} .arrow {{ transform: rotate(90deg); }} }}
  @media print {{ body {{ background: #fff; padding: 0; }} .page {{ border: none; box-shadow: none; }} }}
</style>
</head>
<body>
  <div class="page">
    <header>
      <div class="kicker">Research Paper Brief</div>
      <h1>{title}</h1>
      <div class="citation">{citation}</div>
    </header>
    {objective}
    {hypothesis}
    <section class="block">
      <div class="block-label">Experiment Workflow</div>
      {workflow}
      {procedure}
    </section>
    {outcomes}
    {future}
    <div class="two-col">
      <section class="block">
        <div class="block-label">Main Authors</div>
        {authors}
      </section>
      <section class="block">
        <div class="block-label">Research Institutes</div>
        {institutes}
      </section>
    </div>
    {note}
  </div>
</body>
</html>"""


def build(data):
    return TEMPLATE.format(
        title=esc(data.get("title", "Untitled paper")),
        citation=esc(data.get("citation", "")),
        objective=section_block("Objective", data.get("objective")),
        hypothesis=section_block("Hypothesis", data.get("hypothesis")),
        workflow=workflow_html(data.get("workflow", [])),
        procedure=procedure_html(data.get("procedure", [])),
        outcomes=section_block("Outcomes Generated", data.get("outcomes")),
        future=section_block("Future Directions", data.get("future_directions")),
        authors=authors_html(data.get("authors", [])),
        institutes=institutes_html(data.get("institutes", [])),
        note=note_html(data.get("note")),
    )


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)
    html_out = build(data)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"Wrote {sys.argv[2]}")


if __name__ == "__main__":
    main()
