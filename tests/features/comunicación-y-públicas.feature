Feature: Chat con médico

  Scenario: Interfaz de Chat Funcional
    Dado que el usuario (Paciente o Médico) accede a la sección de Mensajes
    Cuando selecciona una conversación activa de la lista lateral
    Entonces se muestra un panel con el historial de la conversación
    Y se muestra un área de texto multi-línea con el texto de ayuda "Escriba un mensaje..."
    Y se muestra un botón de acción "Enviar"

Feature: Navegación en la Landing Page

  Scenario: Barra de Navegación Consistente
    Dado que el usuario accede a cualquier página pública (Inicio, Contacto o Tecnología)
    Cuando visualiza el encabezado de la página
    Entonces la barra de navegación muestra el logo principal y los enlaces funcionales a "Inicio", "¿Qué brindamos?", "Contacto al cliente" y "Iniciar Sesión"

Feature: Propuesta de valor 

  Scenario: Propuesta de Valor en la Página de Inicio
    Dado que un nuevo usuario carga la página "Inicio"
    Cuando visualiza la sección principal (Hero Section)
    Entonces se encuentra la frase de propuesta de valor "Controla tu asma fácilmente"
    Y se encuentra un botón de llamada a la acción primario que dice "Comenzar" (o similar)

Feature: Llamada a la Acción para Médicos

  Scenario: Acceso a la Simulación del Panel Médico
    Dado que un potencial Médico o profesional de la salud revisa la página "¿Qué brindamos?"
    Cuando navega a la sección final de la página
    Entonces se muestra una Llamada a la Acción (CTA) prominente con el título "¿Listo para ver el Control en Acción?"
    Y se muestra un botón grande que permite "Ver Simulación del Panel Médico"

Feature: Formulario de soporte al cliente

  Scenario: Formulario de Soporte al Cliente
    Dado que el usuario navega a la sección "Contacto al cliente"
    Cuando revisa el contenido principal de la página
    Entonces se muestra un formulario que solicita "Nombre", "Correo Electrónico", "Asunto" y un "Mensaje"
    Y se muestra una casilla de verificación para aceptar la "política de privacidad" antes de que el botón "Enviar mensaje" pueda ser utilizado

Feature: Visualización del footer

  Scenario: Enlaces de Pie de Página
    Dado que el usuario está en la parte inferior de cualquier página pública
    Cuando visualiza el Pie de Página (Footer)
    Entonces encuentra enlaces de navegación con los títulos "¿Qué es AsthmaControl?", "Beneficios", "Cómo funciona" y "Contacto"
    Y encuentra enlaces a las redes sociales (Facebook, Instagram, Twitter) y a las "Política de Privacidad"