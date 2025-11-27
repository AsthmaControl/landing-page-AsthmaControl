Feature: Visualizar reporte del paciente


  Scenario: El doctor visualiza correctamente el reporte de un paciente
    Given que el usuario Médico "Dr. Pérez" inicia sesión con sus credenciales válidas
    And el paciente "Juan López" tiene reportes disponibles
    When el doctor accede a "Lista de pacientes" y selecciona "Ver reporte" del paciente "Juan López"
    Then se muestra el reporte del paciente
    And el reporte incluye nombre del paciente, un historial de adherencia y síntomas y gráficos de seguimiento.

