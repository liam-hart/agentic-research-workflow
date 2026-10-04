# Decision-page spec format

A spec is one JSON object. `render_decision_page.py render` validates it and rejects it with an error that names the bad field. Every `id` uses lowercase letters, digits, and hyphens (at most 64 characters). All text is plain text: markup shows literally and never renders.

## Shared fields

| Field | Required | Notes |
|---|---|---|
| `kind` | yes | `compare` or `gallery` |
| `id` | yes | Page id; also the output filename and the `decisions-<id>.json` name |
| `title` | yes | Page heading |
| `concept` | no | The concept the page teaches |
| `context` | no | One short paragraph of background |

## `compare`: 1–12 decisions

Each entry in `decisions` has:
- `id`, `question` (required)
- `concept`, `context`, `why_it_matters`, `what_teams_do` (optional; the last two become expandable sections)
- `options`: 2–6 entries, each with `id`, `label`, `summary`, and `tradeoffs` (required), `what_goes_wrong` (optional, expandable), and `preview` (optional): `{"kind": "code", "text": "..."}` or `{"kind": "svg", "text": "<svg ...>"}`. SVG is embedded as an image, so it cannot run script.
- `recommendation`: `{"option": "<an option id>", "reason": "..."}` (required)

Every decision also gets a "Something else (explain in the note)" choice. Its result value is `_other`.

```json
{
  "kind": "compare",
  "id": "storage-choice",
  "title": "How results are stored",
  "decisions": [
    {
      "id": "format",
      "question": "Which file format holds trial results?",
      "concept": "schema design",
      "why_it_matters": "Every downstream analysis reads this format.",
      "options": [
        {"id": "csv", "label": "CSV", "summary": "One row per trial.", "tradeoffs": "Simple; no nesting."},
        {"id": "jsonl", "label": "JSON Lines", "summary": "One object per line.", "tradeoffs": "Nesting; larger files."}
      ],
      "recommendation": {"option": "csv", "reason": "Every tool reads it."}
    }
  ]
}
```

## `gallery`: 1–500 items

- `items`: each has `id`, `label`, and `image` (required). `image` is a local path relative to the spec file, an absolute path, or a `data:image/...` URI. Remote URLs are rejected. Each item can also have `meta`, a map of names to strings or numbers.
- `verdicts`: 2–6 unique lowercase words. Defaults to `["keep", "maybe", "reject"]`.
- `questions`: optional, 1–5 entries asked of every item. Each has `id`, `prompt`, and optional `choices` (a list of strings, shown as a dropdown; without it the answer is free text).

Pages over 20 MB trigger a warning. Shrink the images or split the gallery.

```json
{
  "kind": "gallery",
  "id": "chairs",
  "title": "Chair candidates",
  "items": [
    {"id": "chair-a", "label": "Chair A", "image": "renders/chair-a.png", "meta": {"tris": 1200}}
  ],
  "questions": [{"id": "fit", "prompt": "Fits the room?", "choices": ["yes", "no", "unsure"]}]
}
```

## Result

Copy for chat and Save file both carry `{collaborate_result: 1, id, kind, fingerprint, title, answers, general_note}`. The shape of `answers` depends on the kind:
- compare: `{decision_id: {choice, note}}`
- gallery: `{item_id: {verdict, note, answers: {question_id: value}}}`

`read --spec` checks the fingerprint (exit `2` when the page is stale) and prints the decisions with their labels. The fingerprint covers image contents as well as the spec, so regenerating an image under the same filename counts as a new page. `read --spec` therefore needs the images to still be in place.
