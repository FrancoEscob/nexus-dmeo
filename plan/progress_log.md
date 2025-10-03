# 📘 Bitácora de progreso

## 2025-10-03
- ✅ Landing inicial lista con hero, flujo ilustrativo y selector de idioma (EN/ES) soportado por `next-intl`.
- ✅ Backend FastAPI arrancado con endpoints de salud y configuración mediante `pydantic-settings`.
- ✅ Endpoint `/api/v1/locales` creado con datos cacheables y script `scripts/fetch_azure_locales.py` para sincronizar la lista desde Azure.
- ✅ Limitar peticiones con servicio in-memory + endpoint `/api/v1/rate-limit/probe` y pruebas unitarias.
- ✅ Sección de demo interactiva con selector de idiomas, frase sugerida y verificación de cuota directamente desde el backend.
- 🔜 Próximos focos: integrar servicios Azure Speech/Gemini, preparar Cloud Run y visualizaciones accesibles.
