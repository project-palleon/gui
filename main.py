from io import BytesIO
from threading import Thread

from PIL import Image
from palleon import SimpleSocket

from config import Config
from gui import Window, ImageRenderer
from plugins import plugin_mgr

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
                for (data_source_name, input_source_name, timestamp, data) in updates["data"]:
                    plugin_mgr.update(data_source_name, input_source_name, timestamp, data)

            if len(updates["images"]) > 0:
                for image_wrapper in updates["images"]:
                    input_source_name = image_wrapper["input_source"]

                    if input_source_name not in image_renderers:
                        image_renderers[input_source_name] = ImageRenderer()

                    other_metadata = {
                        "timestamp": image_wrapper["timestamp"],
                    }

                    parsed_image = Image.open(BytesIO(image_wrapper["data"]))
                    image_renderers[input_source_name].update_from_image(parsed_image, input_source_name, other_metadata)


def main():
    # TODO if connection fails, close window or show error or smth
    t = Thread(target=receive)
    t.daemon = True
    t.start()

    g = Window(1280, 720, "palleon", plugin_mgr, image_renderers)
    g.loop()


if __name__ == "__main__":
    main()
