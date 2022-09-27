from io import BytesIO

import imgui
from PIL import Image

from gui import ImageRenderer
from plugins.plugin_abc import Plugin


class FacePlugin(Plugin):
    def __init__(self):
        super().__init__(["face"])

        self._image_renderer = ImageRenderer()

    def update(self, data_src, input_src, timestamp, data):
        last_face_img_binary = data["last_face_img_binary"]

        if last_face_img_binary == b"":
            return

        parsed_image = Image.open(BytesIO(last_face_img_binary))

        self._image_renderer.update_from_image(parsed_image, input_src, None)

    def draw(self):
        imgui.text("Last face:")

        # imgui.text_ansi("B\033[31marA\033[mnsi ")
        # imgui.text_ansi_colored("Eg\033[31mgAn\033[msi ", 0.2, 1.0, 0.0)
        # imgui.extra.text_ansi_colored("Eggs", 0.2, 1.0, 0.0)

        self._image_renderer.draw()

    def main_menu_bar(self):
        return {}
