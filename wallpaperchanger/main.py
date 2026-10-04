import os
import argparse

# WindowManager import section
from wallpaperchanger.WindowManager.Gnome import Gnome
from wallpaperchanger.WindowManager.Hyprland import Hyprland


def identify_manager():
    """
    identify what window manager user is using right now
    """

    wm = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()

    match wm:
        case "gnome":
            return Gnome()
        case "hyprland":
            return Hyprland()
        case _:
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

    manager = identify_manager()
    args = parser.parse_args()

    if args.next:
        manager.set_next_wallpaper()

    elif args.default:
        manager.set_default()

    elif args.refresh:
        images = manager.save_images_to_json()
        print(f"Updated: {len(images)} images")
        # manager.set_wallpaper_zoom()
        manager.set_wallpaper(images)


if __name__ == "__main__":
    main()
