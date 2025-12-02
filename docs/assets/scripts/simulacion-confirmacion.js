document.addEventListener("DOMContentLoaded", () => {
  const botonSimulacion = document.querySelector(".boton-descargar"); 
  const modal = document.getElementById("modal-confirmacion");
  const cerrar = document.querySelector(".cerrar");
  const botonCancelar = document.getElementById("modal-cancelar");
  const botonAceptar = document.getElementById("modal-aceptar");

  botonSimulacion.addEventListener("click", (e) => {
    e.preventDefault(); 
    modal.style.display = "block";
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
