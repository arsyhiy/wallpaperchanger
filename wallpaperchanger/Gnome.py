from wallpaperchanger.WindowManager import WindowManager

import subprocess


class Gnome(WindowManager):
    """Gnome implementation of WindowManager"""

    # временное решение
    @staticmethod
    def get_default():
        """search for first default_image"""

        image = "file:///usr/share/backgrounds/gnome/adwaita-l.jpg"
        return image

    default_wallpaper = get_default()

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
