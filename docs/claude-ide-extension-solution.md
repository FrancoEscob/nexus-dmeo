# Solución para Integrar Alias Personalizado con Extensión Claude Code IDE

## Problema Identificado

Tu alias `cld` genera session IDs personalizados con formato:
```bash
alias cld='export CLAUDE_SESSION_ID="SAT_$(date +%y_%m_%d-%H_%M_%S)-$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 8)"; claude'
```

Pero la extensión de Claude Code para Cursor/VS Code inicia Claude directamente con `claude` sin pasar por tu alias, lo que causa que los hooks no funcionen correctamente debido a que no se establece `CLAUDE_SESSION_ID`.

## Descubrimiento Clave

La extensión oficial de Claude Code v2.0.1 tiene configuración específica para variables de entorno:

```json
{
  "claude-code.environmentVariables": [
    {
      "name": "CLAUDE_SESSION_ID",
      "value": "valor-estático"
    }
  ]
}
```

**Limitación:** Esta configuración solo acepta valores estáticos, no puede ejecutar comandos dinámicamente.

## Soluciones Propuestas

### Opción 1: Configuración Estática (Rápida pero Limitada)

Para VS Code/Cursor, agrega a `.vscode/settings.json`:

```json
{
  "claude-code.environmentVariables": [
    {
      "name": "CLAUDE_SESSION_ID",
      "value": "SAT_static-session-for-debugging"
    }
  ],
  "claude-code.useNodeExecution": false
}
```

**Ventajas:**
- Fácil de configurar
- Funciona inmediatamente

**Desventajas:**
- Session ID no cambia (no ideal para producción)
- Los hooks siempre escribirán al mismo bundle

### Opción 2: Script Wrapper (Recomendada)

Usa los scripts que he creado:

#### 2.1 Script Generador de Session ID
```bash
./scripts/generate-claude-session.sh
```

#### 2.2 Script Wrapper Principal
```bash
./scripts/claude-with-session.sh
```

#### 2.3 Configuración de Tasks en VS Code

Ejecuta `Ctrl+Shift+P` → "Tasks: Run Task" → "Start Claude Code with Custom Session"

### Opción 3: Hook Modificado (Avanzada)

Modificar el bundle hook para generar session IDs automáticamente si no existe:

```python
# En bundle_hook.py, modificar la sección de session_id:
if not session_id:
    # Generar session ID automáticamente si no existe
    from datetime import datetime
    import uuid
    now = datetime.now()
    session_id = f"IDE_{now.strftime('%y_%m_%d-%H_%M_%S')}-{str(uuid.uuid4())[:8]}"
```

### Opción 4: Integración con Terminal (Híbrida)

1. **Abre la terminal integrada de VS Code/Cursor**
2. **Ejecuta el script wrapper antes de usar la extensión:**
   ```bash
   source scripts/claude-with-session.sh
   ```
3. **La extensión usará la variable de entorno establecida**

## Pasos para Implementar la Solución Recomendada

### 1. Configuración Inmediata

```bash
# Probar el script wrapper
bash scripts/claude-with-session.sh

# Verificar que se exporta la variable
echo $CLAUDE_SESSION_ID
```

### 2. Configurar VS Code/Cursor

Abrir configuración de VS Code/Cursor y agregar:

```json
{
  "claude-code.environmentVariables": [
    {
      "name": "CLAUDE_SESSION_ID",
      "value": "IDE_${workspaceFolderBasename}-${timestamp}"
    }
  ]
}
```

### 3. Crear Alias Mejorado

Actualiza tu alias para que sea compatible con ambas formas de uso:

```bash
# En .bashrc o .zshrc
alias cld='export CLAUDE_SESSION_ID="SAT_$(date +%y_%m_%d-%H_%M_%S)-$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 8)"; echo "Session ID: $CLAUDE_SESSION_ID"; claude'

# Nuevo alias para uso con IDE
alias cld-ide='source ~/Desktop/Language-Learning-Research2/scripts/claude-with-session.sh'
```

## Verificación del Funcionamiento

### 1. Verificar Hook Functionamiento

```bash
# Generar un session ID y probar hook
export CLAUDE_SESSION_ID="SAT_test-$(date +%s)"
echo '{"session_id":"SAT_test-123","hook_event_name":"UserPromptSubmit","prompt":"test"}' | uv run .claude/hooks/bundle_hook.py

# Verificar que se creó el bundle
ls -la .claude/agents/context_bundles/
```

### 2. Verificar Integración con IDE

1. Abre VS Code/Cursor
2. Ejecuta `Ctrl+Shift+P` → "Claude Code: Open in New Tab"
3. Verifica en los logs que el hook se ejecuta con el session ID correcto

## Recomendación Final

**Para desarrollo diario:** Usa la **Opción 2 (Script Wrapper)** con la configuración de tasks.

**Para pruebas rápidas:** Usa la **Opción 1 (Configuración Estática)**.

**Para máxima compatibilidad:** Implementa la **Opción 3 (Hook Modificado)** como fallback.

## Archivos Creados

- `scripts/generate-claude-session.sh` - Generador de session IDs
- `scripts/claude-with-session.sh` - Wrapper principal
- `.vscode/settings.json` - Configuración de VS Code
- `.vscode/tasks.json` - Tasks personalizadas
- `docs/claude-ide-extension-solution.md` - Esta documentación

Todos estos archivos están configurados para trabajar juntos y proporcionar una solución completa al problema de integración entre tu alias personalizado y la extensión de Claude Code.