import os
import sys
import random
import math

gradient_x_max = 250

gradient_y_max = 250


def build_gradient():
    gradient = []
    random.seed()
    for y in range(gradient_y_max):
        gradient.append([])
        for x in range(gradient_x_max):
            gradient[y].append((random.uniform(-85000, 85000),
                                random.uniform(-85000, 85000),
                                random.uniform(-85000, 85000)))
    # print(str(gradient))
    return gradient


def lerp(a0, a1, w):
    return ((float(1.0)-w)*a0) + (w * a1)


def dotGridGradient(gradient, ix, iy, x, y):
    dx = x - float(ix)
    dy = y - float(iy)

    try:
        a = dx*gradient[iy][ix][0] + dy*gradient[iy][ix][1]
    except Exception:
        print("dx = " + str(dx))
        print("iy = " + str(iy))
        print("ix = " + str(ix))
        print("gradient = " + str(gradient))

    return dx*gradient[iy][ix][0] + dy*gradient[iy][ix][1]


def perlin(gradient, x, y):

    x0 = int(x)
    x1 = x0 + 1
    y0 = int(y)
    y1 = y0 + 1

    sx = x - float(x0)
    sy = y - float(y0)

    n0 = float(dotGridGradient(gradient, x0, y0, x, y))
    n1 = float(dotGridGradient(gradient, x1, y0, x, y))
    ix0 = float(lerp(n0, n1, sx))

    n0 = float(dotGridGradient(gradient, x0, y1, x, y))
    n1 = float(dotGridGradient(gradient, x1, y1, x, y))
    ix1 = float(lerp(n0, n1, sx))

    return float(lerp(ix0, ix1, sy))


def generate_perlin_noise(gradient):
    final_gradient = []
    for y in range(len(gradient)-1):
        final_gradient.append([])
        for x in range(len(gradient[y])-1):
            final_gradient[y].append(perlin(gradient,
                                            (x*1/(gradient_x_max-1)),
                                            (y*1/(gradient_y_max-1))
                                            ))

    return final_gradient
