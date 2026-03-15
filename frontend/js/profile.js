const API_URL = "/api";

const token = localStorage.getItem("token");

if (!token) {
  window.location.href = "/login.html";
}

const list = document.getElementById("itemsList");
const message = document.getElementById("message");


// загрузка всех ссылок

async function loadItems() {

  const res = await fetch(`${API_URL}/items/`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  const items = await res.json();

  list.innerHTML = "";

  items.forEach(item => {
  const li = document.createElement("li");

  // формируем ссылку через редирект
  const redirectUrl = `http://127.0.0.1:8000/r/${item.link_id}`; // <- сюда вставляем link_id

  li.innerHTML = `
    <a href="${redirectUrl}" target="_blank">${item.name}</a>
    <button onclick="deleteItem(${item.id})">Удалить</button>
  `;

  list.appendChild(li);
});

}


// добавление

document.getElementById("addItemForm").addEventListener("submit", async (e) => {

  e.preventDefault();

  const form = e.target;

  const body = {
    name: form.name.value,
    description: form.description.value
  };

  const res = await fetch(`${API_URL}/items/`, {

    method: "POST",

    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },

    body: JSON.stringify(body)

  });

  if (res.ok) {

    message.textContent = "Ссылка добавлена";

    form.reset();

    loadItems();

  } else {

    message.textContent = "Ошибка добавления";

  }

});


// удаление

async function deleteItem(id) {

  const res = await fetch(`${API_URL}/items/${id}`, {

    method: "DELETE",

    headers: {
      Authorization: `Bearer ${token}`
    }

  });

  if (res.ok) {

    message.textContent = "Ссылка удалена";

    loadItems();

  }

}


// logout

document.getElementById("logoutBtn").addEventListener("click", () => {

  localStorage.removeItem("token");

  window.location.href = "/login.html";

});


// загрузка при открытии страницы

loadItems();