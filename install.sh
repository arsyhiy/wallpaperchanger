#!/usr/bin/env bash
set -euo pipefail

echo "Installing wallpaper changer"

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYSTEMD_DIR="$HOME/.config/systemd/user"

if ! command -v systemctl &>/dev/null; then
    echo "systemctl not found"
    exit 1
fi

if ! command -v python3 &>/dev/null; then
    echo "python3 not found"
    exit 1
fi

if ! command -v pipx &>/dev/null; then
    echo "pipx not found"
    echo "Install: python3 -m pip install --user pipx && python3 -m pipx ensurepath"
    exit 1
fi

echo " Installing package via pipx"
pipx install . --force


mkdir -p "$SYSTEMD_DIR"

echo "Creating systemd files"


cp -f "$PROJECT_DIR/systemd/wallpaper.service" \
      "$SYSTEMD_DIR/wallpaper.service"

cp -f "$PROJECT_DIR/systemd/wallpaper.timer" \
      "$SYSTEMD_DIR/wallpaper.timer"

echo "Reloading systemd"
systemctl --user daemon-reload

echo "Enabling timer"
systemctl --user enable --now wallpaper.timer

if ! systemctl --user is-enabled wallpaper.timer &>/dev/null; then
    echo "Failed to enable timer"
    exit 1
fi

echo ""
echo "Installed successfully!"
echo ""
echo "Run:"
echo "wallpaperchanger --next"
echo ""
echo "Check timers:"
echo "systemctl --user list-timers"
echo ""
echo "Logs:"
echo "journalctl --user -u wallpaper.service -f"
