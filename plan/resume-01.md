# Resumen detallado del estado actual (octubre 2025)

## 1. Contexto general del flujo de demo
1. **Backend esperado**: recibir audio del usuario, procesarlo con Azure Speech Pronunciation Assessment, pasar el JSON resultante a Gemini y producir tarjetas de feedback amigables.
2. **Frontend actual**: proveer la landing inspirada en la referencia, permitir preparar la práctica (idiomas, frase), revisar disponibilidad (rate limit) y luego activar el flujo de grabación/carga de audio que aún falta integrar.

## 2. Lo que ya está construido

### 2.1 Backend
- **Endpoints**:
  - `/api/v1/status`: health check.
  - `/api/v1/locales`: lista cacheable de locales de Azure (cargada desde `app/data/azure_locales.json`, con script `scripts/fetch_azure_locales.py` para sincronizarla desde Azure).
  - `/api/v1/rate-limit/probe`: consulta de cuota restante usando IP + UserAgent + idioma objetivo (servicio de rate limiting in-memory configurable por variables).
- **Servicios**:
  - `RateLimitRule`/`RateLimiter`: aplica reglas 5/hora y 10/día, emite errores 429 si se supera.
  - `AzureLocale` schemas: estructuran la lista de idiomas y permiten filtrado futuro.
- **Tests**:
  - `tests/test_rate_limit.py`: confirma comportamiento del rate limit (dentro del límite, bloqueo tras exceder, reset).
- **Configuración**:
  - `.env` admite `RATE_LIMIT_*` y banderas para activar/desactivar.
  - Dependencias actualizadas (FastAPI, pydantic-settings, httpx para script).

### 2.2 Frontend
- **Landing**: hero, flujo visual, destacados de idiomas, sección “próximamente”, todo con Next.js 14 App Router + Tailwind.
- **i18n**: rutas `/[locale]/...`, mensajes en `src/i18n/messages/en.json` y `es.json`, `LanguageSwitcher` integrado.
- **Sección demo interactiva** (nueva `DemoExperienceSection`):
  - Carga locales desde `/api/v1/locales` al montar la página.
  - Permite elegir idioma objetivo y nativo, usando la data real del backend.
  - Genera frases sugeridas (mock local) por idioma para practicar.
  - Botón “Nueva sugerencia” rota la frase.
  - Botón “Revisar disponibilidad” golpea `/api/v1/rate-limit/probe` y muestra:
    - Intentos restantes (cuando hay cuota) y estilo “success”.
    - Mensaje de espera (minutos) si se superan los 5 análisis/hora.
    - “Límite diario” si se agotaron los 10 del día.
    - Mensaje de error en casos inesperados.
  - Botón “Iniciar práctica” (placeholder): reservará el espacio donde implementaremos grabación/subida real.
  - Etiquetas y mensajes localizados en EN/ES.

### 2.3 Documentación
- `plan/progress_log.md`: registra avances por fecha (landing, endpoints, rate limit, demo interactiva, etc.).
- `plan/implementation_tasks.md`: backlog actualizado (tareas completas vs. pendientes con prioridades).
- `plan/new_demo_blueprint.md`: plan maestro con historial de hitos (landing, locales, rate limit, demo interactiva preliminar).
- `plan/previous_version_summary.md` y `plan/ui_concepts.md`: resumen del demo anterior y lineamientos visuales.

## 3. Sobre “Voces disponibles”
- El JSON de Azure incluye información de voces Neural TTS por idioma. Se mostraron como chips informativos para que el usuario supiera qué voces modelo existen.
- No son esenciales para el MVP de pronunciación (el usuario sube su propio audio). Podemos quitarlos si preferimos enfocarnos en el flujo de análisis.

## 4. Botones “Revisar disponibilidad” vs. “Iniciar práctica”
- **Revisar disponibilidad**: pre-chequea la cuota antes de grabar, evitando que el usuario llegue al final del proceso y reciba un 429. Si está bloqueado, se informa tiempo de espera o límite diario.
- **Iniciar práctica**: botón placeholder; en el futuro disparará la grabación/carga de audio.
  1. Selecciona idiomas + frase.
  2. Opcionalmente revisa disponibilidad.
  3. “Iniciar práctica” mostrará el grabador/input.
  4. Tras enviar audio y procesar, se mostrarán métricas y feedback.

## 5. Qué falta por construir

### 5.1 Backend pendiente
- Endpoint real de evaluación (`POST /api/v1/pronunciation` o similar) que reciba audio ≤ 10 s, llame a Azure, procese respuesta, invoque Gemini y devuelva JSON de feedback accesible.
- Integra rate limiting real en ese endpoint (reutilizando el servicio actual).
- Opcional: persistencia (GCS/Supabase) y logging/monitorización.
- Scripts Docker + despliegue Cloud Run.

### 5.2 Frontend pendiente
- Grabador o input de archivo con límite 10 s, waveform opcional, controles (start/stop/play/retry).
- Gestión de estados (grabando, procesando, terminado) y transiciones.
- Consumo del endpoint real: enviar audio, manejar respuesta, mostrar gauges y tarjetas.
- Accesibilidad reforzada (focus, screen readers) y mensajes de rate limit cuando surja durante el envío real.
- Integrar métricas visuales reales en lugar del preview estático.

### 5.3 Integraciones y soporte
- Configurar Azure Speech (keys, región, manejo de errores).
- Confirmar modelo Gemini 2.5 Flash Lite, diseñar prompt e integrar respuesta.
- Configurar despliegue Cloud Run (Dockerfiles, variables de entorno, pipelines).

### 5.4 Documentación / QA
- Mantener `progress_log.md` y `implementation_tasks.md` con cada avance.
- Definir suite de pruebas (unitarias en backend/frontend, pruebas manuales, eventualmente pruebas end-to-end).

## 6. Siguientes pasos recomendados
1. Implementar captura/subida de audio en frontend (con validaciones de duración).
2. Crear endpoint de evaluación en backend (mock inicial + integración real con Azure/Gemini).
3. Crear componentes de visualización para los resultados (gauges, tarjetas amigables con traducciones).
4. Preparar despliegue y pruebas automatizadas.

## 7. Resumen rápido
- **Hecho**: Scaffolding completo, i18n, landing alineada con referencia, backend locales + rate limit + tests, sección de demo interactiva que precarga configuración y chequea la cuota.
- **Pendiente**: Todo el pipeline de audio (captura → envío → Azure → Gemini → feedback) y scripts de deploy.
- **Observación**: Si la sección de “Voces disponibles” no aporta, se puede eliminar para mantener foco en la experiencia de práctica.
