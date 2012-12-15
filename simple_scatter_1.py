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
from fps import fps

LIST_ID = 0
QUIT_VALUE = 99
data = 0

@fps
def display():

    #glVertexPointerf(data)
    glClear(GL_COLOR_BUFFER_BIT)

    #pick a random poitn color
    glColor3f(np.random.random(), np.random.random(), np.random.random())

    #matrix mode is GL_MODELVIEW
    glLoadIdentity()
    gluLookAt(0, 0, 4, 0, 0, 0, 0, 1, 0)

    glCallList(LIST_ID)

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


def init(sz):
    global LIST_ID
    global data

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
