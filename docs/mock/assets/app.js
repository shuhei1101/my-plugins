const TOAST_DISPLAY_MS = 1800;

/** 検索ボックスに入力された語で行を絞り込む */
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

/** 新規追加ボタンを押すとトーストを一時表示する */
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

/** ページ種別を判定して必要なバインドだけ走らせる */
function init() {
  bindSearchFilter();
  bindRowClick();
  bindNewButton();
  bindEditMode();
}

document.addEventListener("DOMContentLoaded", init);
