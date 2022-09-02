import imgui

from plugins.plugin_abc import Plugin


class ExampleElementPlugin(Plugin):
    def __init__(self):
        super().__init__([])

    def update(self, data_src, timestamp, data):
        pass

    def draw(self):
        imgui.begin("Example Element Plugin", True)
        imgui.text("Bar")
        imgui.text_ansi("B\033[31marA\033[mnsi ")
        imgui.text_ansi_colored("Eg\033[31mgAn\033[msi ", 0.2, 1.0, 0.0)
        imgui.extra.text_ansi_colored("Eggs", 0.2, 1.0, 0.0)
        imgui.end()

    # noinspection PyMethodMayBeStatic
    def _main_menu_bar_test(self):
        clicked_test, selected_test = imgui.menu_item("Test", "Cmd+Q", False, True)

        if selected_test:
            print("SELECTED TEST")

        if clicked_test:
            print("CLICKED TEST")

    def main_menu_bar(self):
        return {"Test": self._main_menu_bar_test}
