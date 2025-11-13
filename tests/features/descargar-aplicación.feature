Feature: Descarga motivadora de la aplicación móvil

  Scenario: El usuario descarga la aplicación desde el Landing Page
    Given que el usuario se encuentra en la sección inicial de la Landing Page
    When recorre toda la sección principal y presiona en el botón de "Descargar aplicación"
    Then se redirige al usuario hacia arriba y los botones de descargar a App Store y Google Play se resaltan agrandandose
