#!/usr/bin/env bash
set -e

echo "📦 Installing wallpaper changer..."

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
SYSTEMD_DIR="$HOME/.config/systemd/user"
LOCAL_BIN="$HOME/.local/bin"

PYTHON_PATH="$(command -v python3)"
SCRIPT_PATH="$PROJECT_DIR/main.py"

# --- проверки ---
if [ -z "$PYTHON_PATH" ]; then
	echo "❌ python3 not found"
	exit 1
fi

if ! command -v systemctl &>/dev/null; then
	echo "❌ systemctl not found"
	exit 1
fi

# --- systemd ---
mkdir -p "$SYSTEMD_DIR"

echo "⚙️ Creating systemd files..."

sed "s|__PYTHON__|$PYTHON_PATH|g; s|__SCRIPT__|$SCRIPT_PATH|g" \
	"$PROJECT_DIR/systemd/wallpaper.service" \
	>"$SYSTEMD_DIR/wallpaper.service"

cp "$PROJECT_DIR/systemd/wallpaper.timer" \
	"$SYSTEMD_DIR/wallpaper.timer"

echo "🔄 Reloading systemd..."
systemctl --user daemon-reload

echo "✅ Enabling timer..."
systemctl --user enable --now wallpaper.timer

# --- CLI ---
echo "🔗 Setting up CLI..."

chmod +x "$SCRIPT_PATH"
mkdir -p "$LOCAL_BIN"

ln -sf "$SCRIPT_PATH" "$LOCAL_BIN/wallpaperchanger"

echo "✅ CLI installed to $LOCAL_BIN"

# PATH check
if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
	echo ""
	echo "⚠️  Add this to your shell config (~/.bashrc or ~/.zshrc):"
	echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

# --- done ---
echo ""
echo "🎉 Installed! Wallpaper changer is running."
echo ""
echo "👉 Run:"
echo "wallpaperchanger --next"
echo ""
echo "👉 Check timers:"
echo "systemctl --user list-timers"
echo ""
echo "👉 Logs:"
echo "journalctl --user -u wallpaper.service -f"
