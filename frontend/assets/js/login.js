function login() {
  document
    .getElementById("loginForm")
    .addEventListener("submit", async function (event) {
      event.preventDefault();
      const usernameInput = document.getElementById("username").value;
      const passwordInput = document.getElementById("password").value;
      const submitBtn = document.getElementById("submitBtn");
      const messageDiv = document.getElementById("message");

      submitBtn.disabled = true;
      submitBtn.textContent = "Validando...";
      messageDiv.classList.add("d-none");

      try {
        const response = await fetch(`${API_URL}/internal/user/login`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-API-Key": INTERNAL_API_KEY,
          },
          body: JSON.stringify({
            username: usernameInput,
            password: passwordInput,
          }),
        });

        if (response.ok) {
          const data = await response.json();

          messageDiv.className = "alert alert-success mt-3";
          messageDiv.textContent = "Login efetuado com sucesso!";
          messageDiv.classList.remove("d-none");
          setTimeout(() => {
            window.location.href = "/";
          }, 500);
        } else {
          messageDiv.className = "alert alert-danger mt-3";
          messageDiv.textContent = "Usuário ou senha inválidos.";
          messageDiv.classList.remove("d-none");
        }
      } catch (error) {
        messageDiv.className = "alert alert-warning mt-3";
        messageDiv.textContent = "Erro de conexão com o servidor.";
        messageDiv.classList.remove("d-none");
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "Entrar";
      }
    });
}

login();
