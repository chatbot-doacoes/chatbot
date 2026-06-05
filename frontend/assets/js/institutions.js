window.InstitutionsPage = (() => {
  let editingInstitutionId = null;
  let deletingInstitutionId = null;
  let deletingInstitutionName = null;

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

    if (!table) return;

    table.innerHTML = "";

    institutions.forEach((institution) => {
      table.innerHTML += `
        <tr>

          <td>${institution.institution_name}</td>

          <td>
            ${institution.is_active ? "Ativa" : "Inativa"}
          </td>

          <td>
            <div class="d-flex gap-2">

              <button
                class="btn btn-primary btn-sm"
                onclick="InstitutionsPage.editInstitution(
                  '${institution.id}',
                  \`${institution.institution_name}\`,
                  ${institution.is_active}
                )"
              >
                Editar
              </button>

              <button
                class="btn btn-warning btn-sm"
                onclick="InstitutionsPage.toggleInstitution(
                  '${institution.id}',
                  ${institution.is_active}
                )"
              >
                ${institution.is_active ? "Desativar" : "Ativar"}
              </button>

              <button
                class="btn btn-danger btn-sm"
                onclick="InstitutionsPage.deleteInstitution(
                  '${institution.id}',
                  \`${institution.institution_name}\`
                )"
              >
                Excluir
              </button>

            </div>
          </td>

        </tr>
      `;
    });
  }

  async function createInstitution(event) {
    event.preventDefault();

    const institution_name = document.getElementById("institutionName").value;

    const key_hash = document.getElementById("keyHash").value;

    if (editingInstitutionId) {
      await fetch(`${API_URL}/internal/institutions/${editingInstitutionId}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": INTERNAL_API_KEY,
        },
        body: JSON.stringify({
          institution_name,
        }),
      });
    } else {
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
    }

    resetInstitutionForm();

    await loadInstitutions();
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

    await loadInstitutions();
  }

  function editInstitution(institutionId, institutionName) {
    editingInstitutionId = institutionId;

    document.getElementById("keyHash").disabled = true;

    document.getElementById("institutionName").value = institutionName;

    document.getElementById("formTitle").textContent = "Editar Instituição";

    document.getElementById("submitInstitutionButton").textContent =
      "Salvar Alterações";

    document.getElementById("cancelEditButton").classList.remove("d-none");

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  }

  function resetInstitutionForm() {
    editingInstitutionId = null;

    document.getElementById("keyHash").disabled = false;

    document.getElementById("institutionName").value = "";
    document.getElementById("keyHash").value = "";

    document.getElementById("formTitle").textContent = "Nova Instituição";

    document.getElementById("submitInstitutionButton").textContent =
      "Cadastrar";

    document.getElementById("cancelEditButton").classList.add("d-none");
  }

  function deleteInstitution(institutionId, institutionName) {
    deletingInstitutionId = institutionId;
    deletingInstitutionName = institutionName;

    document.getElementById("deleteInstitutionName").textContent =
      institutionName;

    document.getElementById("deleteConfirmation").classList.remove("d-none");

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  }

  async function confirmDeleteInstitution() {
    if (!deletingInstitutionId) return;

    await fetch(`${API_URL}/internal/institutions/${deletingInstitutionId}`, {
      method: "DELETE",
      headers: {
        "X-API-Key": INTERNAL_API_KEY,
      },
    });

    deletingInstitutionId = null;
    deletingInstitutionName = null;

    document.getElementById("deleteConfirmation").classList.add("d-none");

    await loadInstitutions();
  }

  function cancelDeleteInstitution() {
    deletingInstitutionId = null;
    deletingInstitutionName = null;

    document.getElementById("deleteInstitutionName").textContent = "";

    document.getElementById("deleteConfirmation").classList.add("d-none");
  }

  function initialize() {
    const institutionForm = document.getElementById("institutionForm");

    const cancelEditButton = document.getElementById("cancelEditButton");

    const confirmDeleteButton = document.getElementById("confirmDeleteButton");

    const cancelDeleteButton = document.getElementById("cancelDeleteButton");

    if (!institutionForm) return;

    institutionForm.onsubmit = createInstitution;
    cancelEditButton.onclick = resetInstitutionForm;
    confirmDeleteButton.onclick = confirmDeleteInstitution;
    cancelDeleteButton.onclick = cancelDeleteInstitution;

    loadInstitutions();
  }

  return {
    initialize,
    editInstitution,
    toggleInstitution,
    deleteInstitution,
  };
})();
