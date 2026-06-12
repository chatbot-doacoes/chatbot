window.SendMessagesPage = (() => {
  const TAG_LABELS = {
    food: "Alimentos",
    clothing: "Roupas",
    diapers: "Fraldas",
  };

  function addUserRow() {
    const table = document.getElementById("usersTable");

    if (!table) return;

    table.insertAdjacentHTML(
      "beforeend",
      `
      <tr>

        <td>
          <input
            class="form-control user-name"
            required
          >
        </td>

        <td>
          <input
            class="form-control user-phone"
            placeholder="Ex: (DD)0000-0000"
            maxlength="13"
            required
          >
        </td>

        <td>

          <select
            class="form-select user-tag"
            required
          >

            <option value="food">
              ${TAG_LABELS.food}
            </option>

            <option value="clothing">
              ${TAG_LABELS.clothing}
            </option>

            <option value="diapers">
              ${TAG_LABELS.diapers}
            </option>

          </select>

        </td>

        <td>

          <button
            type="button"
            class="btn btn-danger"
            onclick="this.closest('tr').remove()"
          >
            Remover
          </button>

        </td>

      </tr>
    `,
    );

    const lastPhoneInput = table.querySelector("tr:last-child .user-phone");

    lastPhoneInput.addEventListener("input", (event) => {
      event.target.value = formatPhone(event.target.value);
    });
  }

  async function sendMessages(event) {
    event.preventDefault();

    const rows = document.querySelectorAll("#usersTable tr");

    const users = [];

    rows.forEach((row) => {
      users.push({
        user_name: row.querySelector(".user-name").value,
        user_phone: row.querySelector(".user-phone").value.replace(/\D/g, ""),
        tag: row.querySelector(".user-tag").value,
      });
    });

    const result = document.getElementById("result");

    for (const row of rows) {
      const phone = row.querySelector(".user-phone").value.replace(/\D/g, "");

      if (phone.length !== 10) {
        result.innerHTML = `
      <div class="alert alert-danger">
        O telefone deve conter exatamente 10 dígitos.
      </div>
    `;

        return;
      }
    }

    const sendButton = document.getElementById("sendButton");

    sendButton.disabled = true;

    sendButton.innerHTML = `
      <span class="spinner-border spinner-border-sm me-2"></span>
      Enviando...
    `;

    result.innerHTML = "";

    const response = await fetch(`${API_URL}/api/v1/messages`, {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        "X-API-Key": EXTERNAL_API_KEY,
      },

      body: JSON.stringify({
        send_to: users,
      }),
    });

    const data = await response.json();
    sendButton.disabled = false;
    sendButton.textContent = "Enviar Mensagens";

    renderResult(data);
  }

  function renderResult(data) {
    const result = document.getElementById("result");

    if (!result) return;

    if (data.invalid_users?.length > 0) {
      result.innerHTML = `
      <div class="alert alert-danger">
        Um ou mais destinatários possuem dados inválidos.
      </div>
    `;

      return;
    }

    result.innerHTML = `
    <div class="alert alert-success">
      Mensagens enviadas com sucesso!
    </div>
  `;
  }

  function formatPhone(value) {
    const digits = value.replace(/\D/g, "").slice(0, 10);

    if (digits.length <= 2) {
      return digits;
    }

    if (digits.length <= 6) {
      return `(${digits.slice(0, 2)})${digits.slice(2)}`;
    }

    return `(${digits.slice(0, 2)})${digits.slice(2, 6)}-${digits.slice(6)}`;
  }

  function initialize() {
    const form = document.getElementById("sendMessagesForm");

    if (!form) return;

    form.onsubmit = sendMessages;

    const table = document.getElementById("usersTable");

    if (table && table.children.length === 0) {
      addUserRow();
    }
  }

  return {
    initialize,
    addUserRow,
  };
})();
