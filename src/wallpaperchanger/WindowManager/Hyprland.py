import subprocess
from WindowManager.BaseManager import BaseManager


# NOTE:  на самом деле сделать  hyprland сложней чем для gnome тут больше деталей  

class Hyprland(BaseManager):
    """Hyprland implementation of WindowManager (via hyprpaper IPC)."""

    default_wallpaper = "/usr/share/backgrounds/gnome/adwaita-l.jpg"

    def set_wallpaper(self, image, monitor=""):
        # monitor="" -> применить ко всем мониторам без своего обоя
        try:
            subprocess.run(
                ["hyprctl", "hyprpaper", "wallpaper", f"{monitor},{image}"],
                check=True,
            )
        except FileNotFoundError:
            print("hyprctl not installed")
        except subprocess.CalledProcessError as e:
            print("Command failed:", e)

    def get_current_wallpaper(self):
        try:
            result = subprocess.run(
                ["hyprctl", "hyprpaper", "listactive"],
                capture_output=True, text=True, check=True,
            )
        except FileNotFoundError:
            print("hyprctl not installed")
            return None
        except subprocess.CalledProcessError as e:
            print("Command failed:", e)
            return None

        for line in result.stdout.splitlines():
            if ":" in line:
                return line.split(":", 1)[1].strip()
        return None
