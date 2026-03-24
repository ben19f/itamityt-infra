const API_URL = "https://itamityt.ru/api";
const REDIRECT_URL = "https://itamityt.ru/rserv";

const token = localStorage.getItem("token");
if (!token) {
  window.location.href = "/login.html";
}

// Для дебага: покажем токен в консоли
console.log("JWT token:", token);

const list = document.getElementById("itemsList");
const message = document.getElementById("message");
const deleteBtn = document.getElementById("deleteAccountBtn");

// -------------------------------
// Вспомогательная функция для заголовков
// -------------------------------
function getAuthHeaders() {
  return {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  };
}

// -------------------------------
// Загрузка всех ссылок
// -------------------------------
async function loadItems() {
  try {
    const res = await fetch(`${API_URL}/items/`, {
      method: "GET",
      headers: getAuthHeaders()
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Ошибка загрузки ссылок");
    }

    const items = await res.json();
    list.innerHTML = "";

    if (!items || items.length === 0) {
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
    message.style.color = "red";
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
      headers: getAuthHeaders(),
      body: JSON.stringify(body)
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
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
      headers: getAuthHeaders()
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
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
if (deleteBtn) {
  deleteBtn.addEventListener("click", async () => {
    if (!confirm("Вы точно хотите удалить свой аккаунт? Это действие необратимо!")) return;

    try {
      const res = await fetch(`${API_URL}/users/delete/me`, {
        method: "DELETE",
        headers: getAuthHeaders()
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
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
}

// -------------------------------
// Автозагрузка
// -------------------------------
loadItems();
