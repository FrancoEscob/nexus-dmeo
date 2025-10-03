# 🚀 Plan de la Nueva Demo de Pronunciación

## 1. Objetivos
1. Diseñar landing page limpia y profesional inspirada en `guide/capturas/image.png`.
2. Ofrecer demo libre (sin email obligatorio) con controles de abuso robustos.
3. Permitir selección de idioma nativo y objetivo usando todos los locales del pronouncer de Azure.
4. Mostrar resultados con visualizaciones amigables, profundidad técnica opcional y métricas completas (accuracy, fluency, completeness, prosody, fonemas).
5. Internacionalizar la interfaz (EN/ES inicialmente) y preparar traducciones futuras.
6. Centralizar el nuevo proyecto en `apps/nexus-languages` con subcarpetas `backend/` y `frontend/` para facilitar despliegue independiente.

## 2. Backlog de Trabajo

### 2.1 Backend
- **Locales de Azure:**
  - Crear script `scripts/fetch_azure_locales.py` para importar lista de locales soportados (REST `https://{region}.tts.speech.microsoft.com/cognitiveservices/voices/list` o documentación estática).
  - Guardar resultado en `backend/app/utils/azure_locales.json` con campos `native_language`, `target_language`, `locale`, `display_name`.
  - Endpoint `GET /api/azure-locales` con caching (Redis + memoria) y fallback estático.
- **Rate Limiting mejorado:**
  - Dividir lógica en capa de Redis (contador por IP+UA+lang) y Supabase para registro histórico.
  - Implementar política: 5 análisis/hora, 10/día, bloqueo con cola exponencial; enviar mensaje SSE `warning`.
- **Ingesta de métricas extendida:**
  - Exponer en `summary` datos agregados: conteo de fonemas problemáticos, prosody issues, duración total de pipeline.
  - Guardar JSON de Azure opcionalmente en bucket GCS (configurable) si se desea análisis posterior.
- **Localización en respuestas:**
  - Añadir claves normalizadas (`label`, `description_key`) para que el frontend traduzca sin re-formatear.
- **Observabilidad:**
  - Ajustar logs para incluir `native_language`, `target_language`, `utterance_source`.
- **Gemini:**
  - Confirmar disponibilidad del modelo `gemini-2.5-flash-lite` y su alias más reciente (`gemini-flash-lite-latest`) para mantener siempre la versión vigente mediante variable de entorno configurable.

### 2.2 Frontend
- **Arquitectura:** Mantener Next.js 14 App Router con Tailwind. Introducir `next-intl` para i18n, `zustand` o Context para estado de demo.
- **Landing:**
  - Hero con título, subtítulo, CTA "Probar demo" (scroll a sección demo).
  - Sección "Cómo funciona" con 3 pasos ilustrados.
  - Bloque de "Idiomas soportados" mostrando chips dinámicos (Azure locales). Opción de filtros.
  - Testimonios/opiniones placeholder.
- **Flujo de Demo:**
  - Paso 1: selector nativo/destino (menú dependiente, búsqueda).
  - Paso 2: carrusel de frases sugeridas (consulta a `/api/suggest-utterance`), botón para refrescar.
  - Paso 3: grabadora con waveform, control de 10 s, reproducción.
  - Paso 4: vista de análisis con timeline de SSE (barras de progreso animadas).
- **Visualizaciones:**
  - Meters circulares (SVG/Recharts) para scores principales con etiquetas humanizadas.
  - "Chips de mejora" horizontales; al expandir, mostrar detalle de `coach-card` con microcopys sencillos y botón "Ver explicación avanzada".
  - Sección "Tus próximos pasos" con 3 bullet points + CTA generar plan semanal.
- **i18n:**
  - Arquitectura de mensajes JSON (`en.json`, `es.json`).
  - Traducción básica para navegación, CTA, estados, feedback.
  - Posibilidad de traducir tips usando `coach-card` con `native_language` para generar texto localizado (futuro).
- **Accesibilidad:**
  - Contrastes AA, foco visible, soporte teclado.
  - Mensajes claros para errores/limitaciones (p.ej., rate limit).

### 2.3 Infraestructura / DevOps
- Revisar scripts GCP para incluir variable `SUPPORTED_LOCALES_CACHE_TTL` y credenciales de Redis gestionado si se usa.
- Añadir prueba `scripts/validate-gcp-deployment.sh` para nuevo endpoint `azure-locales`.
- Evaluar usar Cloud Tasks / PubSub si se guarda historial de análisis (fase futura).

## 3. Cronograma Tentativo
| Fase | Duración estimada | Entregables |
| --- | --- | --- |
| Investigación + Diseño detallado | 2-3 días | Wireframes, arquitectura de componentes, borrador de textos |
| Backend mejoras | 3-4 días | Endpoint locales, rate limiting nuevo, métricas extendidas, tests básicos |
| Frontend UI/UX | 5-7 días | Landing, flujo demo, visualizaciones, i18n inicial |
| QA + Deploy | 2 días | Pruebas manuales, ajuste Cloud Run, documentación en `/plan` |

## 4. Riesgos y Mitigaciones
- **Cobertura de locales Azure:** algunos combos no tienen pronunciación. Mantener lista curada y mostrar advertencia si análisis no soporta un par.
- **SSE en Cloud Run/Vercel:** asegurar keep-alive (`event: ping`) cada ≤30 s.
- **Costos Azure/Gemini:** limitar longitud de audio, restringir reintentos y monitorizar uso (añadir contador visible).
- **Sin branding definido:** definir guía de estilo mínima (paleta, tipografía) en `ui_concepts.md` para consistencia.

## 5. Próximos Pasos Inmediatos
1. Consolidar locales Azure y validar endpoint.
2. Diseñar wireframes para landing y demo (low fidelity) en `ui_concepts.md`.
3. Rediseñar servicio de rate limiting y pruebas unitarias.
4. Implementar esqueleto de i18n en Next.js antes de remaquetar UI.

> **Nota:** Este plan se centrará en mantener cambios iterativos, evitando refactors masivos hasta tener la nueva UX probada. Cada subfase debe incluir revisiones contigo antes de codificar componentes complejos.

## 6. Actualizaciones recientes
- **2025-10-03:** Landing inicial e i18n completados; backlog reorganizado priorizando locales Azure, rate limiting y flujo demo interactivo listos para la siguiente iteración. Se abrió `plan/progress_log.md` para registrar avances puntuales.
- **2025-10-03 (tarde):** Endpoint de locales desplegado, script de sincronización Azure, y rate limiting in-memory con endpoint de prueba y tests listos para extender a Redis/Cloud Run.
- **2025-10-03 (noche):** UI interactiva preliminar disponible: selector de idiomas, frases sugeridas y chequeo de cuota conectados a la API para preparar la integración de grabación y resultados.
