// Shared runtime for collaborate decision pages. Each page supplies progress and
// summary hooks; everything here is kind-agnostic. Spec text is only ever set as
// textContent, never parsed as HTML.
const PAYLOAD = JSON.parse(document.getElementById("payload").textContent);
const SPEC = PAYLOAD.spec;
const STORE_KEY = `collaborate:${SPEC.id}:${PAYLOAD.fingerprint}`;

function el(tag, props = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(props)) {
    if (value === undefined || value === null || value === false) continue;
    if (key === "class") node.className = value;
    else if (key === "text") node.textContent = value;
    else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
    else node.setAttribute(key, value === true ? "" : value);
  }
  for (const child of children.flat(Infinity)) {
    if (child === null || child === undefined || child === false) continue;
    node.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
  return node;
}

function loadState() {
  try {
    return JSON.parse(localStorage.getItem(STORE_KEY)) || {};
  } catch (error) {
    return {};
  }
}

function saveState(state) {
  try {
    localStorage.setItem(STORE_KEY, JSON.stringify(state));
  } catch (error) {
    // Storage blocked: answers live in memory until the page closes.
  }
}

function toast(message) {
  const node = el("div", { class: "toast", role: "status", text: message });
  document.body.append(node);
  setTimeout(() => node.remove(), 2600);
}

function buildResult(state) {
  return {
    collaborate_result: 1,
    id: SPEC.id,
    kind: SPEC.kind,
    fingerprint: PAYLOAD.fingerprint,
    title: SPEC.title,
    answers: state.answers || {},
    general_note: state.general_note || "",
  };
}

function resultText(state, summaryLines) {
  const lines = [`## Decisions: ${SPEC.title}`, "", ...summaryLines];
  if (state.general_note) lines.push("", `General note: ${state.general_note}`);
  lines.push("", "```json", JSON.stringify(buildResult(state), null, 2), "```");
  return lines.join("\n");
}

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (error) {
    const area = el("textarea", { class: "offscreen" });
    area.value = text;
    document.body.append(area);
    area.select();
    const ok = document.execCommand("copy");
    area.remove();
    return ok;
  }
}

function saveFile(state) {
  const json = JSON.stringify(buildResult(state), null, 2);
  const url = URL.createObjectURL(new Blob([json], { type: "application/json" }));
  const link = el("a", { href: url, download: `decisions-${SPEC.id}.json` });
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function mountHeader() {
  document.getElementById("app").append(
    el("header", {},
      el("h1", { text: SPEC.title }),
      SPEC.concept ? el("p", { class: "concept" }, "Concept: ", el("strong", { text: SPEC.concept })) : null,
      SPEC.context ? el("p", { class: "context", text: SPEC.context }) : null));
}

// hooks.progress(state) -> [done, total]; hooks.summary(state) -> Markdown lines.
function mountToolbar(state, hooks) {
  const counter = el("span", { class: "progress" });
  const note = el("textarea", { rows: 2, placeholder: "Anything else the agent should know (optional)" });
  note.value = state.general_note || "";
  note.addEventListener("input", () => {
    state.general_note = note.value;
    saveState(state);
  });
  const copyButton = el("button", {
    type: "button",
    class: "primary",
    onclick: async () => {
      const ok = await copyText(resultText(state, hooks.summary(state)));
      toast(ok ? "Copied. Paste it into the chat." : "Copy failed. Use Save file instead.");
    },
  }, "Copy for chat");
  const saveButton = el("button", {
    type: "button",
    onclick: () => {
      saveFile(state);
      toast(`Saved decisions-${SPEC.id}.json (check Downloads).`);
    },
  }, "Save file");
  document.body.append(
    el("footer", { class: "toolbar" }, note, el("div", { class: "actions" }, counter, saveButton, copyButton)));
  const refresh = () => {
    const [done, total] = hooks.progress(state);
    counter.textContent = `${done} of ${total} answered`;
  };
  refresh();
  return refresh;
}
