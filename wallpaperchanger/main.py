#!/usr/bin/env python3

import subprocess
import os
import json
import argparse

from wallpaperchanger.Gnome import Gnome


def detect_manager():
    de = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()

    if "gnome" in de:
        return "gnome"

    return None


def set_manager():
    manager = detect_manager()

    if manager == "gnome":
        return Gnome()

    raise NotImplementedError(
        "Window manager is not supported. "
        "Please open an issue: https://github.com/arsyhiy/wallpaperchanger"
    )


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

    manager = set_manager()
    args = parser.parse_args()

    if args.next:
        manager.set_next_wallpaper()

    elif args.default:
        manager.set_default()

    elif args.refresh:
        images = manager.save_images_to_json()
        print(f"Updated: {len(images)} images")


if __name__ == "__main__":
    main()
