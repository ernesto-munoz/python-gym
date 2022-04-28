import glm
from glm import vec3, c_float
from .ray import Ray


class Camera:
    _position: vec3 = vec3(0.0, 0.0, 0.0)
    _vertical_field_of_view: float
    _aspect_ratio: float
    _focal_length: float = 1.0

    _viewport_height: float
    _viewport_width: float
    _horizontal: vec3
    _vertical: vec3
    _lower_left_corner: vec3

    def __init__(self, vertical_field_of_view: float, aspect_ratio: float):
        """ Initialize the camera with an aspect ratio."""
        self._aspect_ratio = aspect_ratio  # the aspect ratio setter calculates all the needed parameters
        self._vertical_field_of_view = vertical_field_of_view
        self._calculate_camera_parameters()

    @property
    def position(self) -> vec3:
        return self._position

    @position.setter
    def position(self, value: vec3):
        self._position = value

    @property
    def aspect_ratio(self) -> float:
        return self._aspect_ratio

    @aspect_ratio.setter
    def aspect_ratio(self, value: float):
        self._aspect_ratio = value
        self._calculate_camera_parameters()

    @property
    def focal_length(self) -> float:
        return self._focal_length

    @focal_length.setter
    def focal_length(self, value: float):
        """ IF the focal length changes, the lower left corner of the viewport needs to be recalculated.
        """
        self._focal_length = value
        self._calculate_camera_parameters()

    @property
    def vertical_field_of_view(self) -> float:
        return self._vertical_field_of_view

    @vertical_field_of_view.setter
    def vertical_field_of_view(self, value: float):
        self._vertical_field_of_view = value
        self._calculate_camera_parameters()

    def get_ray(self, u: c_float, v: c_float):
        """ Creates a Ray between the camera and the point indicated by the u and v parameters in the viewport.
        U and V must be float values between 0 and 1
        """
        point_of_interest = self._lower_left_corner + u * self._horizontal + v * self._vertical
        return Ray(origin=self._position, direction=point_of_interest - self._position)

    def _calculate_camera_parameters(self):
        """ With the aspect ratio, calculate the width and height of the viewport (height by default 2.0)
        Also calculate the horizontal and vertical vector of the viewport (based in the width and height)
        Lastly, calculate the point of the lower left corner of the viewport (the 0, 0) subtracting to the position
        of the camera, half the width, half the height and the distance between the position
        and the viewport (the near plane)
        """
        theta = glm.radians(self._vertical_field_of_view)
        self._viewport_height = glm.tan(theta / 2) * 2.0
        self._viewport_width = self._aspect_ratio * self._viewport_height
        self._horizontal = vec3(self._viewport_width, 0.0, 0.0)
        self._vertical = vec3(0.0, self._viewport_height, 0.0)
        self._lower_left_corner = self._position - self._horizontal / 2 - self._vertical / 2 - vec3(0.0, 0.0,
                                                                                                    self._focal_length)
