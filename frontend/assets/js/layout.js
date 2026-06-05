async function loadComponent(id, file) {
  const response = await fetch(file);
  const html = await response.text();

  document.getElementById(id).innerHTML = html;
}

async function loadPage(page) {
  const response = await fetch(`/components/${page}.html`);
  const html = await response.text();

  document.getElementById("content-area").innerHTML = html;

  document.querySelectorAll(".sidebar-item").forEach((item) => {
    item.classList.remove("active");

    if (item.dataset.page === page) {
      item.classList.add("active");
    }
  });

  if (page === "institutions") {
    if (!window.InstitutionsPage) {
      await import("/assets/js/institutions.js");
    }

    window.InstitutionsPage.initialize();
  }

  if (page === "messages") {
    if (!window.MessagesPage) {
      await import("/assets/js/messages.js");
    }

    window.MessagesPage.initialize();
  }

  if (page === "send-messages") {
    if (!window.SendMessagesPage) {
      await import("/assets/js/send-messages.js");
    }

    window.SendMessagesPage.initialize();
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  await loadComponent("header", "/components/header.html");
  await loadComponent("sidebar", "/components/sidebar.html");

  document.addEventListener("click", (event) => {
    const item = event.target.closest(".sidebar-item");

    if (!item) return;

    loadPage(item.dataset.page);
  });

  loadPage("about");
});
