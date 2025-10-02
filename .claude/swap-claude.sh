#!/bin/bash

CONFIG_DIR="$HOME/Desktop/Language-Learning-Research/.claude"
ZAI_CONFIG="$CONFIG_DIR/settings_zai.json"
CLAUDE_CONFIG="$CONFIG_DIR/settings_claude.json" 
GROK_CONFIG="$CONFIG_DIR/settings_grok.json"
SETTINGS="$CONFIG_DIR/settings.json"

case "$1" in
  "zai")
    pkill -f "claude-code-router" 2>/dev/null
    cp "$ZAI_CONFIG" "$SETTINGS"
    echo "✅ Usando Z.AI GLM-4.5"
    ;;
  "claude")
    pkill -f "claude-code-router" 2>/dev/null
    cp "$CLAUDE_CONFIG" "$SETTINGS"
    echo "✅ Usando cuenta oficial Claude"
    ;;
  "grok")
    cp "$GROK_CONFIG" "$SETTINGS"
    if ! curl -s http://localhost:3456/status > /dev/null 2>&1; then
      echo "🚀 Iniciando router para Grok 4 Fast..."
      ccr start > /dev/null 2>&1 &
      sleep 3
    fi
    echo "✅ Usando Grok 4 Fast GRATIS (2M context)"
    ;;
  *)
    echo "Uso: $0 [zai|claude|grok]"
    exit 1
    ;;
esac
