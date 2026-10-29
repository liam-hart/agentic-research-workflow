// response-doc.typ — point-by-point response to reviewers, in the grant-doc layout.
//
// Canonical copy: operations/templates/response-doc.typ. It imports grant-doc.typ,
// so a manuscript repository vendors both files side by side and refreshes them by re-copying.
// Typography separates the three voices without color (cover-letter skill § 4):
//   reviewer comment  — italic, indented, numbered (Comment R1.2)
//   author response   — roman, run-in bold "Response."
//   revised text      — indented on both sides, smaller, with its page/line location
//
// Usage:
//   #import "response-doc.typ": response-doc, reviewer, comment, response, revised
//   #show: response-doc.with(title: [...], manuscript: [...], author: "…")
//   [Opening thanks and roadmap.]
//   #reviewer()  // or #reviewer(label: [Editor])
//   #comment[Reviewer text, verbatim.]
//   #response[What changed and why.]
//   #revised(location: [p. 12, lines 240–248])[Quoted revised manuscript text.]

#import "grant-doc.typ": grant-doc, grant-header

#let response-doc-version = "0.1.0" // 2026-10-29

#let _reviewer = counter("response-reviewer")
#let _comment = counter("response-comment")
#let _label = state("response-label", none)

// Page setup and title block. `manuscript` is the manuscript ID and title line; `journal` and
// `date` share the byline's last line.
#let response-doc(
  title: [Response to Reviewers],
  manuscript: none,
  authors: none,
  journal: none,
  date: none,
  author: "",
  running-head: none,
  size: 11pt,
  body,
) = {
  show: grant-doc.with(
    title: title,
    author: author,
    running-head: running-head,
    size: size,
  )
  grant-header(title: title, author: manuscript, affiliation: authors, program: journal, date: date)
  body
}

// Starts a reviewer section. Numbered reviewers by default; pass `label` for the editor or for
// named reviewers; a labelled section does not take a reviewer number. Comment numbers restart
// in each section.
#let reviewer(label: none) = {
  if label == none { _reviewer.step() }
  _comment.update(0)
  _label.update(label)
  context {
    let name = if label != none { label } else [Reviewer #_reviewer.get().first()]
    block(above: 1.4em, below: 0.8em, text(size: 1.1em, weight: "bold", name))
  }
}

// A reviewer comment, quoted verbatim.
#let comment(body) = {
  _comment.step()
  context {
    let prefix = if _label.get() != none { "E" } else { "R" + str(_reviewer.get().first()) }
    block(above: 1.1em, below: 0.6em, [*Comment #prefix.#_comment.get().first()*])
  }
  pad(left: 1.5em, block(below: 0.7em, emph(body)))
}

// The author response, run in after a bold label.
#let response(body) = block(below: 0.7em)[*Response.* #body]

// Quoted revised manuscript text, with its location in the revised manuscript.
#let revised(location: none, body) = pad(x: 1.5em, block(below: 0.8em)[
  #set text(size: 0.92em)
  #set par(justify: false)
  #if location != none [_Revised text (#location):_ \ ]
  “#body”
])
