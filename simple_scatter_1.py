"""
Adapted from OpenGL Distilled book, simple example.

Draws scatter points with numpy arrays.

Renders 10**6 points at 30 fps
        10**7 points at 5  fps
"""
import sys
from time import time

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

LIST_ID = 0
QUIT_VALUE = 99


class fps(object):
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


@fps
def display():

    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()
    glTranslatef(0., 0., -4.)

    glCallList(LIST_ID)

    glutSwapBuffers()

    assert glGetError() == GL_NO_ERROR


def reshape(w, h):

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40., float(w) / float(h), 1.0, 10.0)

    glMatrixMode(GL_MODELVIEW)

    assert glGetError() == GL_NO_ERROR


def mainMenuCB(value):
    if value == QUIT_VALUE:
        sys.exit(0)


def init(sz):
    global LIST_ID

    glDisable(GL_DITHER)

    data = np.random.normal(0, .5, (sz, 2))

    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointerf(data)

    LIST_ID = glGenLists(1)
    glNewList(LIST_ID, GL_COMPILE)

    glDrawArrays(GL_POINTS, 0, sz)

    glEndList()

    assert glGetError() == GL_NO_ERROR

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(display)

    main_menu = glutCreateMenu(mainMenuCB)
    glutAddMenuEntry("Quit", QUIT_VALUE)
    glutAttachMenu(GLUT_RIGHT_BUTTON)


def main(sz=100):
    glutInit([''])

    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(300, 300)
    glutCreateWindow("Simple Example")

    init(sz)

    glutMainLoop()


if __name__ == "__main__":
    main(10**6)
