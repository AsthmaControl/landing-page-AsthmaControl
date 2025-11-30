document.addEventListener("DOMContentLoaded", () => {
  
  const btnLogout = document.getElementById("btnLogout");
  const logoutModal = document.getElementById("logoutModal");
  const logoutConfirm = document.getElementById("logoutConfirm");
  const logoutCancel = document.getElementById("logoutCancel");
  const modalContent = logoutModal.querySelector(".modal-content");

  btnLogout.addEventListener("click", (e) => {
    e.preventDefault(); 
    logoutModal.style.display = "flex";
  });

  logoutCancel.addEventListener("click", () => {
    logoutModal.classList.add("fade-out");
    modalContent.classList.add("fade-out");

    setTimeout(() => {
      logoutModal.style.display = "none";
      logoutModal.classList.remove("fade-out");
      modalContent.classList.remove("fade-out");
    }, 300);
  });

  logoutConfirm.addEventListener("click", () => {

    logoutModal.classList.add("fade-out");
    modalContent.classList.add("fade-out");

    setTimeout(() => {
      logoutModal.style.display = "none";
      logoutModal.classList.remove("fade-out");
      modalContent.classList.remove("fade-out");

      window.location.href = "index.html";
    }, 300);
  });

  window.addEventListener("click", (e) => {
    if (e.target === logoutModal) {
      logoutModal.style.display = "none";
    }
  });

});