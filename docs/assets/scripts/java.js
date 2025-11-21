const botonDescargar = document.querySelector('.boton-descargar');
const botonesApp = document.querySelectorAll('#botones-app img');

botonDescargar.addEventListener('click', function(e) {
    e.preventDefault(); // evita salto instantáneo

    // Scroll suave hacia arriba
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Pequeño delay para esperar que el scroll llegue arriba
    setTimeout(() => {
        botonesApp.forEach(img => img.classList.add('pop'));

        // Quitar la clase después de 600ms para volver al tamaño normal
        setTimeout(() => {
            botonesApp.forEach(img => img.classList.remove('pop'));
        }, 600);
    }, 500);
});




const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.barra-de-navegacion');

toggle.addEventListener('click', () => {
  nav.classList.toggle('show');
});