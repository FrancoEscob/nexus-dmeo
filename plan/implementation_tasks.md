# ✅ Backlog Inicial de Implementación

## ✅ Completado al 2025-10-03
- Configuración i18n en Next.js con soporte EN/ES y selector visible en la landing.
- Hero + sección "Cómo funciona" alineadas con la estética de la referencia.
- Endpoint `/api/v1/locales` con dataset estático inicial y script para sincronizar con Azure.
- Middleware de rate limiting con endpoint de prueba `/api/v1/rate-limit/probe` y tests unitarios.
- Sección base de demo interactiva con selector de idiomas, sugerencias y chequeo de cuota.

## 🔄 Backlog activo

| Prioridad | Tarea | Resultado Esperado | Notas |
| --- | --- | --- | --- |
| Alta | Montar flujo demo interactivo (grabación/subida/resultados) | Probar audio ≤10s y renderizar feedback accesible | Selector + cuota listos; falta grabación, subida y visualización de resultados |
| Alta | Scaffold servicios Azure Speech + Gemini | Clientes con manejo de credenciales y errores listo para conectar endpoints | Definir interfaces y pruebas unitarias básicas |
| Media | Gauges e ImprovementCarousel | Visualizaciones accesibles con datos mock | Ajustar theming y animaciones |
| Media | Integración de métricas extendidas | Mostrar breakdown de fonemas, prosodia, tiempos | Requiere updates en backend summary |
| Media | Handshake frontend-backend (mocks → llamadas reales) | Flujo de demo consumiendo endpoints reales | Alternar entre fixtures locales y API remota |
| Media | Dockerfile + script Cloud Run (frontend/backend) | Despliegue reproducible con variables `.env` documentadas | Añadir verificación local (`docker compose up`) |
| Baja | Guardado opcional en GCS | Persistir JSON y audios para análisis futuro | Activar mediante variable de entorno |
| Baja | Storybook / Doc de componentes | Biblioteca de UI para acelerar iteraciones | Solo si hay capacidad extra |

### Checklist Transversal
- [ ] Revisar costos estimados de Azure/Gemini tras la apertura del demo.
- [ ] Añadir pruebas unitarias/integ en backend (rate limit, locales, SSE).
- [ ] Validar accesibilidad (uso teclado, lectores de pantalla).
- [ ] Configurar monitorización (por ej. Cloud Logging filtros por endpoint).
