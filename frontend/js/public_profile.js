// Получаем username из query-параметра URL
const params = new URLSearchParams(window.location.search);
const username = params.get("username");
const profileTitle = document.getElementById("profile-title");
const linksContainer = document.getElementById("links-container");
const messageEl = document.getElementById("message");

// URL публичного API
const API_URL = "https://itamityt.ru/api/public";

if (!username) {
  messageEl.textContent = "Не указан пользователь";
} else {
  profileTitle.textContent = `Профиль пользователя: ${username}`;

  // Запрос к API
  fetch(`${API_URL}/profile/${username}`)
    .then(res => {
      if (!res.ok) throw new Error(`Ошибка ${res.status}`);
      return res.json();
    })
    .then(items => {
      if (items.length === 0) {
        linksContainer.textContent = "У пользователя пока нет ссылок";
        return;
      }
      items.forEach(item => {
        const a = document.createElement("a");
        a.href = item.description;   // считаем description = ссылка
        a.textContent = item.name;
        a.target = "_blank";
        linksContainer.appendChild(a);
      });
    })
    .catch(err => {
      console.error(err);
      messageEl.textContent = "Не удалось загрузить ссылки пользователя";
    });
}
