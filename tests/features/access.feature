Feature: Inicio de sesión

  Scenario: Formulario de Ingreso de Credenciales
    Dado que el usuario navega a la página de Iniciar Sesión
    Cuando la página carga
    Entonces se visualiza un formulario de acceso con los campos "Correo Electrónico" y "Contraseña" con sus placeholders respectivos (ejemplo@correo.com, ••••••••)
    Y se visualiza un botón de acción primario titulado "Acceder"

  Scenario: Opciones de Recuperación y Registro
    Dado que el usuario visualiza el formulario de acceso
    Cuando revisa las opciones adicionales
    Entonces se muestran una casilla de verificación para "Recordarme"
    Y se muestra un enlace para "¿Olvidaste tu contraseña?"
    Y se muestra un enlace de texto que dice "Regístrate aquí"

Feature: Cerrar sesión como médico o paciente

  Scenario: Confirmación de Cierre de Sesión
    Dado que el usuario (Médico o Paciente) está en cualquier parte de su respectivo panel
    Cuando hace clic en la opción "Cerrar Sesión" en el menú de navegación lateral
    Entonces se despliega una ventana modal en el centro de la pantalla preguntando "¿Deseas cerrar sesión?" con dos botones de acción: "Cancelar" y "Cerrar sesión"