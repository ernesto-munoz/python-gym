import math
import sys
import glm
import random
import functools

import numpy as np
from PySide6.QtGui import QPixmap, QImage, QColor, QRegularExpressionValidator, qRgb
from PySide6.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtCore import QElapsedTimer, QRegularExpression, QThread, Signal
from render_view_window import Ui_RenderViewWindow
from camera_parameters_dialog_ui import CameraDataDialog

from kirara_raytracer.logic.raytracer import Raytracer
from kirara_raytracer.logic.raytracer_events import RaytracerEvents
from kirara_raytracer.logic.raytracer import OutputPixelData


class RenderViewWindow(QMainWindow):
    def __init__(self):
        super(RenderViewWindow, self).__init__()
        self.ui = Ui_RenderViewWindow()
        self.ui.setupUi(self)

        self._camera_data_dialog = CameraDataDialog(self)
        self._raytracer: Raytracer | None = None

        scene = QGraphicsScene()
        self.ui.viewport_graphics_view.setScene(scene)
        self._image = None
        self._pixmap_item = QGraphicsPixmapItem()
        scene.addItem(self._pixmap_item)
        self.ui.render_progress_bar.reset()

        # ui validations
        self.ui.resolution_width_line.setValidator(QRegularExpressionValidator(QRegularExpression("[1-9]\\d{0,3}")))
        self.ui.resolution_height_line.setValidator(QRegularExpressionValidator(QRegularExpression("[1-9]\\d{0,3}")))

        # connections
        # self.ui.render_button.clicked.connect(self._update_progress_bar)
        self.ui.render_button.clicked.connect(self.render_button_clicked)
        self.ui.resolution_combo_box.currentIndexChanged.connect(self.resolution_combo_box_current_index_changed)
        self.ui.camera_parameters_button.clicked.connect(self._camera_parameters_button_clicked)

        self.show()

    def render_button_clicked(self):
        # set teh correct interface configuration while a render
        self.ui.render_button.setEnabled(False)
        self.ui.resolution_combo_box.setEnabled(False)
        self.ui.resolution_width_line.setEnabled(False)
        self.ui.resolution_height_line.setEnabled(False)

        self.ui.status_bar.showMessage(f"Rendering...")

        width, height = self._get_render_resolution()
        # image = QImage(width, height, QImage.Format_ARGB32)
        # self._pixmap_item.setPixmap(QPixmap.fromImage(image))

        self._raytracer = Raytracer(image_width=width, image_height=height)
        # self._raytracer.camera.position.x = self._camera_data_dialog._camera_position_x
        # self._raytracer.camera.position.y = self._camera_data_dialog._camera_position_y
        # self._raytracer.camera.position.z = self._camera_data_dialog._camera_position_z
        # self._raytracer.camera.vertical_field_of_view = self._camera_data_dialog._field_of_view

        self._render_thread = RenderThread(raytracer=self._raytracer, width=width, height=height, render_view=self)
        self._render_thread.start()
        self._render_thread.render_finished_signal.connect(self._render_finished_event)
        # self._render_thread.update_render_progress_bar.connect(self._update_render_progress_bar)
        self._render_thread.pixel_finished_signal.connect(self._pixel_finished_event)

        # image = QImage(width, height, QImage.Format_RGB32)
        # render_timer = QElapsedTimer()
        # render_timer.start()
        # self._raytracer.render(image_width=width, image_height=height)
        # pixels = self._raytracer.pixels
        # self.ui.status_bar.showMessage(f"Render time: {render_timer.elapsed()} ms")
        #
        # for column in range(width):
        #     for row in range(height):
        #         p = pixels[(row, column)]
        #         image.setPixel(column, row, QColor(p.x * 255, p.y * 255, p.z * 255, 255).rgb())
        #
        # self._pixmap_item.setPixmap(QPixmap.fromImage(image))
        #
        # self.ui.render_button.setEnabled(True)

    def _render_finished_event(self, render_time: int):
        self.ui.status_bar.showMessage(f"Render time: {render_time} ms ({render_time / 60000:.2f} m)")
        # width, height = self._get_render_resolution()
        #
        # image = QImage(pixels, width, height, QImage.Format_ARGB32)
        # self._pixmap_item.setPixmap(QPixmap.fromImage(image))

        # restore the correct interface configuration after a render
        self.ui.render_button.setEnabled(True)
        self.ui.resolution_combo_box.setEnabled(True)
        if self.ui.resolution_combo_box.currentIndex() == 0:
            self.ui.resolution_width_line.setEnabled(True)
            self.ui.resolution_height_line.setEnabled(True)

    def _pixel_finished_event(self, output_pixel_data: OutputPixelData, converted_color: glm.vec3,
                              pixels_completed_count: int):
        width, height = self._get_render_resolution()
        if self._image is None:
            self._image = QImage(width, height, QImage.Format_ARGB32)

        self._image.setPixel(
            output_pixel_data.column,
            output_pixel_data.row,
            qRgb(converted_color.x, converted_color.y, converted_color.z)
        )

        self._pixmap_item.setPixmap(QPixmap.fromImage(self._image))

        percentage = (100 * pixels_completed_count) / (width * width)
        self.ui.render_progress_bar.setValue(percentage)

    # def _update_render_progress_bar(self, percentage: float):


    def resolution_combo_box_current_index_changed(self, index):
        if index == 0:
            self.ui.resolution_width_line.setEnabled(True)
            self.ui.resolution_height_line.setEnabled(True)
        else:
            self.ui.resolution_width_line.setEnabled(False)
            self.ui.resolution_height_line.setEnabled(False)

    def _camera_parameters_button_clicked(self):
        self._camera_data_dialog.show()

    def _get_render_resolution(self) -> tuple[int, int]:
        index = self.ui.resolution_combo_box.currentIndex()
        resolutions = {
            0: (int(self.ui.resolution_width_line.text()), int(self.ui.resolution_height_line.text())),
            1: (854, 480),
            2: (1024, 576),
            3: (1280, 720),
            4: (1920, 1080),
            5: (2560, 1440),
        }
        return resolutions[index]


# TODO
class RenderThread(QThread):
    render_finished_signal = Signal(int)
    pixel_finished_signal = Signal(OutputPixelData, glm.vec3, int)

    def __init__(self, raytracer: Raytracer, width: int, height: int, render_view: RenderViewWindow):
        super().__init__()

        self._width = width
        self._height = height
        self._raytracer = raytracer
        self._render_view = render_view
        self._raytracer.publisher.register(event=RaytracerEvents.PIXEL_FINISHED, who=self,
                                           callback=self._pixel_finished_callback)

        self._current_pixels_count = 0

    def run(self):
        self._current_pixels_count = 0
        render_timer = QElapsedTimer()
        render_timer.start()

        import cProfile
        import pstats
        cp = cProfile.Profile()
        cp.enable()

        self._raytracer.render()

        cp.disable()
        stats = pstats.Stats(cp)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()

        elapse_time = render_timer.elapsed()
        print(f"Render time: {elapse_time}")
        self.render_finished_signal.emit(elapse_time)

    def _pixel_finished_callback(self, data):
        self._current_pixels_count += 1
        output_pixel_data = data["output_pixel_data"]
        converted_color = data["converted_color"]
        # if self._current_pixels_count % 10 == 0:
        #     percentage = (100 * self._current_pixels_count) / (self._width * self._height)
        #     self.update_render_progress_bar.emit(math.ceil(percentage))

        self.pixel_finished_signal.emit(output_pixel_data, converted_color, self._current_pixels_count)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    KiraraUI = RenderViewWindow()
    sys.exit(app.exec())
