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
