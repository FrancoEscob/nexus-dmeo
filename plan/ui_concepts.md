# 🎨 Conceptos de UI y UX

## 1. Principios de Diseño
- **Clean & Professional:** Fondo claro con acentos en azul petróleo (#1F3C88) y verde suave (#3BC9A7). Uso de gradientes tenues para hero.
- **Family-friendly:** Iconografía redondeada, ilustraciones amigables (personas practicando idiomas). Tipografías sugeridas: `Inter` para texto, `Playfair Display` o `Fraunces` para titulares.
- **Claridad lingüística:** Textos cortos, evitar jerga fonética salvo en secciones avanzadas; proporcionar tooltips con explicaciones simples.
- **Feedback inmediato:** Animaciones suaves (<300 ms) para transiciones entre etapas y loaders circulares.

## 2. Estructura de la Landing
1. **Hero (Fold inicial):**
   - Columna izquierda con título (H1), subtítulo y CTA "Probar demo gratis".
   - Columna derecha: mockup de dashboard (basado en `capturas/image.png`) con gauges circulares y tarjetas apiladas.
2. **Cómo funciona:** Tres pasos con íconos (Preparar frase → Grabar → Recibir feedback). Cada paso con copy corto.
3. **Idiomas soportados:** Grid de chips filtrables por nombre, bandera y código de Azure (`en-US`, `es-ES`, `fr-FR`, etc.).
4. **Beneficios / Testimonios:** Tarjetas con citas breves orientadas a profesionales.
5. **CTA final + Waitlist:** Banner con formulario email/nombre (opcional) conectado a `/api/waitlist`.

## 3. Flujo de Demo
### 3.1 Paso 1: Selección de Idiomas
- Dropdowns con búsqueda (Combobox). Mostrar nombre amigable (`Spanish (Spain)`) y código.
- Tooltip: "Tu idioma nativo nos ayuda a personalizar el coaching".

### 3.2 Paso 2: Frases sugeridas
- Carrusel horizontal con tarjetas grandes (color pastel) que muestran frase, contexto y botón "Usar".
- Botón "Nueva frase" que llama a `/api/suggest-utterance`.
- Campo `textarea` con contador de caracteres para personalizar.

### 3.3 Paso 3: Grabación
- Componente central tipo tarjeta con waveform animado (p.ej., `wavesurfer.js` o canvas simple).
- Botón primario toggles "Grabar"/"Detener"; mostrar tiempo transcurrido y límite 10 s.
- Botones secundarios para reproducir, borrar y subir archivo (fallback).

### 3.4 Paso 4: Resultados
- **Layout:** Dos columnas en desktop, stack en mobile.
  - Izquierda: Gauges (Accuracy, Fluency, Completeness, Prosody) con colores (#2ECC71 alto, #F1C40F medio, #E74C3C bajo).
  - Derecha: `ImprovementCarousel` con tarjetas expandibles.
- **Detalle adicional:** Acordeón "Ver análisis avanzado" mostrando tabla de palabras problemáticas con explicación simple y botón "Más detalles" que abre modal con JSON formateado para usuarios avanzados.
- **CTA final:** Botón "Plan de 30 días" que llama a `/api/weekly-plan` y muestra resumen.

## 4. Componente: ImprovementCarousel
- Tarjeta base: Ícono redondo, título amigable ("Acentúa las vocales largas"), score resaltado (p.ej. 62/100).
- Al hacer tap/click: se expande para mostrar pasos prácticos, palabras sugeridas, audio/fonema (si se dispone).
- Arrows o scroll horizontal; en mobile usar snaps.
- Soportar traducción del contenido (claves i18n). Indicar `native_language` al solicitar coach card para personalizar.

## 5. Estado y Notificaciones
- Barra superior pegajosa mostrando progreso (chips: Preparar → Grabar → Analizar → Resultados).
- Toasts para errores (p.ej., fallo de micrófono, límite alcanzado) con mensajes empáticos y posibles soluciones.
- Indicador de rate limiting: mini-modal con contador y sugerencias ("Vuelve a intentarlo en 15 minutos").

## 6. Internacionalización
- Switch EN/ES en navbar; recordatorio de idioma actual en footer.
- Diccionario de strings clave: CTA, labels, estados, mensajes de error.
- Ajuste de copy en feedback según idioma; fallback a inglés si `coach-card` no soporta traducción.

## 7. Recursos Visuales
- Ilustraciones vectoriales (Storyset, unDraw) en tonos acordes.
- Iconos de `Phosphor Icons` o `Heroicons` por su consistencia y variantes filled/outline.
- Utilizar sombras suaves (`shadow-lg` con blur alto) y bordes redondeados (`rounded-3xl`) para look moderno.

## 8. Próximos Entregables de Diseño
- Wireframes low-fi para cada paso (pueden ir en Figma o como bocetos anotados en este archivo).
- Lista de componentes reutilizables para documentar en Storybook (si se decide implementar).
- Tabla de tokens de diseño inicial: colores, tipografías, espaciados.
