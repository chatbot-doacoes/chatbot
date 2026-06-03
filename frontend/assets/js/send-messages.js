function addUserRow() {
  const table = document.getElementById("usersTable");

  table.innerHTML += `
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
          required
        >
      </td>

      <td>

        <select
          class="form-select user-tag"
          required
        >

          <option value="food">
            Food
          </option>

          <option value="clothing">
            Clothing
          </option>

          <option value="diapers">
            Diapers
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
  `;
}

async function sendMessages(event) {
  event.preventDefault();

  const rows = document.querySelectorAll("#usersTable tr");

  const users = [];

  rows.forEach((row) => {
    users.push({
      user_name: row.querySelector(".user-name").value,

      user_phone: row.querySelector(".user-phone").value,

      tag: row.querySelector(".user-tag").value,
    });
  });

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

  renderResult(data);
}

function renderResult(data) {
  const result = document.getElementById("result");

  if (data.invalid_users && data.invalid_users.length > 0) {
    result.innerHTML = `
      <div class="alert alert-warning">

        <h5>Usuários inválidos</h5>

        <pre>
${JSON.stringify(data.invalid_users, null, 2)}
        </pre>

      </div>
    `;

    return;
  }

  result.innerHTML = `
    <div class="alert alert-success">
      ${data.message}
    </div>
  `;
}

addUserRow();

document
  .getElementById("sendMessagesForm")
  .addEventListener("submit", sendMessages);
