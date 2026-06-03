async function loadInstitutions() {
  const response = await fetch(`${API_URL}/internal/institutions`, {
    headers: {
      "X-API-Key": INTERNAL_API_KEY,
    },
  });

  const data = await response.json();

  const select = document.getElementById("institutionSelect");

  select.innerHTML = "";

  data.institutions.forEach((institution) => {
    select.innerHTML += `
            <option value="${institution.id}">
                ${institution.institution_name}
            </option>
        `;
  });

  loadMessages();
}

async function loadMessages() {
  const institutionId = document.getElementById("institutionSelect").value;

  if (!institutionId) {
    return;
  }

  const response = await fetch(
    `${API_URL}/internal/institutions/${institutionId}/messages`,
    {
      headers: {
        "X-API-Key": INTERNAL_API_KEY,
      },
    },
  );

  const data = await response.json();

  renderMessages(data.messages);
}

function renderMessages(messages) {
  const table = document.getElementById("messagesTable");

  table.innerHTML = "";

  messages.forEach((message) => {
    table.innerHTML += `
            <tr>

                <td>
                    ${message.tag}
                </td>

                <td>
                    ${message.message_template}
                </td>

            </tr>
        `;
  });
}

async function createMessage(event) {
  event.preventDefault();

  const institutionId = document.getElementById("institutionSelect").value;

  const tag = document.getElementById("messageTag").value;

  const messageTemplate = document.getElementById("messageTemplate").value;

  await fetch(`${API_URL}/internal/institutions/${institutionId}/messages`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
      "X-API-Key": INTERNAL_API_KEY,
    },

    body: JSON.stringify({
      tag: tag,
      message_template: messageTemplate,
    }),
  });

  document.getElementById("messageTemplate").value = "";

  loadMessages();
}

document
  .getElementById("messageForm")
  .addEventListener("submit", createMessage);

document
  .getElementById("institutionSelect")
  .addEventListener("change", loadMessages);

loadInstitutions();
