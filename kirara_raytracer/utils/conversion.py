import glm
import numpy as np


class Conversion:
    @staticmethod
    def get_pixels_as_uint32_array(array: np.ndarray) -> list:
        # 1111 1111 0000 0000 0000 0000 0000 0000 A
        #           0001 1000 0000 0000 0000 0000 R
        #                     1010 1001 0000 0000 G
        #                               1011 1101 B
        return (255 << 24 | array[:, :, 0] << 16 | array[:, :, 1] << 8 | array[:, :, 2]).flatten()

    @staticmethod
    def color_as_uint32(self, color: glm.vec3):
        return 255 << 24 | int(color.x) << 16 | int(color.y) << 8 | int(color.z)
