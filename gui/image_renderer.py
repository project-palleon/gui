from threading import Lock
from typing import Optional, Any

import OpenGL.GL as gl
import imgui
import numpy
from PIL import Image


def get_rgba_pixels(image: Image.Image):
    if image.mode == "RGB":
        return image.tobytes("raw", "RGBX")

    if image.mode != "RGBA":
        image = image.convert("RGBA")

    return image.tobytes("raw", "RGBA")


class ImageRenderer:
    def __init__(self):
        self.rgba_data_lock = Lock()
        self.rgba_data: Optional[bytes] = None
        self.size: Optional[(int, int)] = None
        self.metadata: Any = None
        self.source = None

        self.changed: bool = False
        self.changed_lock = Lock()

        self._texture_id: Optional[numpy.uint32] = None

    def update_from_image(self, image: Image.Image, source, metadata=None):
        size = (image.width, image.height)
        rgba_data = get_rgba_pixels(image)
        self.update(rgba_data, size, source, metadata)

    def update(self, data, size, source, metadata=None):
        with self.rgba_data_lock:
            self.size = size
            self.rgba_data = data
            self.metadata = metadata
            self.source = source
            with self.changed_lock:
                self.changed = True

    def draw(self, scale=0.2):
        if self.rgba_data:
            with self.changed_lock:
                if self.changed:
                    with self.rgba_data_lock:
                        if self._texture_id is None:
                            self._texture_id = gl.glGenTextures(1)

                        gl.glBindTexture(gl.GL_TEXTURE_2D, self._texture_id)
                        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
                        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
                        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_BORDER)
                        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_BORDER)
                        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.size[0], self.size[1], 0,
                                        gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, self.rgba_data)

                    self.changed = False

            scaled_width = int(self.size[0] * scale)
            scaled_height = int(self.size[1] * scale)

            with self.rgba_data_lock:
                if self.rgba_data and imgui.is_rect_visible(scaled_width, scaled_height):
                    imgui.image(self._texture_id, scaled_width, scaled_height)
                else:
                    # Skip if outside view
                    imgui.dummy(scaled_width, scaled_height)
