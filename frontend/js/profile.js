const API_URL = "https://itamityt.ru/api";
const REDIRECT_URL = "https://itamityt.ru/rserv";

const token = localStorage.getItem("token");
if (!token) {
  window.location.href = "/login.html";
}

const list = document.getElementById("itemsList");
const message = document.getElementById("message");
const deleteBtn = document.getElementById("deleteAccountBtn");

// -------------------------------
// Загрузка всех ссылок
// -------------------------------
async function loadItems() {
  try {
    const res = await fetch(`${API_URL}/items/`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Ошибка загрузки ссылок");
    }

    const items = await res.json();
    list.innerHTML = "";

    if (items.length === 0) {
      list.textContent = "Ссылок пока нет";
      return;
    }

    items.forEach(item => {
      const li = document.createElement("li");
      const redirectUrl = `${REDIRECT_URL}/${item.link_id}`;
      li.innerHTML = `
        <a href="${redirectUrl}" target="_blank">${item.name}</a>
        <button onclick="deleteItem(${item.id})">Удалить</button>
      `;
      list.appendChild(li);
    });

  } catch (err) {
    console.error(err);
    message.textContent = err.message;
  }
}

// -------------------------------
// Добавление ссылки
// -------------------------------
document.getElementById("addItemForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;

  const body = {
    name: form.name.value,
    description: form.description.value
  };

  try {
    const res = await fetch(`${API_URL}/items/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(body)
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Ошибка добавления");
    }

    message.style.color = "green";
    message.textContent = "Ссылка добавлена";
    form.reset();
    loadItems();

  } catch (err) {
    message.style.color = "red";
    message.textContent = err.message;
  }
});

// -------------------------------
// Удаление ссылки
// -------------------------------
async function deleteItem(id) {
  try {
    const res = await fetch(`${API_URL}/items/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Ошибка удаления");
    }

    message.style.color = "green";
    message.textContent = "Ссылка удалена";
    loadItems();

  } catch (err) {
    message.style.color = "red";
    message.textContent = err.message;
  }
}

// -------------------------------
// Logout
// -------------------------------
document.getElementById("logoutBtn").addEventListener("click", () => {
  localStorage.removeItem("token");
  window.location.href = "/login.html";
});

// -------------------------------
// Удаление аккаунта
// -------------------------------
deleteBtn.addEventListener("click", async () => {
  if (!confirm("Вы точно хотите удалить свой аккаунт? Это действие необратимо!")) return;

  try {
    const res = await fetch(`${API_URL}/users/delete/me`, {  // эндпоинт на бэке должен позволять удаление текущего пользователя
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Ошибка удаления аккаунта");
    }

    localStorage.removeItem("token");
    alert("Аккаунт удален");
    window.location.href = "/index.html";

  } catch (err) {
    message.style.color = "red";
    message.textContent = err.message;
  }
});

// -------------------------------
// Автозагрузка
// -------------------------------
loadItems();
