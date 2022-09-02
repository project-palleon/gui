from io import BytesIO
from threading import Thread

from PIL import Image

from config import Config
from gui import Window, ImageRenderer
from plugins import plugins
from simple_socket import SimpleSocket

config = Config.from_toml("config.toml")

# TODO make this locked? necessary?
image_renderers = {}


def receive():
    global image_renderers

    # TODO what if random disconnect (sever closes)?
    with SimpleSocket(config.core_host, config.core_port) as s:
        while True:
            updates = s.recv_bson()

            if len(updates["data"]) > 0:
                # todo build lookup dict cuz this is inefficient
                for (source, timestamp, data) in updates["data"]:
                    for plugin in plugins:
                        if source in plugin.keys:
                            plugin.update(source, timestamp, data)

            if len(updates["images"]) > 0:
                for (timestamp, source, raw_img) in updates["images"]:
                    if source not in image_renderers:
                        image_renderers[source] = ImageRenderer()

                    parsed_image = Image.open(BytesIO(raw_img))
                    image_renderers[source].update_from_image(parsed_image, (timestamp, source))


def main():
    # TODO if connection fails, close window or show error or smth
    t = Thread(target=receive)
    t.daemon = True
    t.start()

    g = Window(1280, 720, "palleon", plugins, image_renderers)
    g.loop()


if __name__ == "__main__":
    main()
