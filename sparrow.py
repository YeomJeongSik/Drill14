from math import sin, tau

from pico2d import get_canvas_height, get_canvas_width, get_time, load_image
from transitions import Machine

import game_framework


PIXEL_PER_METER = 10.0 / 0.3
BIRD_SPEED_KMPH = 18.0
BIRD_SPEED_MPM = BIRD_SPEED_KMPH * 1000.0 / 60.0
BIRD_SPEED_MPS = BIRD_SPEED_MPM / 60.0
BIRD_SPEED_PPS = BIRD_SPEED_MPS * PIXEL_PER_METER

SPRITE_WIDTH = 183
SPRITE_HEIGHT = 168
SPRITE_COLUMNS = 5
SPRITE_ROWS = 3
SPRITE_FRAME_COUNT = 14
DRAW_WIDTH = 110
DRAW_HEIGHT = 101
