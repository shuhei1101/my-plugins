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
    const out = { html: [], css: [], js: [], backend: [], other: [] };
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
    const groups = [["html","HTML"],["css","CSS"],["js","JS"],["backend","Backend"],["other","Other"]];
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

  // ── コピー処理 ─────────────────────────────────────────
  async function copyDebugJSON(root) {
    const lines = parseInt(getS("lines"), 10) || DEFAULTS.lines;
    const minLevel = LEVEL_ORDER[getS("level")] ?? LEVEL_ORDER[DEFAULTS.level];
    const entries = buffer.filter((e) => (LEVEL_ORDER[e.level] ?? 20) >= minLevel).slice(-lines);

    const payload = {
      page: location.pathname || "/",
      url:  location.href,
      files: collectFiles(),
      logs: { limit: lines, level: getS("level"), entries: entries },
      capturedAt: new Date().toISOString(),
    };
    const text = JSON.stringify(payload, null, 2);
    const btn = root.querySelector('[data-uidev="copy"]');
    try {
      await navigator.clipboard.writeText(text);
      const original = btn.innerHTML;
      btn.classList.add("copied");
      btn.innerHTML = "✓ コピーしました";
      setTimeout(() => { btn.classList.remove("copied"); btn.innerHTML = original; }, 1500);
    } catch (e) {
      alert("コピーに失敗しました: " + e.message);
    }
  }

  // ── 起動 ───────────────────────────────────────────────
  function init() {
    const root = buildDOM();
    const fab       = root.querySelector(".uidev-fab");
    const backdrop  = root.querySelector(".uidev-modal-backdrop");
    const closeBtn  = root.querySelector('[data-uidev="close"]');
    const copyBtn   = root.querySelector('[data-uidev="copy"]');
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
