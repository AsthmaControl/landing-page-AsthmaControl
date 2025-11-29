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

    // Mostrar modal
    successModal.style.display = "flex";

    // Esperar un poco antes de cerrar
    setTimeout(() => {
      // Agregar clases para animación fade-out
      successModal.classList.add("fade-out");
      modalContent.classList.add("fade-out");

      // Después de la animación, ocultar modal y redirigir
      setTimeout(() => {
        successModal.style.display = "none";
        successModal.classList.remove("fade-out");
        modalContent.classList.remove("fade-out");

        if (email === doctorEmail) {
          window.location.href = "panel-doctor.html";
        } else if (email === patientEmail) {
          window.location.href = "panel-paciente.html";
        }
      }, 300); // Duración de la animación fade-out
    }, 1500);
  });
});


document.addEventListener("DOMContentLoaded", () => {
  const botonSimulacion = document.querySelector(".boton-descargar"); // botón "Probar Simulación"
  const modal = document.getElementById("modal-confirmacion");
  const cerrar = document.querySelector(".cerrar");
  const btnCancelar = document.getElementById("modal-cancelar");
  const btnAceptar = document.getElementById("modal-aceptar");

  // Mostrar modal al hacer clic
  botonSimulacion.addEventListener("click", (e) => {
    e.preventDefault(); // evita redirección inmediata
    modal.style.display = "block";
  });

  // Cerrar modal al hacer clic en X o cancelar
  cerrar.addEventListener("click", () => modal.style.display = "none");
  btnCancelar.addEventListener("click", () => modal.style.display = "none");

  // Confirmar acción
  btnAceptar.addEventListener("click", () => {
    window.location.href = "panel-doctor.html"; // redirige al panel
  });

  // Cerrar modal si se hace clic fuera del contenido
  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
});
