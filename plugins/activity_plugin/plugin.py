from array import array
from threading import Lock

import imgui

from plugins.plugin_abc import Plugin


class ActivityPlugin(Plugin):
    def __init__(self):
        super().__init__(["activity"])

        self.plot_values = array("f", [0 for _ in range(100)])
        self.plot_values_lock = Lock()

    def update(self, data_src, input_src, timestamp, data):
        with self.plot_values_lock:
            self.plot_values.pop(0)
            self.plot_values.append(data["changed"])

    def draw(self):
        with self.plot_values_lock:
            imgui.plot_lines(
                "Aktivität",
                self.plot_values,
                graph_size=(0, 50),  # = (autoscale width, 50px height)
                scale_min=0,
                scale_max=1,
            )

    def main_menu_bar(self):
        return {}
