---
description: "Carga y reproduce las operaciones de un context bundle para restaurar una sesión de agente."
allowed-tools: Read, Bash
argument-hint: "[bundle-path]"
---

# Cargar Context Bundle

Tu tarea es restaurar el estado de una sesión de agente anterior leyendo un archivo de "context bundle". El usuario te proporcionará la ruta al archivo.

## Workflow

1.  **Leer el Bundle:** Lee el contenido completo del archivo `.jsonl` especificado en la ruta del bundle.
2.  **Analizar Operaciones:** Procesa el archivo línea por línea. Cada línea es una operación JSON.
3.  **Deduplicar Operaciones de Lectura:** Es muy importante que si varias operaciones `read` apuntan al mismo `file_path`, solo lo leas UNA VEZ para ser eficiente.
4.  **Ejecutar Operaciones:**
    *   Para cada operación `read` única, lee el archivo correspondiente para cargar su contenido en tu contexto actual.
    *   Para las operaciones `prompt`, muéstralas como parte de tu resumen para entender el flujo de la conversación.
    *   Ignora las operaciones `write` por ahora, ya que no queremos reescribir archivos, solo entender el contexto.
5.  **Reportar Resumen:** Una vez que hayas procesado todas las operaciones, proporciona un resumen conciso de lo que hizo el agente en la sesión anterior, incluyendo:
    *   El prompt principal que inició la sesión (`/prime` o `/prime_cc`).
    *   Una lista de los archivos clave que fueron leídos (`README.md`, `settings.json`, etc.).
    *   Un resumen de alto nivel del objetivo de la sesión.