#!/usr/bin/env python3
"""Render and read collaborate decision pages.

``render`` validates a JSON spec, embeds its images, and writes one
self-contained HTML page. ``read`` parses a Copy-for-chat paste or a saved
``decisions-<id>.json`` and checks it against the spec fingerprint. Standard
library only, so any agent in any repository can run it.
"""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import html
import json
import mimetypes
import re
import sys
import webbrowser
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "assets"
DEFAULT_OUT = Path(".decision-pages")
DEFAULT_VERDICTS = ["keep", "maybe", "reject"]
OTHER_CHOICE = "_other"
RESULT_VERSION = 1
SIZE_WARN_BYTES = 20 * 1024 * 1024
ID_RE = re.compile(r"[a-z0-9][a-z0-9-]{0,63}")
FENCE_RE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)
PLACEHOLDER_RE = re.compile(r"__(TITLE|PAYLOAD)__|/\*__(COMMON_CSS|COMMON_JS)__\*/")


class SpecError(ValueError):
    """The spec cannot be rendered; the message names the offending field."""


class ResultError(ValueError):
    """A pasted or saved result cannot be read."""


class StaleResultError(ResultError):
    """The result came from a different version of the spec."""


def _text(obj: dict, key: str, where: str, *, required: bool = True) -> str | None:
    value = obj.get(key)
    if value is None and not required:
        return None
    if not isinstance(value, str) or not value.strip():
        raise SpecError(f"{where}.{key} must be a non-empty string")
    return value


def _ident(obj: dict, where: str) -> str:
    value = _text(obj, "id", where)
    if not ID_RE.fullmatch(value):
        raise SpecError(
            f"{where}.id {value!r} must be lowercase letters, digits, and hyphens"
        )
    return value


def _objects(obj: dict, key: str, where: str, low: int, high: int) -> list[dict]:
    value = obj.get(key)
    if not isinstance(value, list) or not low <= len(value) <= high:
        raise SpecError(f"{where}.{key} must be a list of {low}-{high} entries")
    for index, entry in enumerate(value):
        if not isinstance(entry, dict):
            raise SpecError(f"{where}.{key}[{index}] must be an object")
    return value


def _unique(ids: list[str], where: str) -> None:
    seen: set[str] = set()
    for ident in ids:
        if ident in seen:
            raise SpecError(f"duplicate id {ident!r} in {where}")
        seen.add(ident)


def _validate_preview(preview: object, where: str) -> None:
    if preview is None:
        return
    if not isinstance(preview, dict) or preview.get("kind") not in {"code", "svg"}:
        raise SpecError(f"{where}.preview must be {{kind: code|svg, text}}")
    text = _text(preview, "text", f"{where}.preview")
    if preview["kind"] == "svg" and not text.lstrip().startswith("<svg"):
        raise SpecError(f"{where}.preview.text must start with <svg")


def _validate_compare(spec: dict) -> None:
    decisions = _objects(spec, "decisions", "spec", 1, 12)
    for d_index, decision in enumerate(decisions):
        where = f"decisions[{d_index}]"
        _ident(decision, where)
        _text(decision, "question", where)
        for key in ("concept", "context", "why_it_matters", "what_teams_do"):
            _text(decision, key, where, required=False)
        options = _objects(decision, "options", where, 2, 6)
        for o_index, option in enumerate(options):
            o_where = f"{where}.options[{o_index}]"
            _ident(option, o_where)
            for key in ("label", "summary", "tradeoffs"):
                _text(option, key, o_where)
            _text(option, "what_goes_wrong", o_where, required=False)
            _validate_preview(option.get("preview"), o_where)
        option_ids = [option["id"] for option in options]
        _unique(option_ids, f"{where}.options")
        recommendation = decision.get("recommendation")
        if not isinstance(recommendation, dict):
            raise SpecError(f"{where}.recommendation must be {{option, reason}}")
        if recommendation.get("option") not in option_ids:
            raise SpecError(
                f"{where}.recommendation.option must name one of {option_ids}"
            )
        _text(recommendation, "reason", f"{where}.recommendation")
    _unique([decision["id"] for decision in decisions], "decisions")


def _validate_gallery(spec: dict) -> None:
    items = _objects(spec, "items", "spec", 1, 500)
    for index, item in enumerate(items):
        where = f"items[{index}]"
        _ident(item, where)
        _text(item, "label", where)
        _text(item, "image", where)
        meta = item.get("meta")
        if meta is not None and not (
            isinstance(meta, dict)
            and all(isinstance(value, (str, int, float)) for value in meta.values())
        ):
            raise SpecError(f"{where}.meta must map names to strings or numbers")
    _unique([item["id"] for item in items], "items")
    verdicts = spec.setdefault("verdicts", list(DEFAULT_VERDICTS))
    if (
        not isinstance(verdicts, list)
        or not 2 <= len(verdicts) <= 6
        or not all(isinstance(v, str) and ID_RE.fullmatch(v) for v in verdicts)
        or len(set(verdicts)) != len(verdicts)
    ):
        raise SpecError("spec.verdicts must be 2-6 unique lowercase words")
    if "questions" in spec:
        questions = _objects(spec, "questions", "spec", 1, 5)
        for index, question in enumerate(questions):
            where = f"questions[{index}]"
            _ident(question, where)
            _text(question, "prompt", where)
            choices = question.get("choices")
            if choices is not None and not (
                isinstance(choices, list)
                and choices
                and all(isinstance(c, str) and c.strip() for c in choices)
            ):
                raise SpecError(f"{where}.choices must be a list of non-empty strings")
        _unique([question["id"] for question in questions], "questions")


def validate_spec(raw: object) -> dict:
    """Return a normalized copy of ``raw`` or raise SpecError."""
    if not isinstance(raw, dict):
        raise SpecError("spec must be a JSON object")
    spec = copy.deepcopy(raw)
    kind = spec.get("kind")
    if kind not in {"compare", "gallery"}:
        raise SpecError("spec.kind must be 'compare' or 'gallery'")
    _ident(spec, "spec")
    _text(spec, "title", "spec")
    for key in ("concept", "context"):
        _text(spec, key, "spec", required=False)
    if kind == "compare":
        _validate_compare(spec)
    else:
        _validate_gallery(spec)
    return spec


def fingerprint(spec: dict) -> str:
    """Stable 16-hex-digit SHA-256 of a normalized spec."""
    canonical = json.dumps(
        spec, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def _data_uri(data: bytes, mime: str) -> str:
    return f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}"


def _embed_image(reference: str, base_dir: Path, where: str) -> str:
    if reference.startswith("data:image/"):
        return reference
    if re.match(r"[a-z]+://", reference):
        raise SpecError(
            f"{where}.image must be a local file; pages never load remote resources"
        )
    path = Path(reference).expanduser()
    if not path.is_absolute():
        path = base_dir / path
    if not path.is_file():
        raise SpecError(f"{where}.image not found: {path}")
    mime = mimetypes.guess_type(path.name)[0] or ""
    if not mime.startswith("image/"):
        raise SpecError(f"{where}.image is not an image file: {path}")
    return _data_uri(path.read_bytes(), mime)


def embed_assets(spec: dict, base_dir: Path) -> dict:
    """Return a copy of a validated spec with images and SVG previews inlined."""
    page = copy.deepcopy(spec)
    if page["kind"] == "gallery":
        for index, item in enumerate(page["items"]):
            item["image"] = _embed_image(item["image"], base_dir, f"items[{index}]")
        return page
    for decision in page["decisions"]:
        for option in decision["options"]:
            preview = option.get("preview")
            if preview and preview["kind"] == "svg":
                svg = preview.pop("text").encode("utf-8")
                preview["src"] = _data_uri(svg, "image/svg+xml")
    return page


def load_spec(spec_path: Path) -> dict:
    try:
        raw = json.loads(spec_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise SpecError(f"cannot read spec: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise SpecError(f"spec is not valid JSON: {exc}") from exc
    return validate_spec(raw)


def load_page_spec(spec_path: Path) -> dict:
    """Validated spec with assets inlined; its fingerprint covers image bytes."""
    return embed_assets(load_spec(spec_path), spec_path.resolve().parent)


def build_html(payload: dict) -> str:
    """Fill the kind's template in one pass so inserted text is never rescanned."""
    spec = payload["spec"]
    template = (TEMPLATES / f"{spec['kind']}.html").read_text(encoding="utf-8")
    parts = {
        "TITLE": html.escape(spec["title"]),
        "PAYLOAD": json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c"),
        "COMMON_CSS": (TEMPLATES / "common.css").read_text(encoding="utf-8"),
        "COMMON_JS": (TEMPLATES / "common.js").read_text(encoding="utf-8"),
    }
    return PLACEHOLDER_RE.sub(lambda m: parts[m.group(1) or m.group(2)], template)


def render_page(spec_path: Path, out_dir: Path) -> Path:
    """Validate, embed, and write ``<out_dir>/<id>.html``; return its path."""
    spec = load_page_spec(spec_path)
    page = build_html({"spec": spec, "fingerprint": fingerprint(spec)})
    if not out_dir.exists():
        # Only a folder this script creates ignores itself; never an existing one.
        out_dir.mkdir(parents=True)
        (out_dir / ".gitignore").write_text("*\n", encoding="utf-8")
    target = out_dir / f"{spec['id']}.html"
    target.write_text(page, encoding="utf-8")
    size = len(page.encode("utf-8"))
    if size > SIZE_WARN_BYTES:
        print(
            f"warning: page is {size // (1024 * 1024)} MB; "
            "shrink images or split the gallery",
            file=sys.stderr,
        )
    return target


def extract_result(text: str) -> dict:
    """Find the result object in a saved file or a Copy-for-chat paste."""
    candidates: list[object] = []
    try:
        candidates.append(json.loads(text))
    except json.JSONDecodeError:
        for block in reversed(FENCE_RE.findall(text)):
            try:
                candidates.append(json.loads(block))
            except json.JSONDecodeError:
                continue
    for candidate in candidates:
        if (
            isinstance(candidate, dict)
            and candidate.get("collaborate_result") == RESULT_VERSION
        ):
            return candidate
    raise ResultError(
        "no collaborate result found; pass the whole Copy-for-chat text "
        "or the saved decisions-<id>.json"
    )


def _allowed(spec: dict) -> dict[str, set[str]]:
    if spec["kind"] == "compare":
        return {
            d["id"]: {o["id"] for o in d["options"]} | {OTHER_CHOICE}
            for d in spec["decisions"]
        }
    return {item["id"]: set(spec["verdicts"]) for item in spec["items"]}


def check_result(result: dict, spec: dict | None = None) -> None:
    """Raise ResultError (StaleResultError for a changed spec) on a bad result."""
    for key in ("id", "kind", "fingerprint", "answers"):
        if key not in result:
            raise ResultError(f"result is missing {key!r}")
    if not isinstance(result["answers"], dict):
        raise ResultError("result.answers must be an object")
    if spec is None:
        return
    if result["id"] != spec["id"]:
        raise ResultError(f"result is for page {result['id']!r}, not {spec['id']!r}")
    if result["fingerprint"] != fingerprint(spec):
        raise StaleResultError(
            "stale result: the page was rendered from a different version of "
            "this spec; re-render and ask again"
        )
    allowed = _allowed(spec)
    field = "choice" if spec["kind"] == "compare" else "verdict"
    for key, answer in result["answers"].items():
        if key not in allowed:
            raise ResultError(f"result answers unknown id {key!r}")
        if not isinstance(answer, dict):
            raise ResultError(f"result answer {key!r} must be an object")
        value = answer.get(field)
        if value is not None and value not in allowed[key]:
            raise ResultError(f"result {key!r} has unknown {field} {value!r}")


def summarize(result: dict, spec: dict | None = None) -> str:
    """Readable decisions for the agent; labels come from the spec when given."""
    answers = result["answers"]
    status = "verified" if spec else "unchecked (pass --spec to verify)"
    lines = [f"page: {result['id']} ({result['kind']}), fingerprint {status}"]
    if result["kind"] == "compare":
        decisions = {d["id"]: d for d in spec["decisions"]} if spec else {}
        for key in list(decisions) or sorted(answers):
            answer = answers.get(key, {})
            decision = decisions.get(key)
            choice = answer.get("choice")
            if choice == OTHER_CHOICE:
                label = "something else (see note)"
            elif decision and choice:
                label = next(
                    o["label"] for o in decision["options"] if o["id"] == choice
                )
            else:
                label = choice or "UNANSWERED"
            note = f" | note: {answer['note']}" if answer.get("note") else ""
            question = decision["question"] if decision else key
            lines.append(f"- {question}: {label}{note}")
    else:
        items = {item["id"]: item for item in spec["items"]} if spec else {}
        for key in list(items) or sorted(answers):
            answer = answers.get(key, {})
            extras = [f"{q}={a}" for q, a in answer.get("answers", {}).items() if a]
            if answer.get("note"):
                extras.append(f"note: {answer['note']}")
            tail = f" | {'; '.join(extras)}" if extras else ""
            label = items[key]["label"] if key in items else key
            lines.append(f"- {label}: {answer.get('verdict') or 'UNANSWERED'}{tail}")
    if result.get("general_note"):
        lines.append(f"general note: {result['general_note']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    render = sub.add_parser("render", help="build a decision page from a JSON spec")
    render.add_argument("spec", type=Path)
    render.add_argument("--out", type=Path, default=DEFAULT_OUT)
    render.add_argument("--no-open", action="store_true", help="skip the browser")
    read = sub.add_parser("read", help="read a saved or pasted result")
    read.add_argument("result", help="saved JSON, a file holding the paste, or -")
    read.add_argument("--spec", type=Path, help="spec the page came from")
    args = parser.parse_args(argv)
    try:
        if args.command == "render":
            target = render_page(args.spec, args.out)
            print(target)
            if not args.no_open:
                webbrowser.open(target.resolve().as_uri())
            return 0
        if args.result == "-":
            text = sys.stdin.read()
        else:
            text = Path(args.result).expanduser().read_text(encoding="utf-8")
        spec = load_page_spec(args.spec) if args.spec else None
        result = extract_result(text)
        check_result(result, spec)
        print(summarize(result, spec))
        return 0
    except StaleResultError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except (SpecError, ResultError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
