const form = document.getElementById("loginForm");
const messageEl = document.getElementById("message");
const API_URL = "/api";

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  messageEl.textContent = "";

  const formData = {
    email: form.email.value,
    password: form.password.value
  };

  try {
    const res = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData)
    });

    const data = await res.json();

    if (res.ok) {
      localStorage.setItem("token", data.access_token);
      messageEl.style.color = "green";
      messageEl.textContent = "Успешный вход";
      window.location.href = "/userhome.html";
    } else {
      messageEl.textContent = data.detail || "Ошибка входа";
    }

  } catch (err) {
    console.error(err);
    messageEl.textContent = "Ошибка сети";
  }
});
