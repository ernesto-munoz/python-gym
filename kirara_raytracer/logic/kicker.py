import os
import sys
import random
from argparse import ArgumentParser, Namespace
from pathlib import Path
import time
from tqdm import tqdm
from kirara_raytracer.logic.raytracer import Raytracer, RaytracerEvents, OutputPixelData


class KiraraKicker(object):

    def __init__(self):
        super(KiraraKicker, self).__init__()
        self._namespace: Namespace or None = None

        self._output_filepath: Path | None = None
        self._image_width: int = 64
        self._image_height: int = 64

        self._raytracer: Raytracer or None = None

        self._progress_bar: tqdm or None = None

    def launch(self):
        self._raytracer = Raytracer(image_width=self._image_width, image_height=self._image_height)
        self._raytracer.publisher.register(event=RaytracerEvents.PIXEL_FINISHED, who=self,
                                           callback=self._pixel_finished_callback)

        self._progress_bar = tqdm(total=self._image_width * self._image_height)
        start = time.time()
        self._raytracer.render()
        print(f"Raw Render Time: {time.time() - start}")

        self._progress_bar.close()
        self._raytracer.save_to_image(output_filepath=self._output_filepath)

    def _pixel_finished_callback(self, data):
        output_pixel_data: OutputPixelData = data["output_pixel_data"]
        self._progress_bar.update(output_pixel_data.height * output_pixel_data.width)

    @staticmethod
    def parse_command_line_flags():
        parser = ArgumentParser()

        parser.add_argument('-o', '--output_filepath', type=str, help='')
        parser.add_argument('-w', '--image_width', type=int, help='')
        parser.add_argument('-hh', '--image_height', type=int, help='')

        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit()

        return parser.parse_args()

    def launch_console(self):
        self._namespace = self.parse_command_line_flags()
        self._output_filepath = Path(self._namespace.output_filepath)
        self._image_width = self._namespace.image_width or self._image_width
        self._image_height = self._namespace.image_height or self._image_height

        self.launch()


if __name__ == '__main__':
    KiraraKicker().launch_console()
