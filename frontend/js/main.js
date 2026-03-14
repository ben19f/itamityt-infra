const API_URL = "https://itamityt.ru/api/public";

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

  // Проверяем, существует ли пользователь через API
  fetch(`${API_URL}/profile/${username}`)
    .then(res => {
      if (!res.ok) throw new Error("Пользователь не найден");
      return res.json();
    })
    .then(() => {
      // Если пользователь есть, переходим на public_profile.html с query-параметром
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

      // Ссылки пользователя (только для отображения)
      if (user.items && user.items.length) {
        user.items.forEach(item => {
          const p = document.createElement("p");
          const a = document.createElement("a");
          a.href = item.description;
          a.textContent = item.name;
          a.target = "_blank";
          p.appendChild(a);
          card.appendChild(p);
        });
      }

      // Клик по карточке — переход на публичный профиль
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
