from pico2d import get_canvas_width, load_image

import game_world
import game_framework


class Ball:
    images = {}

    def __init__(self, x, y, velocity, ball_type=1):
        if ball_type not in Ball.images:
            Ball.images[ball_type] = load_image(
                'ball21x21.png' if ball_type == 1 else 'ball41x41.png')
        self.image = Ball.images[ball_type]
        self.x, self.y = x, y
        self.velocity = velocity
        self.vertical_velocity = 350.0
        self.gravity = -980.0

    def update(self):
        frame_time = game_framework.frame_time
        self.x += self.velocity * frame_time
        self.y += self.vertical_velocity * frame_time
        self.vertical_velocity += self.gravity * frame_time

        if self.x < 0 or self.x > get_canvas_width() or self.y < 0:
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y)
