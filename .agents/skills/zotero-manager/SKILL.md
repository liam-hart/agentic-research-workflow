---
name: zotero-manager
description: "Manage Zotero discovery, metadata, attachments, missing-evidence diagnosis, and MinerU acquisition or synchronization. Use when the user must find or repair a library item or determine whether local evidence exists; route complete source ingestion to LLM Wiki `$ingest`."
---

# Zotero Manager

Use this skill to discover Zotero items, verify metadata, resolve attachments, diagnose whether local MinerU evidence exists, and coordinate evidence acquisition or synchronization. It does not ingest or certify source notes.

## Guidelines

1. **Resolve identity and evidence state**:
   - Match citekey, Zotero parent key, DOI, normalized title, year, and creators before treating records as the same source.
   - Check verified local LLM Wiki source notes first, then the reference-trimmed local MinerU mirror.
   - When evidence is missing, resolve the Zotero parent and markdown attachment, diagnose acquisition state, and coordinate MinerU generation or sync.
   - Stop before synthesis. “Ingest the next paper” routes directly to the LLM Wiki `$ingest` skill and its exactly-one-paper immutable packet workflow. Do not activate or use `zotero-manager` as a companion for that request; `$ingest` owns its own identity and evidence preflight.

2. **Zotero Search Preference**:
   - Force all search operations to prioritize `.md` files in the `.raw/zotero/` folders rather than calling expensive, slow PDF text retrieval tools.

3. **Maintenance boundary**:
   - Metadata repair, attachment linking, index refreshes, and missing-evidence diagnosis are in scope. Source-note drafting, semantic fidelity certification, construct promotion, and multi-paper batch audits are not.

4. **Discovery**:
   - Semantic search may identify related library items, but discovery results are candidates rather than evidence. Confirm claims against local full text before synthesis.

5. **Save-time abstract highlighting** (human workflow; remind when coaching intake):
   - At save, highlight the abstract sentence(s) that motivated keeping the paper.
   - Yellow for the triggering claim/finding; Purple if the trigger is a personal research idea.
   - Full rule: your project's reading-and-notes workflow note.

6. **Linter and sync**:
   - Use current repository scripts and authorities for abstract linting and synchronization. This skill does not carry schedule or command authority.

## Verification

- Records treated as the same source match on citekey, Zotero parent key, DOI, normalized title, year, and creators.
- Whether local evidence exists is stated from what was read, not assumed.
- Discovery results are labelled as candidates until confirmed against local full text.
- Nothing was ingested, drafted, or certified here.
