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
FLIGHT_AMPLITUDE = 32.0
FLIGHT_FREQUENCY = tau / 3.2


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
    image = None

    def __init__(self, index):
        self.index = index
        if Sparrow.image is None:
            Sparrow.image = load_image('bird_animation.png')
        self.image = Sparrow.image
        self.frame = 0
        self.idle_started_at = get_time()
        self.x = 0.0
        self.y = 0.0
        self.phase = 0.0
        self.base_y = 0.0
        self.flight_time = 0.0
        self.configure_initial_position()
        self.states = {'IDLE': Idle(), 'FLY': Fly()}
        self.machine = Machine(
            model=self,
            states=['IDLE', 'FLY'],
            transitions=[
                {'trigger': 'start_flying', 'source': 'IDLE', 'dest': 'FLY'},
                {'trigger': 'reset_flight', 'source': 'FLY', 'dest': 'IDLE'},
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

    def configure_initial_position(self):
        spacing = get_canvas_width() / 10.0
        self.x = -DRAW_WIDTH / 2 + self.index * spacing
        self.base_y = get_canvas_height() * 0.45 + (self.index % 3) * 55
        self.y = self.base_y
        self.phase = self.index * tau / 10.0

    def move(self):
        frame_time = game_framework.frame_time
        self.flight_time += frame_time
        self.x += BIRD_SPEED_PPS * frame_time
        self.y = self.base_y + FLIGHT_AMPLITUDE * sin(
            self.phase + FLIGHT_FREQUENCY * self.flight_time
        )

    def update(self):
        self.states[self.state].do(self)
        if self.x - DRAW_WIDTH / 2 > get_canvas_width():
            self.respawn()

    def respawn(self):
        self.x = -DRAW_WIDTH / 2
        self.flight_time = 0.0
        self.phase += tau / 7.0
        self.reset_flight()

    def draw(self):
        frame = int(self.frame)
        row, column = divmod(frame, SPRITE_COLUMNS)
        source_x = column * SPRITE_WIDTH
        source_y = (SPRITE_ROWS - row - 1) * SPRITE_HEIGHT + SPRITE_TOP_OFFSET
        self.image.clip_draw(
            source_x, source_y, SPRITE_WIDTH, SPRITE_HEIGHT,
            self.x, self.y, DRAW_WIDTH, DRAW_HEIGHT
        )
