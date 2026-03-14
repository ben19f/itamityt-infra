const API_URL = "https://itamityt.ru/api/public";

const searchBtn = document.getElementById("search-btn");
const searchUsernameInput = document.getElementById("search-username");
const searchResult = document.getElementById("search-result");
const lastUsersContainer = document.getElementById("last-users-container");
const messageEl = document.getElementById("message");

// Поиск профиля по username
searchBtn.addEventListener("click", () => {
  const username = searchUsernameInput.value.trim();
  searchResult.innerHTML = "";
  messageEl.textContent = "";

  if (!username) {
    messageEl.textContent = "Введите username";
    return;
  }

  fetch(`${API_URL}/profile/${username}`)
    .then(res => {
      if (!res.ok) throw new Error(`Пользователь не найден (${res.status})`);
      return res.json();
    })
    .then(items => {
      if (items.length === 0) {
        searchResult.textContent = "У пользователя пока нет ссылок";
        return;
      }
      const container = document.createElement("div");
      items.forEach(item => {
        const a = document.createElement("a");
        a.href = item.description;
        a.textContent = item.name;
        a.target = "_blank";
        container.appendChild(a);
      });
      searchResult.appendChild(container);
    })
    .catch(err => {
      console.error(err);
      messageEl.textContent = err.message;
    });
});

// Загрузка последних зарегистрированных пользователей
fetch(`${API_URL}/last-users`)
  .then(res => {
    if (!res.ok) throw new Error("Не удалось загрузить последних пользователей");
    return res.json();
  })
  .then(users => {
    if (!users.length) {
      lastUsersContainer.textContent = "Нет зарегистрированных пользователей";
      return;
    }
    users.forEach(user => {
      const card = document.createElement("div");
      card.classList.add("card");
      const h3 = document.createElement("h3");
      h3.textContent = user.username;
      card.appendChild(h3);

      // Ссылки пользователя
      if (user.items && user.items.length) {
        user.items.forEach(item => {
          const a = document.createElement("a");
          a.href = item.description;
          a.textContent = item.name;
          a.target = "_blank";
          card.appendChild(a);
        });
      }
      lastUsersContainer.appendChild(card);
    });
  })
  .catch(err => {
    console.error(err);
    lastUsersContainer.textContent = "Не удалось загрузить последних пользователей";
  });
