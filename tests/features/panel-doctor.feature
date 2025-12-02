Feature: Visualizar vista principal de médico

  Scenario: Resumen del Dashboard Médico
    Dado que el Médico inicia sesión correctamente
    Cuando accede a su panel de inicio (Dashboard)
    Entonces visualiza cuatro botones o tarjetas de acceso rápido con los títulos "Ver alertas", "Lista de pacientes", "Registrar paciente" y "Mensajes"

Feature: Registrar paciente

  Scenario: Acceso al Formulario de Registro
    Dado que el Médico está en el Dashboard o en la lista de Pacientes
    Cuando navega a la sección "Registrar Paciente"
    Entonces se muestra un formulario completo organizado en secciones (ej. Información Personal, Datos Médicos, Contacto Cuidador)
    Y el formulario finaliza con un botón de acción primario que dice "Registrar Paciente"

Feature: Marcar alertas

  Scenario: Gestión de Estado de Alerta por el Médico
    Dado que el Médico accede a la sección de Alertas Críticas
    Cuando revisa una alerta específica de un paciente (ej. Omisión de Dosis)
    Entonces la tarjeta de alerta contiene botones para gestionar su estado: "Marcar como atendida" y "Marcar en Seguimiento"

Feature: Evaluar y recomendar al paciente

  Scenario: Añadir Evaluación Médica al Reporte
    Dado que el Médico revisa el reporte de un paciente
    Cuando navega a la sección "Evaluación y recomendaciones"
    Entonces se muestra un área de texto grande (textarea) con un placeholder para escribir las conclusiones y recomendaciones médicas