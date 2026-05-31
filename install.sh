#!/usr/bin/env bash
set -euo pipefail

echo "Installing wallpaper changer"

# --- paths ---
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYSTEMD_DIR="$HOME/.config/systemd/user"

# --- deps check ---
if ! command -v systemctl &>/dev/null; then
    echo "❌ systemctl not found"
    exit 1
fi

if ! command -v python3 &>/dev/null; then
    echo "❌ python3 not found"
    exit 1
fi

if ! command -v pipx &>/dev/null; then
    echo "❌ pipx not found"
    echo "Install: python3 -m pip install --user pipx && python3 -m pipx ensurepath"
    exit 1
fi

# --- install app FIRST ---
echo "📦 Installing package via pipx..."
pipx install . --force

# --- get installed python + script paths ---
PYTHON_PATH="$(command -v python3)"
SCRIPT_PATH="$(pipx list --short | grep wallpaperchanger || true)"

# fallback safe check
if [ -z "$SCRIPT_PATH" ]; then
    SCRIPT_PATH="wallpaperchanger"
fi

# --- systemd ---
mkdir -p "$SYSTEMD_DIR"

echo "⚙️ Creating systemd files..."

escape_sed() {
    printf '%s' "$1" | sed 's/[&|]/\\&/g'
}

PYTHON_ESC=$(escape_sed "$PYTHON_PATH")
SCRIPT_ESC=$(escape_sed "$SCRIPT_PATH")

sed \
  "s|__PYTHON__|${PYTHON_ESC}|g; s|__SCRIPT__|${SCRIPT_ESC}|g" \
  "$PROJECT_DIR/systemd/wallpaper.service" \
  > "$SYSTEMD_DIR/wallpaper.service"

cp -f "$PROJECT_DIR/systemd/wallpaper.timer" \
      "$SYSTEMD_DIR/wallpaper.timer"

# --- systemd reload ---
echo "🔄 Reloading systemd..."
systemctl --user daemon-reload

echo "▶️ Enabling timer..."
systemctl --user enable --now wallpaper.timer

# --- verify ---
if ! systemctl --user is-enabled wallpaper.timer &>/dev/null; then
    echo "❌ Failed to enable timer"
    exit 1
fi

# --- done ---
echo ""
echo "🎉 Installed successfully!"
echo ""
echo "👉 Run:"
echo "wallpaperchanger --next"
echo ""
echo "👉 Check timers:"
echo "systemctl --user list-timers"
echo ""
echo "👉 Logs:"
echo "journalctl --user -u wallpaper.service -f"
