Feature: Visualizar vista principal de paciente

  Scenario: Visualización de Progreso del Paciente
    Dado que el Paciente inicia sesión correctamente
    Cuando accede a su panel de inicio
    Entonces visualiza una tarjeta grande titulada "Progreso y Adherencia" que muestra el porcentaje de adherencia diaria
    Y visualiza otra tarjeta titulada "Meta Rápida" con un objetivo de progreso

Feature: Ver historial clínico

  Scenario: Consulta de Historial Detallado
    Dado que el Paciente navega a la sección "Historial"
    Cuando la vista carga el contenido
    Entonces visualiza una tabla con columnas que detallan los eventos registrados, incluyendo "Fecha y Hora", "Inhalaciones" y "Desencadenante"

Feature: Ver contenido educativo

  Scenario: Acceso al Plan de Acción de Asma
    Dado que el Paciente navega a la sección "Logística y Recursos"
    Cuando revisa la sección de Recursos Educativos
    Entonces encuentra y visualiza un elemento claramente etiquetado como "Guía: Plan de Acción de Asma" con su descripción

Feature: Visualizar calendario de paciente

  Scenario: Revisión de Citas Próximas
    Dado que el Paciente accede a la sección de Logística
    Cuando revisa la vista
    Entonces se visualiza un módulo con la tabla o lista titulada "Próximas Citas"
    Y se visualiza otra sección para la "Gestión de Medicamentos"