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
ANIMATION_FPS = 12.0
SPRITE_TOP_OFFSET = 2


class Idle:
    def enter(self, sparrow):
        sparrow.idle_started_at = get_time()
        sparrow.frame = 0

    def do(self, sparrow):
        sparrow.advance_frame()
        if get_time() - sparrow.idle_started_at >= 0.35:
            sparrow.start_flying()


class Fly:
    def enter(self, sparrow):
        sparrow.frame = 0

    def do(self, sparrow):
        sparrow.advance_frame()
        sparrow.move()


class Sparrow:
    def __init__(self, index):
        self.index = index
        self.image = load_image('bird_animation.png')
        self.frame = 0
        self.idle_started_at = get_time()
        self.x = 0.0
        self.y = 0.0
        self.phase = 0.0
        self.states = {'IDLE': Idle(), 'FLY': Fly()}
        self.machine = Machine(
            model=self,
            states=['IDLE', 'FLY'],
            transitions=[
                {'trigger': 'start_flying', 'source': 'IDLE', 'dest': 'FLY'},
            ],
            initial='IDLE',
            auto_transitions=False,
        )

    def on_enter_IDLE(self):
        self.states['IDLE'].enter(self)

    def on_enter_FLY(self):
        self.states['FLY'].enter(self)

    def advance_frame(self):
        self.frame = (self.frame + ANIMATION_FPS *
                      game_framework.frame_time) % SPRITE_FRAME_COUNT

    def draw(self):
        frame = int(self.frame)
        row, column = divmod(frame, SPRITE_COLUMNS)
        source_x = column * SPRITE_WIDTH
        source_y = (SPRITE_ROWS - row - 1) * SPRITE_HEIGHT + SPRITE_TOP_OFFSET
        self.image.clip_draw(
            source_x, source_y, SPRITE_WIDTH, SPRITE_HEIGHT,
            self.x, self.y, DRAW_WIDTH, DRAW_HEIGHT
        )
