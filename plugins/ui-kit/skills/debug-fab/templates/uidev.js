/*
  uidev.js — dev-kit:ui-dev フロートデバッグウィジェット
  See: plugins/dev-kit/skills/ui-dev/SKILL.md

  使い方:
    1. このファイルと uidev.css を 1 回だけ読み込む
    2. 各画面で <body data-debug-files='{...}'> または window.__uidevFiles = {...} で
       関連ファイルを宣言
    3. 自動でフロートボタン + モーダルが画面に挿入される
    4. Ctrl+Shift+D でも開閉可能

  単一画面に複数回ロードしないこと(自動的にスキップする)。
*/

(function () {
  "use strict";

  if (window.__uidevLoaded) return;
  window.__uidevLoaded = true;

  // ── ストレージキー ───────────────────────────────────────
  const LS = { lines: "uidev.lines", level: "uidev.level", pos: "uidev.pos" };
  const DEFAULTS = { lines: 100, level: "error", pos: "bottom-right" };
  const getS = (k) => localStorage.getItem(LS[k]) ?? DEFAULTS[k];
  const setS = (k, v) => localStorage.setItem(LS[k], v);

  // ── ログリングバッファ ───────────────────────────────────
  const LEVEL_ORDER = { debug: 10, info: 20, warn: 30, error: 40, log: 20 };
  const MAX_BUFFER = 2000;
  const buffer = [];

  function push(level, args) {
    buffer.push({
      ts: new Date().toISOString(),
      level: level,
      args: args.map((a) => {
        if (typeof a === "string") return a;
        try { return JSON.stringify(a); } catch { return String(a); }
      }),
    });
    if (buffer.length > MAX_BUFFER) buffer.shift();
  }

  // console フック(uidev.js 読み込み後の console 呼び出しを全て収集)
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

  // ── DOM 構築 ────────────────────────────────────────────
  function buildDOM() {
    const root = document.createElement("div");
    root.className = "uidev-root";
    root.innerHTML = `
      <div class="uidev-fab" data-pos="${getS("pos")}" title="開発デバッグパネルを開く">🐛</div>
      <div class="uidev-modal-backdrop" data-open="false">
        <div class="uidev-modal" role="dialog" aria-modal="true">
          <header>
            <div class="title">
              <span>ui-dev デバッグパネル</span>
              <span class="badge">dev-kit:ui-dev</span>
            </div>
            <div class="pos-field">
              <span>ボタン位置</span>
              <select data-uidev="pos">
                <option value="bottom-right">右下</option>
                <option value="bottom-left">左下</option>
                <option value="top-right">右上</option>
                <option value="top-left">左上</option>
              </select>
            </div>
            <button class="pick" data-uidev="pick" title="要素ピッカーモードに入る(クリックで XPath + URL を JSON コピー)">🎯 要素選択</button>
            <button class="copy" data-uidev="copy" title="関連ファイル情報 + 直近 N 行ログを JSON でコピー">📋 コピー</button>
            <button class="close" data-uidev="close" aria-label="閉じる">×</button>
          </header>
          <div class="uidev-body">
            <section>
              <div class="section-head"><h3>概要</h3></div>
              <div class="uidev-info-card">
                <div class="row"><div class="key">page</div><div class="val" data-uidev="page"></div></div>
                <div class="row"><div class="key">url</div><div class="val" data-uidev="url"></div></div>
              </div>
            </section>
            <section>
              <div class="section-head"><h3>関連ファイル</h3></div>
              <div class="uidev-files" data-uidev="files"></div>
              <div class="uidev-setting-hint">画面側で <code>data-debug-files</code> 属性または <code>window.__uidevFiles</code> で明示登録します。</div>
            </section>
            <section>
              <div class="section-head">
                <h3>直近ログ</h3>
                <span class="count" data-uidev="log-count"></span>
                <div class="controls">
                  <div class="inline-field">
                    <span>レベル</span>
                    <select data-uidev="level">
                      <option value="error">エラー以上</option>
                      <option value="warn">警告以上</option>
                      <option value="info">情報以上</option>
                      <option value="debug">デバッグ以上</option>
                    </select>
                  </div>
                  <div class="inline-field">
                    <span>行数</span>
                    <input type="number" data-uidev="lines" min="10" max="2000" step="10" value="100" />
                  </div>
                </div>
              </div>
              <div class="uidev-logs" data-uidev="logs"></div>
              <div class="uidev-setting-hint">バッファは全レベル収集、表示・コピーはこのフィルタで絞り込みます。</div>
            </section>
            <section>
              <div class="section-head">
                <h3>要素ピッカー</h3>
              </div>
              <div class="uidev-setting-hint">
                ヘッダの「🎯 要素選択」を押すと、モーダルが一時非表示になり要素ピッカーモードに入る。
                <strong>クリックで複数選択(再クリックで解除)</strong>、画面右下の <strong>🐛 → 📋 N</strong> ボタンを押すと
                通常の JSON コピー(files + logs)に <code>elements: [...]</code> を加えてクリップボードへ。
                <kbd>Esc</kbd> でキャンセル。XPath は短縮形式(相対)で固定。
              </div>
            </section>
          </div>
          <div class="uidev-footer-hint">
            <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>D</kbd> でも開閉できます。コピーした JSON はそのまま Claude Code に貼り付けてデバッグ可能です。
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(root);
    return root;
  }

  // ── レンダリング ───────────────────────────────────────
  function getFilteredLogs() {
    const lines = parseInt(getS("lines"), 10) || DEFAULTS.lines;
    const minLevel = LEVEL_ORDER[getS("level")] ?? LEVEL_ORDER[DEFAULTS.level];
    return buffer.filter((e) => (LEVEL_ORDER[e.level] ?? 20) >= minLevel).slice(-lines);
  }

  function renderOverview(root) {
    root.querySelector('[data-uidev="page"]').textContent = location.pathname || "/";
    root.querySelector('[data-uidev="url"]').textContent  = location.href;

    const files = collectFiles();
    const wrap = root.querySelector('[data-uidev="files"]');
    wrap.innerHTML = "";
    const groups = [["html","HTML"],["css","CSS"],["js","JS"]];
    let hasAny = false;
    groups.forEach(([k, lbl]) => {
      if (!files[k].length) return;
      hasAny = true;
      const g = document.createElement("div");
      g.className = "group";
      g.innerHTML = `<div class="label">${lbl} <span class="tag">${files[k].length}</span></div>
        <ul>${files[k].map((f) => `<li>${escapeHTML(f)}</li>`).join("")}</ul>`;
      wrap.appendChild(g);
    });
    if (!hasAny) {
      wrap.innerHTML = '';
      const empty = document.createElement("div");
      empty.className = "uidev-files-empty";
      empty.innerHTML = '登録されたファイルがありません。<code>data-debug-files</code> 属性または <code>window.__uidevFiles</code> で登録してください。';
      wrap.appendChild(empty);
    }
  }

  function renderLogs(root) {
    const logs = getFilteredLogs();
    const wrap = root.querySelector('[data-uidev="logs"]');
    root.querySelector('[data-uidev="log-count"]').textContent = `(${logs.length} / バッファ ${buffer.length})`;
    if (!logs.length) {
      wrap.innerHTML = '<div class="empty">該当ログなし(現在の出力レベルでは表示対象なし)</div>';
      return;
    }
    wrap.innerHTML = logs.map((e) => {
      const t = e.ts.slice(11, 23);
      return `<div class="row" data-level="${e.level}">
        <div class="ts">${t}</div>
        <div class="level">${e.level}</div>
        <div class="msg">${escapeHTML(e.args.join(" "))}</div>
      </div>`;
    }).join("");
    wrap.scrollTop = wrap.scrollHeight;
  }

  function escapeHTML(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({
      "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"
    })[c]);
  }

  // ── ペイロード組立(共通) ─────────────────────────────
  /**
   * @param {Element[]} [elements] 要素ピッカーで選択された要素配列(なければ空)
   */
  function buildPayload(elements) {
    const els = Array.isArray(elements) ? elements : [];
    const lines = parseInt(getS("lines"), 10) || DEFAULTS.lines;
    const minLevel = LEVEL_ORDER[getS("level")] ?? LEVEL_ORDER[DEFAULTS.level];
    const entries = buffer.filter((e) => (LEVEL_ORDER[e.level] ?? 20) >= minLevel).slice(-lines);

    return {
      page: location.pathname || "/",
      url:  location.href,
      files: collectFiles(),
      logs: { limit: lines, level: getS("level"), entries: entries },
      elements: els.map(describeElement),
      capturedAt: new Date().toISOString(),
    };
  }

  /** @param {Element} el */
  function describeElement(el) {
    const cls = el.className && typeof el.className === "string"
      ? el.className.split(/\s+/).filter(Boolean)
      : [];
    return {
      xpath:   shortXPath(el),
      tag:     el.tagName,
      id:      el.id || null,
      classes: cls,
      text:    (el.textContent || "").trim().slice(0, 120),
    };
  }

  /** @param {string} text  非セキュアコンテキスト(HTTP)でも動く execCommand フォールバック */
  function legacyCopyText(text) {
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.cssText = "position:fixed;top:0;left:0;opacity:0";
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    try {
      return document.execCommand("copy");
    } finally {
      ta.remove();
    }
  }

  /** @param {Element} target  クリップボードにコピーしフィードバック表示 */
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

  async function copyDebugJSON(root) {
    const btn = root.querySelector('[data-uidev="copy"]');
    await copyJSON(buildPayload([]), btn);
  }

  // ── XPath 生成(短縮形式・相対) ──────────────────────────
  /** @param {Element} el  short XPath: 直近の id を起点に */
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

  // ── 要素ピッカー(多選択 + FAB コピー) ─────────────────
  /** @param {ReturnType<typeof buildDOM>} root */
  function startPicker(root) {
    const backdrop = root.querySelector(".uidev-modal-backdrop");
    const fab      = /** @type {HTMLElement} */ (root.querySelector(".uidev-fab"));
    const originalFabHTML  = fab.innerHTML;
    const originalFabTitle = fab.title;
    const wasOpen = backdrop.getAttribute("data-open") === "true";
    backdrop.setAttribute("data-open", "false");
    document.body.classList.add("uidev-picker-active");
    fab.setAttribute("data-picker-active", "true");

    const hint = document.createElement("div");
    hint.className = "uidev-picker-hint";
    hint.innerHTML = `要素ピッカーモード — クリックで複数選択(再クリックで解除) / 右下のボタンでコピー / <kbd>Esc</kbd> でキャンセル`;
    document.body.appendChild(hint);

    const selected = /** @type {Set<Element>} */ (new Set());
    let hovered = /** @type {Element|null} */ (null);

    function clearHover() {
      if (hovered && !selected.has(hovered)) hovered.classList.remove("uidev-picker-highlight");
      hovered = null;
    }

    function refreshFab() {
      const n = selected.size;
      fab.innerHTML = n > 0 ? `📋 ${n}` : "📋";
      fab.title = n > 0 ? `選択中 ${n} 件 — クリックで JSON コピー` : "要素を 1 つ以上選択してください";
    }

    /** @param {MouseEvent} e */
    function onMove(e) {
      const el = /** @type {Element} */ (e.target);
      if (!el || el === hint || hint.contains(el) || el === fab || fab.contains(el)) return;
      if (hovered !== el) {
        clearHover();
        hovered = el;
        if (!selected.has(el)) el.classList.add("uidev-picker-highlight");
      }
    }

    /** @param {MouseEvent} e */
    async function onClick(e) {
      const el = /** @type {Element} */ (e.target);
      if (!el) return;

      // FAB クリック → コピーして終了
      if (el === fab || fab.contains(el)) {
        e.preventDefault();
        e.stopPropagation();
        if (selected.size === 0) {
          flashHint("要素を 1 つ以上選択してください");
          return;
        }
        const ok = await copyJSON(buildPayload(Array.from(selected)));
        if (ok) {
          const toast = document.createElement("div");
          toast.className = "uidev-picker-toast";
          toast.textContent = `✓ ${selected.size} 件の要素 + files + logs を JSON でコピーしました`;
          document.body.appendChild(toast);
          setTimeout(() => toast.remove(), 1800);
        }
        stop();
        if (wasOpen) backdrop.setAttribute("data-open", "true");
        return;
      }

      // hint をクリックされた場合は無視
      if (el === hint || hint.contains(el)) return;

      e.preventDefault();
      e.stopPropagation();

      // トグル選択
      if (selected.has(el)) {
        selected.delete(el);
        el.classList.remove("uidev-picker-selected");
      } else {
        selected.add(el);
        el.classList.remove("uidev-picker-highlight");
        el.classList.add("uidev-picker-selected");
      }
      refreshFab();
    }

    function flashHint(msg) {
      const original = hint.innerHTML;
      hint.innerHTML = msg;
      setTimeout(() => { hint.innerHTML = original; }, 1200);
    }

    function onKey(e) {
      if (e.key === "Escape") {
        e.preventDefault();
        stop();
        if (wasOpen) backdrop.setAttribute("data-open", "true");
      }
    }

    function stop() {
      clearHover();
      selected.forEach((el) => el.classList.remove("uidev-picker-selected"));
      selected.clear();
      document.body.classList.remove("uidev-picker-active");
      fab.removeAttribute("data-picker-active");
      fab.innerHTML = originalFabHTML;
      fab.title = originalFabTitle;
      hint.remove();
      document.removeEventListener("mousemove", onMove, true);
      document.removeEventListener("click", onClick, true);
      document.removeEventListener("keydown", onKey, true);
    }

    refreshFab();
    document.addEventListener("mousemove", onMove, true);
    document.addEventListener("click", onClick, true);
    document.addEventListener("keydown", onKey, true);
  }

  // ── 起動 ───────────────────────────────────────────────
  function init() {
    const root = buildDOM();
    const fab       = root.querySelector(".uidev-fab");
    const backdrop  = root.querySelector(".uidev-modal-backdrop");
    const closeBtn  = root.querySelector('[data-uidev="close"]');
    const copyBtn   = root.querySelector('[data-uidev="copy"]');
    const pickBtn   = root.querySelector('[data-uidev="pick"]');
    const linesEl   = root.querySelector('[data-uidev="lines"]');
    const levelEl   = root.querySelector('[data-uidev="level"]');
    const posEl     = root.querySelector('[data-uidev="pos"]');

    linesEl.value = getS("lines");
    levelEl.value = getS("level");
    posEl.value   = getS("pos");

    function openModal()  { backdrop.setAttribute("data-open", "true");  renderOverview(root); renderLogs(root); }
    function closeModal() { backdrop.setAttribute("data-open", "false"); }

    fab.addEventListener("click", openModal);
    closeBtn.addEventListener("click", closeModal);
    backdrop.addEventListener("click", (e) => { if (e.target === backdrop) closeModal(); });
    copyBtn.addEventListener("click", () => copyDebugJSON(root));
    pickBtn.addEventListener("click", () => startPicker(root));
    linesEl.addEventListener("change", () => { setS("lines", linesEl.value); renderLogs(root); });
    levelEl.addEventListener("change", () => { setS("level", levelEl.value); renderLogs(root); });
    posEl.addEventListener("change",   () => { setS("pos",   posEl.value);   fab.setAttribute("data-pos", posEl.value); });

    document.addEventListener("keydown", (e) => {
      if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === "d") {
        e.preventDefault();
        if (backdrop.getAttribute("data-open") === "true") closeModal(); else openModal();
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
