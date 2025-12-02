document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const errorMessage = document.getElementById("mensaje-error");
  const successModal = document.getElementById("successModal");
  const modalContent = successModal.querySelector(".modal-content");

  const validPassword = "123456";
  const doctorEmail = "doctor@ejemplo.com";
  const patientEmail = "paciente@ejemplo.com";

  successModal.style.display = "none";

  loginForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    if (password !== validPassword) {
      errorMessage.textContent = "Contraseña incorrecta.";
      errorMessage.style.display = "block";
      return;
    }

    if (email !== doctorEmail && email !== patientEmail) {
      errorMessage.textContent = "Correo no reconocido.";
      errorMessage.style.display = "block";
      return;
    }

    errorMessage.style.display = "none";

    successModal.style.display = "flex";

    setTimeout(() => {
      successModal.classList.add("fade-out");
      modalContent.classList.add("fade-out");

      setTimeout(() => {
        successModal.style.display = "none";
        successModal.classList.remove("fade-out");
        modalContent.classList.remove("fade-out");

        if (email === doctorEmail) {
          window.location.href = "panel-doctor.html";
        } else if (email === patientEmail) {
          window.location.href = "panel-paciente.html";
        }
      }, 300);
    }, 1500);
  });
});


document.addEventListener("DOMContentLoaded", () => {
  const botonsSimulacion = document.querySelectorAll(".boton-descargar, .boton-doctor, .boton-simulacion");
  const modal = document.getElementById("modal-confirmacion");
  const cerrar = document.querySelector(".cerrar");
  const botonCancelar = document.getElementById("modal-cancelar");
  const botonAceptar = document.getElementById("modal-aceptar");

  botonsSimulacion.forEach(boton => {
    boton.addEventListener("click", (e) => {
      e.preventDefault();
      modal.style.display = "block";
    });
  });

  cerrar.addEventListener("click", () => modal.style.display = "none");
  botonCancelar.addEventListener("click", () => modal.style.display = "none");

  botonAceptar.addEventListener("click", () => {
    window.location.href = "panel-doctor.html";
  });

  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
});

