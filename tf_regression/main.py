import random
import pygame
import tensorflow as tf

FPS = 0
FPS_CLOCK = pygame.time.Clock()


def maprange(v, a, b) -> float:
    (a1, a2), (b1, b2) = a, b
    return b1 + ((v - a1) * (b2 - b1) / (a2 - a1))


class App:
    BACKGROUND_COLOR = (15, 15, 15)

    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 640, 640
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Snake")
        self._fps_font = pygame.font.Font("freesansbold.ttf", 18)
        self._running = True

        self._dataset = list()

        # regression
        self._degree = 2
        self._coefficients = list()
        for d in range(self._degree + 1):
            self._coefficients.append(
                tf.Variable(random.random())
            )
        # self._m = tf.Variable(random.random())
        # self._b = tf.Variable(random.random())

        # optimizer
        self._optimizer = tf.keras.optimizers.Adagrad(learning_rate=0.2)

    def event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for i in range(10):
                offset_x = random.randint(-30, 30)
                offset_y = random.randint(-30, 30)
                x = maprange(event.pos[0] + offset_x, (0, self.width), (0, 1))
                y = maprange(event.pos[1] + offset_y, (0, self.height), (0, 1))
                self._dataset.append((x, y))

    def loop(self):
        xs = [d[0] for d in self._dataset]
        ys = tf.constant([d[1] for d in self._dataset])
        if len(xs) > 0:
            self._optimizer.minimize(
                lambda: self.loss(predictions=self.predict(x_from_dataset=xs), reality=ys),
                var_list=self._coefficients
            )

    def render(self):
        self._display_surf.fill(self.BACKGROUND_COLOR)

        for each_data in self._dataset:
            x = maprange(each_data[0], (0, 1), (0, self.width))
            y = maprange(each_data[1], (0, 1), (0, self.height))
            pygame.draw.circle(self._display_surf, (240, 240, 240), (x, y), 3)

        xs = [x / 100 for x in range(0, 100)]
        ys = self.predict(xs).numpy()
        points = list()
        for x, y in zip(xs, ys):
            points.append((maprange(x, (0, 1), (0, self.width)), maprange(y, (0, 1), (0, self.height))))
            # begin = (maprange(xs[index], (0, 1), (0, self.width)), maprange(ys[0], (0, 1), (0, self.height)))
            # end = (maprange(xs[index], (0, 1), (0, self.width)), maprange(ys[1], (0, 1), (0, self.height)))
            # pygame.draw.aaline(self._display_surf, (240, 120, 120), begin, end)
        pygame.draw.aalines(self._display_surf, (240, 120, 120), False, points)

        fps = self._fps_font.render(f"fps: {FPS_CLOCK.get_fps():.1f}", True, (200, 10, 10))
        fps_size = fps.get_size()
        self._display_surf.blit(fps, (0, self.height - fps_size[1]))

        pygame.display.update()

    def cleanup(self):
        pygame.quit()

    def execute(self):

        while self._running is True:
            for event in pygame.event.get():
                self.event(event)
            self.loop()
            self.render()
            FPS_CLOCK.tick(FPS)
        self.cleanup()

    def predict(self, x_from_dataset: list) -> tf.Tensor:
        tensor_xs = tf.constant(x_from_dataset, dtype=tf.float32)
        # y = mx + b
        # tensor_ys = tensor_xs.mul(self._m).add(self._b)
        # tensor_ys = tf.add(tf.multiply(tensor_xs, self._m), self._b)
        # tensor_ys = tensor_xs * self._m + self._b
        tensor_ys = tf.constant([1.0] * len(x_from_dataset), dtype=tf.float32)
        for index, each_coefficient in enumerate(self._coefficients):
            exp = self._degree - index
            tensor_exp = tf.constant([exp] * len(x_from_dataset), dtype=tf.float32)
            tensor_ys = tensor_ys + (tf.pow(tensor_xs, tensor_exp) * each_coefficient)
        return tensor_ys

    def loss(self, predictions: tf.Tensor, reality: tf.Tensor) -> tf.Tensor:
        return tf.reduce_mean(tf.math.squared_difference(predictions, reality))


if __name__ == "__main__":
    theApp = App()
    theApp.execute()
