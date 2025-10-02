#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pytz",
# ]
# ///

import json
import os
import sys
from pathlib import Path
with open("logs/BUNDLE_ALWAYS.log", "a") as f:
    f.write("\nBUNDLE HOOK LLAMADO EN EVENTO\n")

# DEBUG: imprime cwd y si existe .claude ahí
print(f"DEBUG_HOOK: cwd={Path.cwd()} | .claude exists: {(Path.cwd() / '.claude').exists()} | session_id env: {os.environ.get('CLAUDE_SESSION_ID', '<VACIO>')}", file=sys.stderr)
sys.stderr.flush()

def write_to_context_bundle(record: dict, session_id: str):
    from datetime import datetime
    import pytz

    # path fijo: relativo al cwd SI existe .claude ahí (marcador de proyecto válido)
    bundles_dir = Path.cwd() / ".claude/agents/context_bundles"
    bundles_dir.mkdir(parents=True, exist_ok=True)

    # Formato: DIA_HORA_sessionID.jsonl (ej: SAT_12_592226a2c-c2c1-4d85-b68e-fd5e3822aa96.jsonl)
    # Usar zona horaria de Argentina (GMT-3)
    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    now = datetime.now(argentina_tz)
    day_abbr = now.strftime("%a").upper()  # SAT, SUN, MON, etc.
    hour = now.strftime("%H")  # 00-23

    bundle_filename = f"{day_abbr}_{hour}_{session_id}.jsonl"
    bundle_path = bundles_dir / bundle_filename

    with open(bundle_path, 'a') as f:
        json.dump(record, f)
        f.write('\n')

def main():
    try:
        # Dump EVERYTHING received by stdin a log para rastrear errores de pipeline real
        raw_stdin = sys.stdin.read()
        with open("logs/raw_stdin_bundle_hook.log", "a") as f:
            f.write(f"\n=== Nueva llamada ===\n{raw_stdin}\n")
        
        try:
            input_data = json.loads(raw_stdin)
        except Exception as e:
            with open("logs/hook_errors.log", "a") as f:
                f.write(f"Error decoding JSON in bundle_hook.py: {e}\nRaw: {raw_stdin}\n")
            input_data = {}

        # Busca session_id primero en JSON, si no en env. Si falta, aborta y loguea.
        session_id = input_data.get("session_id") or os.environ.get("CLAUDE_SESSION_ID", None)
        if not session_id:
            print("ERROR: No session_id (ni en JSON, ni en env)", file=sys.stderr)
            sys.exit(1)

        # Chequea que cwd/.claude exista. Si no, aborta (no mezcles bundles globales).
        if not (Path.cwd() / ".claude").exists():
            print("ERROR: No .claude/ in cwd, aborting bundle write (proyecto mal posicionado)", file=sys.stderr)
            sys.exit(1)

        operation_record = {}
        event_type = input_data.get('hook_event_name')

        # ---- LOGICA DE REGISTRO POR EVENTOS ----
        if event_type == 'UserPromptSubmit':
            operation_record = {
                "operation": "prompt",
                "prompt": input_data.get('prompt', '')
            }
        elif event_type == 'PostToolUse':
            tool_name = input_data.get('tool_name')
            tool_input = input_data.get('tool_input')
            if tool_name == 'Read':
                file_path = tool_input.get("file_path", "") if isinstance(tool_input, dict) else str(tool_input)
                operation_record = {"operation": "read", "file_path": file_path}
            elif tool_name == 'Write':
                operation_record = {
                    "operation": "write",
                    "file_path": tool_input.get("file_path", "") if isinstance(tool_input, dict) else "",
                    "content_length": len(tool_input.get("content", "")) if isinstance(tool_input, dict) else 0
                }
            elif tool_name in ['Edit', 'MultiEdit']:
                file_path = tool_input.get("file_path", "") if isinstance(tool_input, dict) else ""
                operation_record = {"operation": "edit", "file_path": file_path}
            elif tool_name == 'Bash':
                command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
                operation_record = {"operation": "bash", "command": command}
            else:
                # Para otros tools, guardamos info básica
                operation_record = {"operation": tool_name.lower(), "tool": tool_name}

        # Guarda solo si hay registro válido
        if operation_record:
            write_to_context_bundle(operation_record, session_id)
        sys.exit(0)
    except Exception as e:
        # log error detallado para debug
        with open("logs/hook_errors.log", "a") as f:
            f.write(f"Error en bundle_hook.py: {e}\n")
        sys.exit(0)

if __name__ == '__main__':
    main()
