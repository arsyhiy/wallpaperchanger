# старая версия запуска этой программы
import os
import argparse

import dearpygui.dearpygui as dpg  # pyright: ignore[reportMissingImports] классная вещь 

# WindowManager import section
from WindowManager.Gnome import Gnome
from WindowManager.Hyprland import Hyprland


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


# def main():
#     parser = argparse.ArgumentParser(
#         prog="wallpaperchanger",
#         usage="%(prog)s [options]",
#         description="wallpaper changer",
#     )
# 
#     parser.add_argument("--next", action="store_true", help="Set next wallpaper")
#     parser.add_argument("--default", action="store_true", help="Set default wallpaper")
#     parser.add_argument(
#         "--refresh", action="store_true", help="refresh the list of images"
#     )
# 
#     manager = identify_manager()
#     args = parser.parse_args()
# 
#     if args.next:
#         manager.set_next_wallpaper()
# 
#     elif args.default:
#         manager.set_default()
# 
#     elif args.refresh:
#         images = manager.save_images_to_json()
#         print(f"Updated: {len(images)} images")
#         # manager.set_wallpaper_zoom()
#         manager.set_wallpaper(images)

def main():
    dpg.create_context()

    with dpg.window(label="Wallpaper Changer"):
        dpg.add_text("Wallpaper Changer")
        dpg.add_button(label="Next")
        dpg.add_button(label="Previous")

        dpg.create_viewport(
            title="Wallpaper Changer",
            width=500,
            height=300,
        )

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()


if __name__ == "__main__":
    main()
