Feature: Formulario de contacto

  Scenario: El usuario envía un mensaje correctamente
    Given que el usuario se encuentra en la sección Contáctanos
    When completa los campos Nombre, Correo y Mensaje
    And presiona el botón Enviar
    Then el sistema muestra un mensaje "Gracias por tu mensaje"
    And los campos se limpian correctamente
