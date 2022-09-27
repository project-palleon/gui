from threading import Lock

import imgui

from plugins.plugin_abc import Plugin


class MetadataPlugin(Plugin):
    def __init__(self):
        super().__init__(["metadata"])

        self.data = {}
        self.data_lock = Lock()

    def update(self, data_src, input_src, timestamp, data):
        with self.data_lock:
            self.data = data

    def draw(self):
        with self.data_lock:
            for key, value in self.data.items():
                imgui.text_ansi(f"{key}: \033[31m{value}")  # \033[mnsi ")

    def main_menu_bar(self):
        return {}
