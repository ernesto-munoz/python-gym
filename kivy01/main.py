from random import randint
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock


class PongGame(Widget):
    ball = ObjectProperty(None)
    left_paddle = ObjectProperty(None)
    right_paddle = ObjectProperty(None)

    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()
        self.left_paddle.bounce_ball(self.ball)
        self.right_paddle.bounce_ball(self.ball)

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # bounce off left and right
        if self.ball.x < 0:
            self.right_paddle.score += 1
            self.serve_ball()

        if self.ball.right > self.width:
            self.left_paddle.score += 1
            self.serve_ball()

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.left_paddle.center_y = touch.y

        if touch.x > self.width - self.width / 3:
            self.right_paddle.center_y = touch.y


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            speedup = 1.1
            offset = Vector(0, (ball.center_y - self.center_y) * 0.02)
            ball.velocity = speedup * (offset - ball.velocity)
            import maya.cmds as cmds
            cmds.polyCube()


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
