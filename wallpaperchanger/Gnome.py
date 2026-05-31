from wallpaperchanger.WindowManager import WindowManager

import subprocess


class Gnome(WindowManager):
    """Gnome implementation of WindowManager"""

    default_wallpaper = "file:///usr/share/backgrounds/gnome/adwaita-l.jpg"

    def set_wallpaper(self, image):

        try:
            subprocess.run(
                [
                    "gsettings",
                    "set",
                    "org.gnome.desktop.background",
                    "picture-uri",
                    image,
                ],
                check=True,
            )
        except FileNotFoundError:
            print("gsettings not installed")

        except subprocess.CalledProcessError as e:
            print("Command failed:", e)

    def get_current_wallpaper(self):
        try:
            result = subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.background", "picture-uri"],
                capture_output=True,
                text=True,
                check=True,
            )
        except FileNotFoundError:
            print("gsettings not installed")

        except subprocess.CalledProcessError as e:
            print("Command failed:", e)

        value = result.stdout.strip().strip("'")

        if not value or value == "none":
            return None

        return value
