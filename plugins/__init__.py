from collections import defaultdict

from plugins.activity_plugin import ActivityPlugin
from plugins.face_plugin.plugin import FacePlugin
from plugins.metadata_plugin.plugin import MetadataPlugin
from plugins.plugin_abc import Plugin

data_source_handlers = {
    "activity": ActivityPlugin,
    "face": FacePlugin,
    "metadata": MetadataPlugin
}


class PluginManager:
    def __init__(self):
        # [data_source_name][input_source_name]
        self._plugins = {
            data_source_name: defaultdict(handler)
            for data_source_name, handler in data_source_handlers.items()
        }

    def update(self, data_source_name, input_source_name, timestamp, data):
        if data_source_name not in self._plugins:
            raise KeyError(f"No handler registered (in the data_source_handlers dictionary) for {data_source_name!r}.")

        plugin: Plugin = self._plugins[data_source_name][input_source_name]
        plugin.update(data_source_name, input_source_name, timestamp, data)

    @property
    def plugins(self):
        for plugin_dicts in self._plugins.values():
            for plugin in plugin_dicts.values():
                yield plugin

    @property
    def plugins_by_input_source(self):
        plugins = defaultdict(list)
        for data_source_name, plugin_dicts in self._plugins.items():
            for input_source_name, plugin in plugin_dicts.items():
                plugins[input_source_name].append(plugin)
        return dict(plugins)


plugin_mgr = PluginManager()
