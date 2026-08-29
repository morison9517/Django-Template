/* ===========================================================================
   todo.js = デモページだけで使うサンプル

   ★これは動作確認用です。自分たちのJSは static/js/ に置きます。
     書き方の見本としてどうぞ。

   ▼ 相手は demo/api.py
       GET    /__demo/api/todos              一覧
       POST   /__demo/api/todos/create       追加   {"title": "..."}
       PATCH  /__demo/api/todos/:id          完了の切り替え
       DELETE /__demo/api/todos/:id/delete   削除

   ▼ 項目名(id / title / is_done)は demo/models.py の
     to_dict() で決まっている。★ここを変えるときは両方直す。

   ▼ api.get / api.post / showMessage / withBusy は main.js の道具。
     整理券(CSRFトークン)は api が自動で付けるので、ここでは意識しない。
   =========================================================================== */

const form = document.getElementById("todo-form");
const input = document.getElementById("todo-title");
const list = document.getElementById("todo-list");

// このページ(トップ)以外では要素が無いので、何もしない。
if (form && input && list) {
  loadTodos();

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const title = input.value.trim();
    if (!title) return;

    await withBusy(form.querySelector("button"), async () => {
      try {
        await api.post("/__demo/api/todos/create", { title });
        input.value = "";
        await loadTodos();
      } catch (error) {
        showMessage(error.message, "error");
      }
    });
  });
}

async function loadTodos() {
  try {
    const data = await api.get("/__demo/api/todos");
    render(data.todos ?? []);
  } catch (error) {
    showMessage(error.message, "error");
  }
}

function render(todos) {
  list.textContent = "";

  if (todos.length === 0) {
    const empty = document.createElement("li");
    empty.className = "todo-empty";
    empty.textContent = "まだ何もありません。";
    list.appendChild(empty);
    return;
  }

  for (const todo of todos) {
    list.appendChild(createItem(todo));
  }
}

function createItem(todo) {
  const item = document.createElement("li");
  item.className = todo.is_done ? "todo-item is-done" : "todo-item";

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.checked = todo.is_done;
  checkbox.addEventListener("change", () => toggle(todo.id));

  const text = document.createElement("span");
  text.className = "todo-text";
  text.textContent = todo.title;

  const removeButton = document.createElement("button");
  removeButton.className = "btn btn-ghost btn-small";
  removeButton.textContent = "削除";
  removeButton.addEventListener("click", () => remove(todo.id, removeButton));

  item.append(checkbox, text, removeButton);
  return item;
}

async function toggle(id) {
  try {
    await api.patch(`/__demo/api/todos/${id}`);
    await loadTodos();
  } catch (error) {
    showMessage(error.message, "error");
  }
}

async function remove(id, button) {
  await withBusy(button, async () => {
    try {
      await api.delete(`/__demo/api/todos/${id}/delete`);
      await loadTodos();
    } catch (error) {
      showMessage(error.message, "error");
    }
  });
}
