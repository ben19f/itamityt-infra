const form = document.getElementById("registerForm");
const messageEl = document.getElementById("message");

// URL бэкенда через Nginx proxy на /api
const API_URL = "/api";  

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  messageEl.textContent = "";

  const formData = {
    username: form.username.value,
    email: form.email.value,
    password: form.password.value
  };

  try {
    const res = await fetch(`${API_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData)
    });

    const data = await res.json();

    if (res.ok) {
      messageEl.style.color = "green";
      messageEl.textContent = `Пользователь ${data.username} успешно зарегистрирован!`;
      form.reset();
    } else {
      // отображаем ошибки валидации от FastAPI
      if (data.detail && Array.isArray(data.detail)) {
        messageEl.textContent = data.detail.map(err => `${err.loc[1]}: ${err.msg}`).join("; ");
      } else {
        messageEl.textContent = data.detail || "Ошибка регистрации";
      }
    }
  } catch (err) {
    console.error(err);
    messageEl.textContent = "Ошибка сети";
  }
});