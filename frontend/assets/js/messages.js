let editingMessageId = null;

const TAG_LABELS = {
  food: "Alimentos",
  clothing: "Roupas",
  diapers: "Fraldas",
};

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

        <td>${TAG_LABELS[message.tag] ?? message.tag}</td>

        <td>${message.message_template}</td>

        <td>
          <div class="d-flex gap-2">

            <button
              class="btn btn-warning btn-sm"
              onclick="editMessage(
                '${message.id}',
                '${message.tag}',
                \`${message.message_template}\`
              )"
            >
              Editar
            </button>

            <button
              class="btn btn-danger btn-sm"
              onclick="deleteMessage('${message.id}')"
            >
              Excluir
            </button>

          </div>
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

  if (editingMessageId) {
    await fetch(`${API_URL}/internal/messages/${editingMessageId}`, {
      method: "PATCH",

      headers: {
        "Content-Type": "application/json",
        "X-API-Key": INTERNAL_API_KEY,
      },

      body: JSON.stringify({
        tag,
        message_template: messageTemplate,
      }),
    });
  } else {
    await fetch(`${API_URL}/internal/institutions/${institutionId}/messages`, {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        "X-API-Key": INTERNAL_API_KEY,
      },

      body: JSON.stringify({
        tag,
        message_template: messageTemplate,
      }),
    });
  }

  resetMessageForm();

  loadMessages();
}

async function deleteMessage(messageId) {
  const confirmed = confirm("Deseja realmente excluir este template?");

  if (!confirmed) {
    return;
  }

  await fetch(`${API_URL}/internal/messages/${messageId}`, {
    method: "DELETE",

    headers: {
      "X-API-Key": INTERNAL_API_KEY,
    },
  });

  loadMessages();
}

function editMessage(messageId, currentTag, currentTemplate) {
  editingMessageId = messageId;

  document.getElementById("formTitle").textContent = "Editar Template";

  document.getElementById("messageTag").value = currentTag;

  document.getElementById("messageTemplate").value = currentTemplate;

  document.getElementById("submitMessageButton").textContent =
    "Salvar Alterações";

  document.getElementById("cancelEditButton").classList.remove("d-none");

  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
}

function resetMessageForm() {
  editingMessageId = null;

  document.getElementById("formTitle").textContent = "Novo Template";

  document.getElementById("messageTag").value = "food";

  document.getElementById("messageTemplate").value = "";

  document.getElementById("submitMessageButton").textContent = "Cadastrar";

  document.getElementById("cancelEditButton").classList.add("d-none");
}

document
  .getElementById("messageForm")
  .addEventListener("submit", createMessage);

document
  .getElementById("institutionSelect")
  .addEventListener("change", loadMessages);

document
  .getElementById("cancelEditButton")
  .addEventListener("click", resetMessageForm);

loadInstitutions();
