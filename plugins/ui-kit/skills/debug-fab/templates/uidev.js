/*
  uidev.js — ui-kit:debug-fab フロートデバッグウィジェット
  See: plugins/ui-kit/skills/debug-fab/SKILL.md

  使い方:
    1. このファイルと uidev.css を 1 回だけ読み込む
    2. 各画面で <body data-debug-files='{...}'> または window.__uidevFiles = {...} で
       関連ファイルを宣言
    3. 右下の FAB (🐛) をクリックすると要素選択モードに入る
    4. 要素を選択して FAB (📋 N) または上部中央の「コピー」ボタンでコピー

  単一画面に複数回ロードしないこと(自動的にスキップする)。
*/

(function () {
  "use strict";

  if (window.__uidevLoaded) return;
  window.__uidevLoaded = true;

  // ── ログリングバッファ ───────────────────────────────────
  const LEVEL_ORDER = { debug: 10, info: 20, warn: 30, error: 40, log: 20 };
  const MAX_BUFFER = 2000;
  const DEFAULT_LINES = 100;
  const DEFAULT_LEVEL = "error";
  const buffer = [];

  function push(level, args) {
    buffer.push({
      ts: new Date().toISOString(),
      level,
      args: args.map((a) => {
        if (typeof a === "string") return a;
        try { return JSON.stringify(a); } catch { return String(a); }
      }),
    });
    if (buffer.length > MAX_BUFFER) buffer.shift();
  }

  ["log", "info", "warn", "error", "debug"].forEach((lv) => {
    const orig = console[lv].bind(console);
    console[lv] = (...args) => { push(lv, args); orig(...args); };
  });

  window.addEventListener("error", (e) =>
    push("error", [`[onerror] ${e.message} @ ${e.filename}:${e.lineno}`]));
  window.addEventListener("unhandledrejection", (e) =>
    push("error", [`[unhandledrejection] ${e.reason}`]));

  // ── 関連ファイル収集 ─────────────────────────────────────
  function collectFiles() {
    const out = { html: [], css: [], js: [] };
    if (window.__uidevFiles && typeof window.__uidevFiles === "object") {
      for (const k of Object.keys(out)) {
        if (Array.isArray(window.__uidevFiles[k])) out[k].push(...window.__uidevFiles[k]);
      }
    }
    document.querySelectorAll("[data-debug-files]").forEach((el) => {
      try {
        const obj = JSON.parse(el.getAttribute("data-debug-files"));
        for (const k of Object.keys(out)) {
          if (Array.isArray(obj[k])) out[k].push(...obj[k]);
        }
      } catch (_) { /* invalid JSON はスキップ */ }
    });
    for (const k of Object.keys(out)) out[k] = [...new Set(out[k])];
    return out;
  }

  // ── ペイロード組立 ────────────────────────────────────────
  function buildPayload(elements) {
    const els = Array.isArray(elements) ? elements : [];
    const minLevel = LEVEL_ORDER[DEFAULT_LEVEL];
    const entries = buffer
      .filter((e) => (LEVEL_ORDER[e.level] ?? 20) >= minLevel)
      .slice(-DEFAULT_LINES);
    return {
      page: location.pathname || "/",
      url: location.href,
      files: collectFiles(),
      logs: { limit: DEFAULT_LINES, level: DEFAULT_LEVEL, entries },
      elements: els.map(describeElement),
      capturedAt: new Date().toISOString(),
    };
  }

  function describeElement(el) {
    const cls = el.className && typeof el.className === "string"
      ? el.className.split(/\s+/).filter(Boolean)
      : [];
    return {
      xpath: shortXPath(el),
      tag: el.tagName,
      id: el.id || null,
      classes: cls,
      text: (el.textContent || "").trim().slice(0, 120),
    };
  }

  // ── クリップボードコピー ──────────────────────────────────
  function legacyCopyText(text) {
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.cssText = "position:fixed;top:0;left:0;opacity:0";
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    try { return document.execCommand("copy"); } finally { ta.remove(); }
  }

  async function copyJSON(payload, btn) {
    const text = JSON.stringify(payload, null, 2);
    try {
      if (navigator.clipboard) {
        await navigator.clipboard.writeText(text);
      } else {
        const ok = legacyCopyText(text);
        if (!ok) throw new Error("execCommand('copy') failed");
      }
      if (btn) {
        const original = btn.innerHTML;
        btn.classList.add("copied");
        btn.innerHTML = "✓ コピーしました";
        setTimeout(() => { btn.classList.remove("copied"); btn.innerHTML = original; }, 1500);
      }
      return true;
    } catch (e) {
      alert("コピーに失敗しました: " + e.message);
      return false;
    }
  }

  // ── XPath 生成(短縮形式・相対) ──────────────────────────
  function shortXPath(el) {
    if (!el || el.nodeType !== 1) return "";
    const segments = [];
    let node = /** @type {Element|null} */ (el);
    while (node && node.nodeType === 1) {
      if (node.id) {
        segments.unshift(`//*[@id="${node.id}"]`);
        return segments.join("/").replace(/^\/\//, "//");
      }
      let i = 1;
      let sib = node.previousElementSibling;
      while (sib) {
        if (sib.tagName === node.tagName) i++;
        sib = sib.previousElementSibling;
      }
      const parent = node.parentElement;
      const hasSameTagSibling = parent
        ? Array.from(parent.children).filter((c) => c.tagName === node.tagName).length > 1
        : false;
      segments.unshift(`${node.tagName.toLowerCase()}${hasSameTagSibling ? `[${i}]` : ""}`);
      node = parent;
    }
    return "/" + segments.join("/");
  }

  // ── トースト通知 ─────────────────────────────────────────
  function showToast(msg) {
    const toast = document.createElement("div");
    toast.className = "uidev-picker-toast";
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 1800);
  }

  // ── DOM 構築 ────────────────────────────────────────────
  function buildDOM() {
    const root = document.createElement("div");
    root.className = "uidev-root";
    root.innerHTML = `
      <div class="uidev-fab" data-pos="bottom-right" title="要素選択モードに入る">🐛</div>
      <div class="uidev-top-bar">
        <button class="uidev-copy-btn" data-uidev="top-copy">📋 コピー</button>
      </div>
    `;
    document.body.appendChild(root);
    return root;
  }

  // ── 要素ピッカー ─────────────────────────────────────────
  let currentSelected = /** @type {Set<Element>} */ (new Set());

  function startPicker(root) {
    const fab = /** @type {HTMLElement} */ (root.querySelector(".uidev-fab"));
    const topCopyBtn = /** @type {HTMLButtonElement} */ (root.querySelector('[data-uidev="top-copy"]'));
    document.body.classList.add("uidev-picker-active");
    fab.setAttribute("data-picker-active", "true");
    currentSelected = new Set();

    function refreshFab() {
      const n = currentSelected.size;
      fab.innerHTML = n > 0 ? `📋 ${n}` : "📋";
      fab.title = n > 0
        ? `選択中 ${n} 件 — クリックで JSON コピー`
        : "要素を 1 つ以上選択してください";
    }

    let hovered = /** @type {Element|null} */ (null);

    function clearHover() {
      if (hovered && !currentSelected.has(hovered)) hovered.classList.remove("uidev-picker-highlight");
      hovered = null;
    }

    function onMove(e) {
      const el = /** @type {Element} */ (e.target);
      if (!el || el === fab || fab.contains(el) || el === topCopyBtn || topCopyBtn.contains(el)) return;
      if (hovered !== el) {
        clearHover();
        hovered = el;
        if (!currentSelected.has(el)) el.classList.add("uidev-picker-highlight");
      }
    }

    async function onClick(e) {
      const el = /** @type {Element} */ (e.target);
      if (!el) return;

      // 上部コピーボタンは通常のイベントに任せる
      if (el === topCopyBtn || topCopyBtn.contains(el)) return;

      // FAB クリック → コピーして終了
      if (el === fab || fab.contains(el)) {
        e.preventDefault();
        e.stopPropagation();
        if (currentSelected.size === 0) return;
        const ok = await copyJSON(buildPayload(Array.from(currentSelected)));
        if (ok) showToast(`✓ ${currentSelected.size} 件の要素 + files + logs を JSON でコピーしました`);
        stop();
        return;
      }

      e.preventDefault();
      e.stopPropagation();

      // トグル選択
      if (currentSelected.has(el)) {
        currentSelected.delete(el);
        el.classList.remove("uidev-picker-selected");
      } else {
        currentSelected.add(el);
        el.classList.remove("uidev-picker-highlight");
        el.classList.add("uidev-picker-selected");
      }
      refreshFab();
    }

    function onKey(e) {
      if (e.key === "Escape") {
        e.preventDefault();
        stop();
      }
    }

    function stop() {
      clearHover();
      currentSelected.forEach((el) => el.classList.remove("uidev-picker-selected"));
      currentSelected.clear();
      document.body.classList.remove("uidev-picker-active");
      fab.removeAttribute("data-picker-active");
      fab.innerHTML = "🐛";
      fab.title = "要素選択モードに入る";
      topCopyBtn.removeEventListener("click", onTopCopy);
      document.removeEventListener("mousemove", onMove, true);
      document.removeEventListener("click", onClick, true);
      document.removeEventListener("keydown", onKey, true);
    }

    async function onTopCopy() {
      const ok = await copyJSON(buildPayload(Array.from(currentSelected)), topCopyBtn);
      if (ok && currentSelected.size > 0) {
        showToast(`✓ ${currentSelected.size} 件の要素 + files + logs を JSON でコピーしました`);
      }
      stop();
    }

    topCopyBtn.addEventListener("click", onTopCopy);
    refreshFab();
    document.addEventListener("mousemove", onMove, true);
    document.addEventListener("click", onClick, true);
    document.addEventListener("keydown", onKey, true);
  }

  // ── 起動 ───────────────────────────────────────────────
  function init() {
    const root = buildDOM();
    const fab = /** @type {HTMLElement} */ (root.querySelector(".uidev-fab"));
    const topCopyBtn = /** @type {HTMLButtonElement} */ (root.querySelector('[data-uidev="top-copy"]'));

    fab.addEventListener("click", () => {
      if (!fab.hasAttribute("data-picker-active")) {
        startPicker(root);
      }
    });

  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
