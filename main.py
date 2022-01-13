import math
import random
import time

from numba import jit

import pygame
import pygame.freetype


class Circle:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.speed = 40
        self.radius = random.randrange(20, 100)
        self.x = random.randrange(0, 1000)
        self.y = random.randrange(0, 700)
        self.dx = random.randrange(-self.speed, self.speed)
        self.dy = random.randrange(-self.speed, self.speed)
        self.color = (random.randrange(0, 255), random.randrange(
            0, 255), random.randrange(0, 255))

    def update(self, delta_time):
        if self.x >= self.w:
            self.dx = -abs(self.dx)
        elif self.x <= 0:
            self.dx = abs(self.dx)

        if self.y >= self.h:
            self.dy = -abs(self.dy)
        elif self.y <= 0:
            self.dy = abs(self.dy)

        self.x += self.dx * delta_time
        self.y += self.dy * delta_time

    def render(self, screen):
        # pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.ellipse(screen, self.color,
                            (self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2), 1)


# BEGIN PARAMS
width = 1000
height = 700
circle_count = 10
step = 10
DEBUG = False
level = 1
# END PARAMS

# private
CIRCLES = []
screen = None
pygame.init()
screen = pygame.display.set_mode([width, height])
running = True
font = pygame.font.SysFont('Comic Sans MS', 10)
ft_font = pygame.freetype.SysFont('Sans', 15)
value_table = [[0 for y in range(int(height/step))]
               for x in range(int(width/step))]


LINES = []


def distance(pos, circle):
    return math.sqrt(math.pow(pos[0] - circle.x, 2) + math.pow(pos[1] - circle.y, 2))


def get_state(a, b, c, d):
    global level
    if a < level and b < level and c < level and d < level:
        return 0
    elif a < level and b < level and c < level and d >= level:
        return 1
    elif a < level and b < level and c >= level and d < level:
        return 2
    elif a < level and b < level and c >= level and d >= level:
        return 3
    elif a < level and b >= level and c < level and d < level:
        return 4
    elif a < level and b >= level and c < level and d >= level:
        return 5
    elif a < level and b >= level and c >= level and d < level:
        return 6
    elif a < level and b >= level and c >= level and d >= level:
        return 7
    elif a >= level and b < level and c < level and d < level:
        return 8
    elif a >= level and b < level and c < level and d >= level:
        return 9
    elif a >= level and b < level and c >= level and d < level:
        return 10
    elif a >= level and b < level and c >= level and d >= level:
        return 11
    elif a >= level and b >= level and c < level and d < level:
        return 12
    elif a >= level and b >= level and c < level and d >= level:
        return 13
    elif a >= level and b >= level and c >= level and d < level:
        return 14
    elif a >= level and b >= level and c >= level and d >= level:
        return 15


def scale(point):
    global step
    return (point[0] * step, point[1] * step)


def marching_squares():
    global LINES
    LINES = []
    for x in range(int(width/step) - 1):
        for y in range(int(height/step) - 1):
            state = get_state(
                value_table[x][y], value_table[x + 1][y], value_table[x + 1][y + 1], value_table[x][y + 1])
            a = scale((x + 0.5, y))
            b = scale((x + 1, y + 0.5))
            c = scale((x + 0.5, y + 1))
            d = scale((x, y + 0.5))
            if state == 1:
                LINES.append((c, d))
            elif state == 2:
                LINES.append((b, c))
            elif state == 3:
                LINES.append((b, d))
            elif state == 4:
                LINES.append((a, b))
            elif state == 5:
                LINES.append((a, d))
                LINES.append((b, c))
            elif state == 6:
                LINES.append((a, c))
            elif state == 7:
                LINES.append((a, d))
            elif state == 8:
                LINES.append((a, d))
            elif state == 9:
                LINES.append((a, c))
            elif state == 10:
                LINES.append((a, b))
                LINES.append((c, d))
            elif state == 11:
                LINES.append((a, b))
            elif state == 12:
                LINES.append((b, d))
            elif state == 13:
                LINES.append((b, c))
            elif state == 14:
                LINES.append((c, d))


def calc_sumed_distances_to_circles(pos):
    global CIRCLES
    sum = 0
    for circle in CIRCLES:
        if not circle.x == pos[0] and not circle.y == pos[1]: 
            sum += (math.pow(circle.radius, 2) / (math.pow(pos[0] - circle.x, 2) + math.pow(pos[1] - circle.y, 2)))
    return sum


def init():
    global CIRCLES, width, height, circle_count
    for i in range(circle_count):
        CIRCLES.append(Circle(width, height))


def draw_text(txt, pos, color=(0, 0, 0)):
    global font, screen
    ft_font.render_to(screen, pos, txt, color)


def hight_map(number):
    number = clamp(number, 0, 1)
    number *= 255
    col = (110 - number * (110 / 255), 110 - number/8, 110)
    return col


def clamp(value, _min, _max):
    return max(min(value, _max), _min)


def calc_values():
    global value_table
    for x in range(int(width / step)):
        for y in range(int(height / step)):
            dist = calc_sumed_distances_to_circles((x * step, y * step))
            value_table[x][y] = dist


def render_debug():
    global screen, value_table
    for x in range(int(width / step)):
        for y in range(int(height / step)):
            col = hight_map(value_table[x][y])
            pygame.draw.rect(screen, col, (x * step, y * step, step, step))
            if DEBUG:
                draw_text(
                    str(round(value_table[x][y], 4)), (x * step, y * step))


def render_grid():
    global screen, width, height, step
    for x in range(int(width / step)):
        pygame.draw.line(screen, (0, 0, 0),
                         (x * step, 0), (x * step, height), 1)
    for y in range(int(height / step)):
        pygame.draw.line(screen, (0, 0, 0),
                         (0, y * step), (width, y * step), 1)


def handle_input():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


def update(delta_time):
    global CIRCLES
    start = time.time()
    calc_values()
    end = time.time()
    print("    Calc_Values: " + str(end - start))
    start = time.time()
    marching_squares()
    end = time.time()
    print("    Marching_Squares: " + str(end - start))
    start = time.time()
    for circle in CIRCLES:
        circle.update(delta_time)
    end = time.time()
    print("    Update Circles: " + str(end - start))


def render_lines():
    global screen, LINES
    for line in LINES:
        pygame.draw.line(screen, (0, 0, 0), line[0], line[1])


def render(screen):
    screen.fill((255, 255, 255))

#    render_grid()
#    render_debug()

    render_lines()

    if DEBUG:
        for circle in CIRCLES:
            circle.render(screen)

    pygame.display.flip()


def main():
    global running
    init()
    get_ticks_last_frame = 0
    while running:
        t = pygame.time.get_ticks()
        delta_time = (t - get_ticks_last_frame) / 1000.0
        handle_input()
        start = time.time()
        update(delta_time)
        end = time.time()
        print("Update: " + str(end - start) + " - " + str(1/(end - start)))
        start = time.time()
        render(screen)
        end = time.time()
        print("Render:" + str(end - start))
        get_ticks_last_frame = t

    pygame.quit()


if __name__ == "__main__":
    main()
