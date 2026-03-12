// Статические данные для MVP
const links = [
  {name: "Telegram", url: "https://t.me/example"},
  {name: "YouTube", url: "https://youtube.com/example"},
  {name: "Instagram", url: "https://instagram.com/example"}
];

// Функция отображения ссылок на index.html
function renderLinks() {
  const container = document.getElementById('links-container');
  if (!container) return;

  container.innerHTML = '';
  links.forEach(link => {
    const a = document.createElement('a');
    a.href = link.url;
    a.target = '_blank';
    a.textContent = link.name;
    container.appendChild(a);
  });
}

renderLinks();

// Форма добавления ссылок на admin.html
const form = document.getElementById('add-link-form');
if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('link-name').value;
    const url = document.getElementById('link-url').value;
    links.push({name, url});
    document.getElementById('links-list').innerHTML += `<li>${name} - <a href="${url}" target="_blank">${url}</a></li>`;
    form.reset();
  });
}