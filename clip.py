"""
Experiment with OpenGL clipping

Use the stencil buffer to clip objects
"""
import sys
from time import time

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

QUIT_VALUE = 99


class fps(object):
    """Print calls per second, once per second"""
    def __init__(self, func):
        self.ctr = 0
        self.t0 = time()
        self.func = func

    def __call__(self, *args, **kwargs):
        self.ctr += 1
        t = time()
        if t - self.t0 > 1:
            print "fps: %0.2f" % (self.ctr / (t - self.t0))
            self.ctr = 0
            self.t0 = t
        return self.func(*args, **kwargs)


def draw_scene(mode=GL_POLYGON):
    xy = np.array([[-1, -1], [-1, 1], [1, 1], [1, -1]]).astype(np.float)
    glColor3f(0, 1, 0)
    glVertexPointerf(xy)
    glDrawArrays(mode, 0, 4)


class Clip(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.data = np.vstack((x, y)).T

    def __enter__(self):
        glEnable(GL_STENCIL_TEST)
        glClear(GL_STENCIL_BUFFER_BIT)

        #divert draws to stencil buffer
        glStencilMask(0xff)   # all bits editable
        glStencilFunc(GL_NEVER, 1, 1)  # test failes = no color/depth draw
        glStencilOp(GL_REPLACE, GL_REPLACE, GL_REPLACE)  # send to stencil
        self.draw()

        #freeze stencil
        glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)
        glStencilFunc(GL_EQUAL, 1, 1)

    def __exit__(self, exc_type, exc_value, traceback):
        glDisable(GL_STENCIL_TEST)

    def draw(self):
        glVertexPointerf(self.data)
        glColor3f(1, 0, 0)
        glDrawArrays(GL_POLYGON, 0, self.x.size)

x0 = 0


def display():
    global x0
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    #define a clipping ellipse that moves to the right
    x0 = (x0 + .01) % 1
    theta = np.linspace(0, 2 * np.pi, 100)
    c = Clip(.5 * np.cos(theta) + x0, np.sin(theta) * 2)

    with c:
        draw_scene()

    #draw original shape in outline
    draw_scene(GL_LINE_LOOP)

    glutSwapBuffers()
    assert glGetError() == GL_NO_ERROR


def reshape(w, h):

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glOrtho(-3, 3, -3, 3, -4, 4)

    glMatrixMode(GL_MODELVIEW)

    assert glGetError() == GL_NO_ERROR


def mainMenuCB(value):
    if value == QUIT_VALUE:
        sys.exit(0)


def init():
    glEnableClientState(GL_VERTEX_ARRAY)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(display)

    main_menu = glutCreateMenu(mainMenuCB)
    glutAddMenuEntry("Quit", QUIT_VALUE)
    glutAttachMenu(GLUT_RIGHT_BUTTON)


def main():
    glutInit([''])

    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE |
                        GLUT_STENCIL)
    glutInitWindowSize(300, 300)
    glutCreateWindow("Simple Example")

    init()

    glutMainLoop()


if __name__ == "__main__":
    main()
