#!/usr/bin/env bash
set -e

echo "🧹 Uninstalling wallpaper changer..."

SYSTEMD_DIR="$HOME/.config/systemd/user"

systemctl --user stop wallpaper.timer || true
systemctl --user disable wallpaper.timer || true

rm -f "$SYSTEMD_DIR/wallpaper.service"
rm -f "$SYSTEMD_DIR/wallpaper.timer"

systemctl --user daemon-reload

rm -f "$HOME/.wallpaper_state.json"

echo "✅ Uninstalled."

echo "🗑 Removing symlink..."
sudo rm -f /usr/local/bin/wallpaperchanger
