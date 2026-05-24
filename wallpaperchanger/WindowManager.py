import os
import json


class WindowManager:
    "base class for window manager"

    default_wallpaper = None

    def get_current_wallpaper(self):
        raise NotImplementedError

    def set_wallpaper(self, image):
        _ = image
        raise NotImplementedError

    def set_default(self):
        if self.default_wallpaper is None:
            raise NotImplementedError("default_wallpaper was not set")

        self.set_wallpaper(self.default_wallpaper)

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

    def save_images_to_json(self, base_path="~/images", json_path="~/images.json"):
        images = self.collect_images(base_path)
        json_path = os.path.expanduser(json_path)

        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(images, f, indent=2)
        except OSError as e:
            raise RuntimeError(f"Failed to write images cache: {json_path}") from e

        return images

    def load_images_from_json(self, json_path="~/images.json"):
        json_path = os.path.expanduser(json_path)

        if not os.path.exists(json_path):
            raise FileNotFoundError("JSON файл не найден")

        with open(
            json_path, "r", encoding="utf-8"
        ) as f:  # FIXME: надо обарачивать подобные вещи в try expect.
            return json.load(f)

    def load_or_refresh_images(self, base_path="~/images", json_path="~/images.json"):
        json_path = os.path.expanduser(json_path)

        if not os.path.exists(json_path):
            return self.save_images_to_json(base_path, json_path)

        return self.load_images_from_json(json_path)

    def set_next_wallpaper(self):

        images = self.load_or_refresh_images()

        if not images:
            raise ValueError("images not available")

        state_file = os.path.expanduser("~/.wallpaper_state.json")

        index = 0

        try:
            with open(state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
                index = state.get("index", 0)

        except (FileNotFoundError, json.JSONDecodeError, OSError):
            index = 0

        index = (index + 1) % len(images)

        self.set_wallpaper(images[index])

        try:
            tmp_file = state_file + ".tmp"

            with open(tmp_file, "w", encoding="utf-8") as f:
                json.dump({"index": index}, f)

            os.replace(tmp_file, state_file)

        except OSError as e:
            # можно логировать, но не ломать программу
            print(f"Failed to write state file: {e}")
