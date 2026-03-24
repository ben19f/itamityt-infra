const API_URL = "https://itamityt.ru/api/public";
const REDIRECT_URL = "https://itamityt.ru/rserv";

const searchBtn = document.getElementById("search-btn");
const searchUsernameInput = document.getElementById("search-username");
const messageEl = document.getElementById("message");
const lastUsersContainer = document.getElementById("last-users-container");

// Поиск профиля по username
searchBtn.addEventListener("click", () => {
  const username = searchUsernameInput.value.trim();
  messageEl.textContent = "";

  if (!username) {
    messageEl.textContent = "Введите username";
    return;
  }

  fetch(`${API_URL}/profile/${encodeURIComponent(username)}`)
    .then(res => {
      if (!res.ok) throw new Error("Пользователь не найден");
      return res.json();
    })
    .then(() => {
      window.location.href = `public_profile.html?username=${encodeURIComponent(username)}`;
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

      // Items пользователя
      if (user.items && user.items.length) {
        user.items.forEach(item => {
          const p = document.createElement("p");
          const redirectUrl = `${REDIRECT_URL}/${item.link_id}`;
          const a = document.createElement("a");
          a.href = `${REDIRECT_URL}/${item.link_id}`; // публичный link_id
          a.textContent = item.name;
          a.target = "_blank";
          a.addEventListener("click", e => e.stopPropagation()); // чтобы card click не срабатывал
          p.appendChild(a);
          card.appendChild(p);
        });
      }

      // Клик по карточке пользователя
      card.addEventListener("click", () => {
        window.location.href = `public_profile.html?username=${encodeURIComponent(user.username)}`;
      });

      lastUsersContainer.appendChild(card);
    });
  })
  .catch(err => {
    console.error(err);
    lastUsersContainer.textContent = "Не удалось загрузить последних пользователей";
  });
