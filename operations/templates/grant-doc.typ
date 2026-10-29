// grant-doc.typ — minimalist scientific layout for grant and fellowship applications.
//
// Canonical copy: operations/templates/grant-doc.typ.
// Grant repositories vendor a pinned copy at their root; refresh one by re-copying this file.
// Modeled on a plain LaTeX grant application: a bold title,
// a few lines of plain byline text, an optional hairline, then the narrative.
// No shaded boxes, borders, or rounded corners.
//
// Usage:
//   #import "grant-doc.typ": grant-doc, grant-header
//   #show: grant-doc.with(title: "…", author: "…", running-head: [Name · Program])
//   #grant-header(title: [...], author: [...], affiliation: [...], mentor: [...], program: [...])
//   #grant-table(columns: 3, [*Head*], [*Head*], [*Head*], [cell], [cell], [cell])
//   #grant-letter(letterhead: (institution: [...], unit: [...], address: ([...],)), date: [...],
//     salutation: [...], signer: [...], signer-lines: ([...],))[Letter body.]
//   #show: nih-doc.with(title: "Specific Aims", author: "…", page-limit: nih-f-limits.specific-aims)

#let grant-doc-version = "0.4.0" // 2026-10-29: adds nih-doc and page-numbers

// Title and plain byline. Each argument is one line; `none` drops it.
// `program`, `track`, and `date` share the last standard line, separated by a middle dot.
// `extra` appends further lines (an array of content).
#let grant-header(
  title: none,
  author: none,
  affiliation: none,
  mentor: none,
  mentor-label: "Faculty Mentor",
  program: none,
  track: none,
  date: none,
  extra: (),
  title-size: 12.5pt,
  byline-size: 1em,
  rule: true,
) = {
  set par(justify: false, leading: 0.45em, spacing: 0.45em)
  block(below: 0.45em, text(size: title-size, weight: "bold", title))
  let award = (program, track, date).filter(x => x != none)
  let lines = (
    author,
    affiliation,
    if mentor != none [#mentor-label: #mentor],
    if award.len() > 0 { award.join[ · ] },
    ..extra,
  ).filter(x => x != none)
  text(size: byline-size, lines.join(linebreak()))
  if rule {
    v(0.15em)
    line(length: 100%, stroke: 0.4pt + luma(150))
  }
  v(0.45em)
}

// Booktabs-style table: a top rule, a thin rule under the header rows, and a bottom rule.
// No fills and no vertical lines. `rule-above` lists body rows (by table row index) that get a
// thin rule above them, for totals or subtotals. Cells are set ragged-right.
// Other arguments pass through to `table`.
#let grant-table(header-rows: 1, rule-above: (), ..args) = {
  set par(justify: false)
  table(
    stroke: (x, y) => (
      top: if y == 0 { 0.8pt } else if y == header-rows or y in rule-above { 0.4pt } else { none },
    ),
    ..args,
    table.hline(stroke: 0.8pt),
  )
}

// Institutional letterhead: institution and unit on the left, address on the right, hairline below.
#let grant-letterhead(institution: none, unit: none, address: ()) = {
  grid(
    columns: (1fr, auto),
    align: (left + bottom, right + bottom),
    [
      #text(size: 12pt, weight: "bold", institution)
      #if unit != none [\ #text(size: 0.9em, unit)]
    ],
    text(size: 0.85em, address.join(linebreak())),
  )
  v(0.15em)
  line(length: 100%, stroke: 0.4pt + luma(150))
  v(0.8em)
}

// Letter: optional letterhead (a dictionary of grant-letterhead arguments), optional title with
// plain detail lines, then date, recipient lines, salutation, body, closing, and signature block.
// `gap` separates date, recipient, salutation, body, and closing.
// Use for support, recommendation, and cover letters. Without a letterhead, the title block
// takes the hairline instead.
#let grant-letter(
  letterhead: none,
  title: none,
  details: (),
  date: none,
  recipient: (),
  salutation: none,
  closing: "Sincerely,",
  signer: none,
  signer-lines: (),
  signature-space: 2.2em,
  gap: 0.9em,
  body,
) = {
  if letterhead != none { grant-letterhead(..letterhead) }
  if title != none {
    grant-header(title: title, title-size: 11.5pt, byline-size: 0.9em, extra: details, rule: letterhead == none)
  }
  if date != none { block(below: gap, par(justify: false, date)) }
  if recipient.len() > 0 { block(below: gap, par(justify: false, recipient.join(linebreak()))) }
  if salutation != none { block(below: gap, par(justify: false, salutation)) }
  body
  v(gap, weak: true)
  par(closing)
  v(signature-space)
  block(below: 0.4em, line(length: 220pt, stroke: 0.6pt))
  set par(justify: false, leading: 0.45em)
  strong(signer)
  if signer-lines.len() > 0 { linebreak(); text(size: 0.9em, signer-lines.join(linebreak())) }
}

// Page, type, and paragraph setup. Apply with `#show: grant-doc.with(...)`.
// `running-head` is content, or a function from page number to content (for packets whose
// parts need different heads). It shows from page 2 unless `head-first-page` is true.
// The footer is a centered page number unless `page-numbers` is false.
#let grant-doc(
  title: none,
  author: "",
  keywords: (),
  running-head: none,
  head-first-page: false,
  page-numbers: true,
  margin: 0.75in,
  font: ("New Computer Modern", "Libertinus Serif", "Times New Roman"),
  size: 10.5pt,
  leading: 0.55em,
  spacing: 0.75em,
  body,
) = {
  set document(title: title, author: author, keywords: keywords)
  set page(
    paper: "us-letter",
    margin: margin,
    header: context {
      let p = counter(page).get().first()
      let head = if type(running-head) == function { running-head(p) } else { running-head }
      if head != none and (p > 1 or head-first-page) {
        set text(size: 8.5pt, fill: luma(90))
        head
      }
    },
    footer: if page-numbers { context align(center, text(size: 8.5pt, fill: luma(90), counter(page).display())) },
  )
  set text(font: font, size: size)
  set par(justify: true, leading: leading, spacing: spacing)
  body
}

// NIH attachment preset. Each NIH attachment is its own PDF. Rules checked 2026-10-29 against
// grants.nih.gov "Format Attachments" (updated 2024-09-30): margins of at least 0.5in, type of at
// least 11pt, at most 15 characters per inch and 6 lines per inch, and no headers, footers, or
// page numbers (NIH adds them). Arial, Georgia, Helvetica, and Palatino Linotype are recommended.
// Limits below are the Fellowship (F) column of "Page Limits" (updated 2026-09-30); the funding
// opportunity overrides them. The biosketch is built in SciENcv, not here.
#let nih-f-limits = (
  introduction: 1,
  candidate-goals: 3,
  training-activities: 3,
  specific-aims: 1,
  research-strategy: 6,
  rcr: 1,
  sponsor-commitment: 6,
  letters-of-support: 6,
  concurrent-support: 1,
)

// `page-limit` fails the compile when the attachment runs long.
#let nih-doc(
  title: none,
  author: "",
  page-limit: none,
  font: ("Georgia", "Arial"),
  size: 11pt,
  margin: 0.5in,
  body,
) = {
  assert(size >= 11pt, message: "NIH requires type of at least 11pt")
  show: grant-doc.with(
    title: title,
    author: author,
    page-numbers: false,
    margin: margin,
    font: font,
    size: size,
    leading: 0.6em,
    spacing: 0.9em,
  )
  body
  if page-limit != none {
    context {
      let n = counter(page).final().first()
      assert(n <= page-limit, message: "NIH page limit exceeded: " + str(n) + " pages, limit " + str(page-limit))
    }
  }
}
