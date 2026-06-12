window.Header = (() => {
  function initialize() {
    const profileButton = document.getElementById("profileButton");

    const profileMenu = document.getElementById("profileMenu");

    const logoutButton = document.getElementById("logoutButton");

    const username = localStorage.getItem("loggedUser") || "Administrador";

    document.getElementById("loggedUsername").textContent = username;

    document.getElementById("profileUsername").textContent = username;

    profileButton.onclick = () => {
      profileMenu.classList.toggle("d-none");

      profileButton.classList.toggle("open");
    };

    document.addEventListener("click", (event) => {
      if (!event.target.closest(".profile-container")) {
        profileMenu.classList.add("d-none");

        profileButton.classList.remove("open");
      }
    });

    logoutButton.onclick = () => {
      localStorage.removeItem("loggedUser");

      window.location.href = "/pages/login.html";
    };
  }

  return {
    initialize,
  };
})();
