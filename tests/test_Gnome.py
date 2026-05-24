# """
# test_Gnome.py: testing a gnome class.
# """

# import os
# from urllib.parse import urlparse

# # from unittest.mock import patch
# # import pytest
# #
# # import subprocess
# #
# # import re


# from wallpaperchanger.Gnome import Gnome

# # честно надо еще подумать нужно мне этот тест
# # def test_is_default_image_start_with_uri():
# #     assert Gnome.default_wallpaper.startswith("file://") == True


# def test_is_default_image_available():
#     path = urlparse(Gnome.default_wallpaper).path
#     assert os.path.exists(path) == True


# # @patch("subprocess.run")
# # def test_set_wallpaper_adds_file_prefix(mock_run):
# #     wm = Gnome()
# #
# #     wm.set_wallpaper("~/wall.jpg")
# #
# #     mock_run.assert_called_once_with(
# #         [
# #             "gsettings",
# #             "set",
# #             "org.gnome.desktop.background",
# #             "picture-uri",
# #             "file://" + "/home/arsen/wall.jpg",
# #         ],
# #         check=True,
# #     )


# # @patch("subprocess.run")
# # def test_set_wallpaper_keeps_uri(mock_run):
# #     wm = Gnome()
# #
# #     wm.set_wallpaper("file:///tmp/a.jpg")
# #
# #     mock_run.assert_called_once_with(
# #         [
# #             "gsettings",
# #             "set",
# #             "org.gnome.desktop.background",
# #             "picture-uri",
# #             "file:///tmp/a.jpg",
# #         ],
# #         check=True,
# #     )

# # def set_wallpaper(self, image):
# #     if not image.startswith("file://"):
# #         image = "file://" + os.path.abspath(os.path.expanduser(image))

# #     # FIXME: обернуть это в try
# #     subprocess.run(
# #         [
# #             "gsettings",
# #             "set",
# #             "org.gnome.desktop.background",
# #             "picture-uri",
# #             image,
# #         ],
# #         check=True,
# #     )
