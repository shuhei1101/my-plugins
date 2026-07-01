/* ============================================================================
 * my-plugins docs 共通スクリプト
 *
 * docs/ 配下すべてのページで読み込む単一 JS。
 * 各機能は「対象 DOM が無ければ何もしない」形で並べており、
 * Mock demo / Jekyll 描画ページ / Wiki など、ページ種別を問わず同じファイルで動く。
 *
 * Markdown → HTML の変換は Jekyll 側で完了しているので、ここでは行わない。
 *
 * 提供する機能:
 *   1. パンくずリスト  ... [data-breadcrumb] があれば URL 階層から自動生成
 *   2. テーブルソート  ... table にヘッダクリックで昇降ソートを付与
 *   3. テーブルフィルタ ... table 上部に検索ボックスを差し込み行を絞り込み
 *   4. トップに戻る    ... [data-back-to-top] のボタンをスクロール量で表示切替
 *   5. Mock demo 用    ... 検索・行クリック・新規追加・編集モード・トースト
 * ============================================================================ */

/* ---------- 定数 ---------- */
const TOAST_DISPLAY_MS = 1800;
const BACK_TO_TOP_THRESHOLD_PX = 300;

/* パンくず階層のラベル辞書。URL セグメント → 表示名。未登録は素通し。 */
const BREADCRUMB_LABELS = {
  "": "トップ",
  "docs": "ドキュメント",
  "mock": "モック",
  "wiki": "Wiki",
  "pages": "画面",
  "components": "コンポーネント",
  "styles": "スタイル",
  "issues": "Issue",
  "assets": "アセット",
  "gh-kit": "gh-kit",
  "テンプレート": "テンプレート",
  "規約": "規約",
};


/* ============================================================================
 * 1. パンくずリスト
 * ---------------------------------------------------------------------------- */

/** ルート（末尾スラッシュ付き）とパス配下のセグメントに分割する */
function splitPathBySiteRoot() {
  // _layouts/default.html が data-site-root="{{ '/' | relative_url }}" を注入する
  // GitHub Pages（project pages）だと "/my-plugins/"、ローカルルート配信だと "/"
  const bodyRoot = document.body?.dataset?.siteRoot || "/";
  const siteRoot = bodyRoot.endsWith("/") ? bodyRoot : bodyRoot + "/";

  const pathname = decodeURIComponent(window.location.pathname);
  // 末尾のファイル名を落として必ずディレクトリ形にする
  const dir = pathname.endsWith("/") ? pathname : pathname.replace(/\/[^\/]*$/, "/");

  // site root 直下の相対パスを取り出す
  const rel = dir.startsWith(siteRoot) ? dir.slice(siteRoot.length) : dir.replace(/^\//, "");
  const segs = rel.split("/").filter(Boolean);
  return { siteRoot, segs };
}

/** その中間層セグメントを「非リンクの中間表示」にするかどうか */
function isNonLinkableSegment(seg, index, segs) {
  // pages/{画面名}/issues/ は index.md を置かない中間層（規約）→ リンクにしない
  return seg === "issues" && segs[index - 2] === "pages";
}

/** URL パスの各セグメントを辿ってパンくずリンクを組み立てる */
function buildBreadcrumb() {
  const host = document.querySelector("[data-breadcrumb]");
  if (!host) return;

  const { siteRoot, segs } = splitPathBySiteRoot();

  const parts = [];
  parts.push(`<a href="${siteRoot}">${BREADCRUMB_LABELS[""]}</a>`);

  // 各セグメントの累積 URL を絶対パス（site root からの絶対）で組む
  let acc = siteRoot;
  segs.forEach((seg, i) => {
    acc += seg + "/";
    const label = BREADCRUMB_LABELS[seg] || seg;
    const isLast = i === segs.length - 1;
    parts.push(`<span class="sep">/</span>`);
    if (isLast || isNonLinkableSegment(seg, i, segs)) {
      // 現在地 or 中間層 → リンクにしない
      parts.push(`<span class="current">${label}</span>`);
    } else {
      parts.push(`<a href="${acc}">${label}</a>`);
    }
  });

  host.innerHTML = parts.join("");
}


/* ============================================================================
 * 2-3. テーブルソート・フィルタ
 * ---------------------------------------------------------------------------- */

/** 指定スコープ内のテーブルにソートとフィルタを付与する */
function enhanceTables(scope) {
  scope.querySelectorAll("table").forEach((table) => {
    // 二重適用防止
    if (table.dataset.enhanced === "true") return;
    table.dataset.enhanced = "true";
    bindTableSort(table);
    injectTableFilter(table);
  });
}

/** テーブルヘッダをクリックで昇降ソートできるようにする */
function bindTableSort(table) {
  const thead = table.tHead;
  const tbody = table.tBodies[0];
  if (!thead || !tbody) return;

  Array.from(thead.rows[0].cells).forEach((th, colIdx) => {
    th.classList.add("sortable");
    th.addEventListener("click", () => {
      // 現状の方向を判定して反転（初回は昇順）
      const asc = !th.classList.contains("sort-asc");
      // 他のヘッダの矢印はクリア
      Array.from(thead.rows[0].cells).forEach((h) => h.classList.remove("sort-asc", "sort-desc"));
      th.classList.add(asc ? "sort-asc" : "sort-desc");

      const rows = Array.from(tbody.rows);
      rows.sort((a, b) => compareCells(a.cells[colIdx], b.cells[colIdx], asc));
      rows.forEach((row) => tbody.appendChild(row));
    });
  });
}

/** セル内容を数値優先で比較する */
function compareCells(a, b, asc) {
  const av = (a?.textContent || "").trim();
  const bv = (b?.textContent || "").trim();
  const an = Number(av);
  const bn = Number(bv);
  let result;
  if (!Number.isNaN(an) && !Number.isNaN(bn) && av !== "" && bv !== "") {
    result = an - bn;
  } else {
    result = av.localeCompare(bv, "ja");
  }
  return asc ? result : -result;
}

/** テーブル上に検索ボックスを挿入し、入力語で行を絞り込む */
function injectTableFilter(table) {
  const tbody = table.tBodies[0];
  if (!tbody || tbody.rows.length < 2) return; // 行が少なければフィルタ不要

  const input = document.createElement("input");
  input.type = "search";
  input.className = "table-filter";
  input.placeholder = "この表を絞り込む...";
  table.parentNode.insertBefore(input, table);

  input.addEventListener("input", () => {
    const keyword = input.value.trim().toLowerCase();
    Array.from(tbody.rows).forEach((row) => {
      const text = row.textContent.toLowerCase();
      row.classList.toggle("hidden", keyword !== "" && !text.includes(keyword));
    });
  });
}


/* ============================================================================
 * 4. トップに戻るボタン
 * ---------------------------------------------------------------------------- */

/** スクロール量で表示切替し、クリックで先頭へスムーズスクロール */
function bindBackToTop() {
  const btn = document.querySelector("[data-back-to-top]");
  if (!btn) return;

  const update = () => {
    btn.classList.toggle("visible", window.scrollY > BACK_TO_TOP_THRESHOLD_PX);
  };
  window.addEventListener("scroll", update, { passive: true });
  update();

  btn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}


/* ============================================================================
 * 5. Mock demo 用ハンドラ
 * 対象 DOM が無いページでは何もしない（早期 return）。
 * ---------------------------------------------------------------------------- */

/** 検索ボックスの入力語で顧客一覧の行を絞り込む */
function bindSearchFilter() {
  const input = document.getElementById("search");
  if (!input) return;
  input.addEventListener("input", () => {
    const keyword = input.value.trim().toLowerCase();
    document.querySelectorAll("#customer-table tbody tr").forEach((row) => {
      const text = row.textContent.toLowerCase();
      row.classList.toggle("hidden", keyword !== "" && !text.includes(keyword));
    });
  });
}

/** 行クリックで疑似遷移トーストを表示する */
function bindRowClick() {
  document.querySelectorAll("#customer-table tbody tr").forEach((row) => {
    row.addEventListener("click", (event) => {
      if (event.target instanceof HTMLInputElement) return;
      const id = row.dataset.id;
      showToast(`顧客 ${id} を選択しました（モック）`);
    });
  });
}

/** 新規追加ボタンでトーストを一時表示する */
function bindNewButton() {
  const button = document.getElementById("new-btn");
  if (!button) return;
  button.addEventListener("click", () => {
    showToast("新規追加ダイアログを開きました（モック）");
  });
}

/** 詳細画面の編集モードを切り替える */
function bindEditMode() {
  const editBtn = document.getElementById("edit-btn");
  const cancelBtn = document.getElementById("cancel-btn");
  const saveBtn = document.getElementById("save-btn");
  if (!editBtn || !cancelBtn || !saveBtn) return;

  /** 編集可能フィールドの readonly 属性を切り替える */
  function setEditing(editing) {
    document.querySelectorAll(".field-value input, .field-value textarea").forEach((field) => {
      if (editing) field.removeAttribute("readonly");
      else field.setAttribute("readonly", "readonly");
    });
    editBtn.hidden = editing;
    cancelBtn.hidden = !editing;
    saveBtn.hidden = !editing;
  }

  editBtn.addEventListener("click", () => setEditing(true));
  cancelBtn.addEventListener("click", () => setEditing(false));
  saveBtn.addEventListener("click", () => {
    setEditing(false);
    showToast("変更を保存しました（モック）");
  });
}

/** 画面下部のトーストを一定時間表示する */
function showToast(message) {
  const toast = document.getElementById("toast");
  if (!toast) return;
  toast.textContent = message;
  toast.hidden = false;
  window.clearTimeout(showToast._timer);
  showToast._timer = window.setTimeout(() => {
    toast.hidden = true;
  }, TOAST_DISPLAY_MS);
}


/* ============================================================================
 * エントリポイント
 * ---------------------------------------------------------------------------- */

function init() {
  // 共通機能
  buildBreadcrumb();
  bindBackToTop();
  enhanceTables(document);

  // Mock demo 固有のハンドラ
  bindSearchFilter();
  bindRowClick();
  bindNewButton();
  bindEditMode();
}

document.addEventListener("DOMContentLoaded", init);
