async function loadInstitutions() {
  const response = await fetch(`${API_URL}/internal/institutions`, {
    headers: {
      "X-API-Key": INTERNAL_API_KEY,
    },
  });

  const data = await response.json();

  renderInstitutions(data.institutions);
}

function renderInstitutions(institutions) {
  const table = document.getElementById("institutionsTable");

  table.innerHTML = "";

  institutions.forEach((institution) => {
    table.innerHTML += `
            <tr>

                <td>
                    ${institution.institution_name}
                </td>

                <td>
                    ${institution.is_active ? "Ativa" : "Inativa"}
                </td>

                <td>

                    <button
                        class="btn btn-warning btn-sm"
                        onclick="toggleInstitution(
                            '${institution.id}',
                            ${institution.is_active}
                        )">

                        ${institution.is_active ? "Desativar" : "Ativar"}

                    </button>

                </td>

            </tr>
        `;
  });
}

async function createInstitution(event) {
  event.preventDefault();

  const institution_name = document.getElementById("institutionName").value;

  const key_hash = document.getElementById("keyHash").value;

  await fetch(`${API_URL}/internal/institutions`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
      "X-API-Key": INTERNAL_API_KEY,
    },

    body: JSON.stringify({
      institution_name,
      key_hash,
    }),
  });

  loadInstitutions();
}

async function toggleInstitution(institutionId, currentStatus) {
  await fetch(`${API_URL}/internal/institutions/${institutionId}`, {
    method: "PATCH",

    headers: {
      "Content-Type": "application/json",
      "X-API-Key": INTERNAL_API_KEY,
    },

    body: JSON.stringify({
      is_active: !currentStatus,
    }),
  });

  loadInstitutions();
}

document
  .getElementById("institutionForm")
  .addEventListener("submit", createInstitution);

loadInstitutions();
