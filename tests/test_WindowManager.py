# """
# test_WindowManager.py: tests for base class: WindowManager
# """

# import pytest

# from wallpaperchanger.WindowManager import WindowManager


# def test_default_wallpaper_is_none():
#     wm = WindowManager()
#     assert wm.default_wallpaper == None


# def test_set_default_requires_default_wallpaper():
#     wm = WindowManager()

#     with pytest.raises(
#         NotImplementedError,
#         match="default_wallpaper was not set",
#     ):
#         wm.set_default()


# def test_get_current_wallpaper_raise_NotImplementedError():
#     wm = WindowManager()
#     with pytest.raises(NotImplementedError):
#         wm.get_current_wallpaper()


# def test_set_wallpaper_not_implemented():
#     wm = WindowManager()
#     with pytest.raises(NotImplementedError):
#         wm.set_wallpaper("image.jpg")


# def test_collect_images_collects_only_images(tmp_path):
#     (tmp_path / "a.jpg").write_text("")
#     (tmp_path / "b.png").write_text("")
#     (tmp_path / "notes.txt").write_text("")

#     wm = WindowManager()

#     result = wm.collect_images(str(tmp_path))

#     assert len(result) == 2
#     assert result == sorted(result)


# def test_collect_images_empty_dir(tmp_path):
#     wm = WindowManager()

#     result = wm.collect_images(str(tmp_path))

#     assert result == []
