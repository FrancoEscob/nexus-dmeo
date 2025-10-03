# 📚 X-DEMO: Resumen de la Versión Anterior

## 1. Arquitectura General
- **Backend:** FastAPI en `guide/X-DEMO/backend/app/main.py` con middlewares de CORS, métricas de rendimiento y cabeceras de seguridad.
  - Endpoints clave: `/api/analyze-pronunciation` (SSE con Azure Speech), `/api/suggest-utterance`, `/api/waitlist`, `/api/demo-optin`, `/api/coach-card`, `/api/coach-cards`, `/api/teaser`, `/api/weekly-plan`.
  - Servicios auxiliares en `app/services`: análisis de audio (`analysis_service.py`), caché Redis, deduplicación, LLM Gemini, base de datos, límites de uso, lista de espera.
  - Configuración en `app/utils/config.py` con lectura de variables de entorno (.env) y creación de `TMP_DIR` para archivos temporales.
- **Frontend:** Next.js 14 (App Router) en `guide/X-DEMO/frontend` con Tailwind, Framer Motion y componentes desacoplados para grabación, visualización de scores y feedback.
- **Storage y Datos:** Uso de Supabase (Postgres + PostgREST) para registrar waitlist, demo opt-in y límites de uso. Redis se emplea como caché (requerido en producción).

## 2. Flujo de Pronunciation Assessment
1. **Subida y Validación:** `/api/analyze-pronunciation` recibe `UploadFile` y texto de referencia opcional; controla tipos MIME y tamaño (<10 MB).
2. **Límites de Uso:** `rate_limit_service.check_and_increment` aplica límites diarios y de por vida usando hash de IP + Supabase (`usage_log`).
3. **Normalización de Audio:** `analysis_service.convert_and_trim_to_wav` usa `ffmpeg` para convertir a PCM mono 16 kHz, recortar silencios y limitar a 10 s.
4. **Transcripción:** Si el frontend no envía `reference_text`, se ejecuta Azure STT (`asr_stream_from_file`).
5. **Pronunciation Assessment:** `pronunciation_assessment_stream` aplica `speechsdk.PronunciationAssessmentConfig` (granularidad fonema, miscue y prosodia opcional).
6. **Streaming de Resultados:** `analyze_pronunciation_sse` publica eventos SSE (`status`, `prosody_chunk`, `scores`, `summary`, `artifact`, `metric`, `complete`). También guarda JSON crudo del SDK en disco temporal.
7. **Feedback Avanzado:** Si `ENABLE_LEGACY_REPORT` está activo, se invoca Gemini (`generate_gemini_feedback`) para texto extenso.

## 3. Scripts y Despliegue
- **Google Cloud Run (Preferido):**
  - `scripts/gcp-setup.sh`: crea proyecto, habilita APIs, bucket y service account (`nexus-demo-sa`).
  - `scripts/gcp-deploy.sh`: compila imagen con Cloud Build usando `backend/Dockerfile.gcp`, despliega a Cloud Run (2 Gi RAM, 1 CPU, máx. 100 instancias) y realiza health check.
  - `scripts/gcp-set-env-vars.sh`: sincroniza variables `.env` al servicio Cloud Run.
- **Azure (Alternativa):** Scripts `azure-setup.sh`, `set-env-vars.sh`, `deploy.sh` para App Service.
- **Frontend:** Se sugiere Vercel; requiere `NEXT_PUBLIC_BACKEND_URL` apuntando al servicio Cloud Run.
- **Docker Compose:** Archivo `docker-compose.yml` lanza frontend, backend y dependencias para desarrollo local.

## 4. Dependencias y Configuración
- **APIs Externas:** Azure Speech (`SPEECH_KEY`, `SPEECH_REGION`), Google Gemini (`GEMINI_API_KEY`), Supabase (`SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`).
- **Prompts/LLM:** `app/services/llm_service.py` define prompts para análisis corto, coach cards y planes semanales.
- **Logging:** `app/utils/simple_logger.py` genera logs estructurados para requests, costos Azure/Gemini y métricas.
- **Limitaciones Detectadas:**
  - Rate limit basado en Supabase falla si la tabla no existe o hay latencia → los usuarios pueden evadir límites.
  - UI actual muestra feedback técnico difícil de interpretar (cards densas, jerga fonética).
  - No hay localización en frontend; textos solo en inglés.

## 5. Aprendizajes Clave
- El pipeline de Azure funciona pero necesita mejor UX (copy y visualizaciones más amigables).
- La arquitectura es modular, lo que facilita insertar nuevos endpoints (p. ej., listar locales soportados).
- La infraestructura Cloud Run ya probada; mantener scripts reducirá esfuerzos futuros.
- Es vital reforzar rate limiting y monitoreo antes de abrir la demo libremente.
