const form = document.getElementById("registerForm");
const messageEl = document.getElementById("message");

// URL твоего бэкенда (через Docker, если фронт в контейнере, можно backend:8100)
// const API_URL = "http://localhost:8100"; // для локальной разработки
// const API_URL = "http://backend:8100"; // для Docker сети
const API_URL = "http://172.21.0.2:8100"; // для vps разработки

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  messageEl.textContent = "";

  const formData = {
    username: form.username.value,
    password: form.password.value
  };

  try {
    const res = await fetch(`${API_URL}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(formData)
    });

    const data = await res.json();

    if (res.ok) {
      messageEl.textContent = `Пользователь ${data.username} зарегистрирован!`;
      form.reset();
    } else {
      messageEl.textContent = data.detail || "Ошибка регистрации";
    }
  } catch (err) {
    console.error(err);
    messageEl.textContent = "Ошибка сети";
  }
});