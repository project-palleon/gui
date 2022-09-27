from collections import defaultdict

import OpenGL.GL as gl
import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer


class Window:
    def __init__(self, width, height, window_name, plugin_mgr, image_drawers):
        self._window_name = window_name
        self._height = int(height)
        self._width = int(width)
        self._plugin_mgr = plugin_mgr
        self._image_drawers = image_drawers

    def _draw_loop(self):
        for input_source, plugins in self._plugin_mgr.plugins_by_input_source.items():
            imgui.begin(input_source, True)

            if input_source in self._image_drawers:
                self._image_drawers[input_source].draw()

            for plugin in plugins:
                plugin.draw()
            imgui.end()

    def loop(self):
        window = self.impl_glfw_init()
        imgui.create_context()
        impl = GlfwRenderer(window)

        menus = defaultdict(list)

        for plugin in self._plugin_mgr.plugins:
            for menu_name, fn in plugin.main_menu_bar().items():
                menus[menu_name].append(fn)

        while not glfw.window_should_close(window):
            glfw.poll_events()
            impl.process_inputs()

            imgui.new_frame()

            self._draw_loop()

            if imgui.begin_main_menu_bar():
                for menu_name, fns in menus.items():
                    if imgui.begin_menu(menu_name, True):
                        for fn in fns:
                            fn()

                        imgui.end_menu()
                imgui.end_main_menu_bar()

            gl.glClearColor(0.0, 0.0, 0.0, 0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            imgui.render()
            impl.render(imgui.get_draw_data())
            glfw.swap_buffers(window)

        impl.shutdown()
        glfw.terminate()

    def impl_glfw_init(self):  # alias = create_window
        if not glfw.init():
            print("Could not initialize OpenGL context")
            exit(1)

        # OS X supports only forward-compatible core profiles from 3.2
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

        # Create a windowed mode window and its OpenGL context
        window = glfw.create_window(self._width, self._height, self._window_name, None, None)
        glfw.make_context_current(window)

        if not window:
            glfw.terminate()
            print("Could not initialize Window")
            exit(1)

        return window
