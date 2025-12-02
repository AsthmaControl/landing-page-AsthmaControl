Feature: Inicio de sesión

Escenario 1: Formulario de Ingreso de Credenciales

Dado que el usuario navega a la página de Iniciar Sesión,
CUANDO la página carga,
ENTONCES se visualiza un formulario de acceso con los campos "Correo Electrónico" y "Contraseña" con sus placeholders respectivos (ejemplo@correo.com, ••••••••), y un botón de acción primario titulado "Acceder".

Escenario 2: Opciones de Recuperación y Registro

Dado que el usuario visualiza el formulario de acceso,
CUANDO revisa las opciones adicionales.
ENTONCES se muestran una casilla de verificación para "Recordarme", un enlace para "¿Olvidaste tu contraseña?" y, en la parte inferior, un enlace de texto que dice "Regístrate aquí".