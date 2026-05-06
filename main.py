#!/usr/bin/env python3

import subprocess
import os
import json
import argparse


class WindowManager:
    "base class for window manager, inheritance only purpose"

    default_wallpaper = None

    def get_current_wallpaper(self):
        raise NotImplementedError

    def set_wallpaper(self, image):
        _ = image
        raise NotImplementedError

    def collect_images(self, base_path="~/images"):
        base_path = os.path.expanduser(base_path)

        image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}
        images = []

        for root, _, files in os.walk(base_path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in image_extensions:
                    images.append(os.path.join(root, file))

        return sorted(images)

    def set_default(self):
        if self.default_wallpaper is None:
            raise NotImplementedError("default_wallpaper was not set")

        self.set_wallpaper(self.default_wallpaper)


class Gnome(WindowManager):
    """Gnome implementation"""

    default_wallpaper = "file:///usr/share/backgrounds/gnome/adwaita-l.jpg"

    def set_wallpaper(self, image):
        if not image.startswith("file://"):
            image = "file://" + os.path.abspath(os.path.expanduser(image))

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

    def get_current_wallpaper(self):
        result = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.background", "picture-uri"],
            capture_output=True,
            text=True,
            check=True,
        )

        value = result.stdout.strip().strip("'")

        if not value or value == "none":
            return None

        return value


def save_images_to_json(base_path="~/images", json_path="~/images.json"):
    gnome = Gnome()
    images = gnome.collect_images(base_path)

    json_path = os.path.expanduser(json_path)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(images, f, indent=2)

    return images


def load_images_from_json(json_path="~/images.json"):
    json_path = os.path.expanduser(json_path)

    if not os.path.exists(json_path):
        raise FileNotFoundError("JSON файл не найден")

    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_or_refresh_images(base_path="~/images", json_path="~/images.json"):
    json_path = os.path.expanduser(json_path)

    if not os.path.exists(json_path):
        return save_images_to_json(base_path, json_path)

    return load_images_from_json(json_path)


def set_next_wallpaper():
    gnome = Gnome()

    images = load_or_refresh_images()

    if not images:
        raise ValueError("Нет изображений")

    state_file = os.path.expanduser("~/.wallpaper_state.json")

    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            state = json.load(f)
        index = state.get("index", 0)
    else:
        index = 0

    index = (index + 1) % len(images)

    gnome.set_wallpaper(images[index])

    with open(state_file, "w") as f:
        json.dump({"index": index}, f)

def detect_manager():
    de = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()

    if "gnome" in de:
        return "gnome"

def choose_manager():
    if detect_manager() == "gnome":
        return Gnome()
    else:
        print("program can't identify your window manager! please send issue to project! https://github.com/arsyhiy/wallpaperchanger")
        raise NotImplemented

def main():
    parser = argparse.ArgumentParser(
        prog="wallpaperchanger",
        usage="%(prog)s [options]",
        description="wallpaper changer",
    )

    parser.add_argument("--next", action="store_true", help="Set next wallpaper")
    parser.add_argument("--default", action="store_true", help="Set default wallpaper")
    parser.add_argument(
        "--refresh", action="store_true", help="refresh the list of images"
    )

    # gnome = Gnome()
    manager = choose_manager()
    args = parser.parse_args()

    if args.next:
        set_next_wallpaper()

    elif args.default:
        manager.set_default()

    elif args.refresh:
        images = save_images_to_json()
        print(f"Updated: {len(images)} images")


if __name__ == "__main__":
    main()
