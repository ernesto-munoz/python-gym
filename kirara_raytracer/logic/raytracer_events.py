from enum import Enum


class RaytracerEvents(Enum):
    RENDER_STARTED = "render_started"
    PIXEL_FINISHED = "pixel_finished"
    RENDER_FINISHED = "render_finished"
    RENDER_TILE_FINISHED = "render_tile_finished"

