import ctypes
from math import *
from OpenGL.GL import *
import numpy as np
from pyrr import matrix44 as m4
np.set_printoptions(formatter={'float': lambda f: "{:.1f}".format(f)})

class Shape:
    clearColor = 0.2, 0.3, 0.4, 1.0
    enable = [GL_BLEND]
    texture = None
    vertex_buffer = None
    indices = None


    def __init__(self):
        self.initData()

    def settings(self):
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # glEnable(GL_CULL_FACE)
        # glCullFace(GL_BACK)

    def draw(self):
        glDrawElements(GL_TRIANGLE_FAN, 12, GL_UNSIGNED_INT, ctypes.c_void_p(0))
        glDrawElements(GL_TRIANGLE_STRIP, 82, GL_UNSIGNED_INT, ctypes.c_void_p(10 * 4))
        glDrawElements(GL_TRIANGLE_FAN, 12, GL_UNSIGNED_INT, ctypes.c_void_p(92*4))
        glDrawElements(GL_LINES, 6, GL_UNSIGNED_INT, ctypes.c_void_p(104*4))

    def setupBuffers(self):
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(16))

        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)

    def sendData(self):
        glBufferData(GL_ARRAY_BUFFER, self.vertex_buffer.nbytes, self.vertex_buffer, GL_STATIC_DRAW)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.index_buffer.nbytes, self.index_buffer, GL_STATIC_DRAW)

    def initData(self):
        ry = m4.create_from_y_rotation

        pt = np.array([0, 1, 1, 1])
        half = np.array([
            pt,
            ry(np.pi/5) @ pt,
            ry(np.pi/5*2) @ pt,
            ry(np.pi/5*3) @ pt,
            ry(np.pi/5*4) @ pt,
            ])

        frst = np.vstack((half, half @ ry(np.pi)))
        scnd = frst @ ry(-np.pi/10) + [0, -0.5, 0, 0]
        thrd = frst @ ry(-np.pi/10*2) + [0, -1.0, 0, 0]
        frth = frst @ ry(-np.pi/10*3) + [0, -1.5, 0, 0]
        ffth = frst @ ry(-np.pi/10*4) + [0, -2.0, 0, 0]


        north = np.array([0, 1.3, 0, 1])
        south = np.array([0, -1.3, 0, 1])

        vertices = np.vstack(
            (north, frst,
                    scnd,
                    thrd,
                    frth,
                    ffth, south)
        )

        start_color = [0, 0, 0]
        end_color = np.array([np.pi, np.pi, np.pi])

        colors3 = np.vstack(
            ([0, 0, 0],
             np.cos(np.linspace(start_color, end_color * [2, 2, 2] * 5, 50)),
             [0, 0, 0])
        )

        colors4 = np.hstack(
            (colors3,
             np.ones(52).reshape(52, 1))
        ) / 2 + .5

        shape = np.hstack(
            (vertices, colors4)
        )

        lines = np.array([
            [-4, 0, 0, 1],  [.4, .4, .4, 1],
            [4, 0, 0, 1],   [1, 1, 1, 1],
            [0, 0, 0, 1],  [1, .5, .9, 1],
            [0, 4, 0, 1],   [1, 1, 1, 1],
            [0, 0, -2, 1],  [.4, .4, .4, 1],
            [0, 0, 4, 1],   [1, 1, 1, 1],
        ]).reshape(6, 8)

        buffer = np.vstack(
            (shape, lines)
        )


        self.vertex_buffer = np.array(buffer, dtype=np.float32)

        grid = np.mgrid[0:20:10, 1:41]
        interleave = (grid[0] + grid[1]).transpose()
        idx = np.hstack(interleave)
        indices = np.hstack(
                (
                    np.arange(11),
                    idx,
                 [41],
                np.arange(51, 40, -1),
                 [50],
                np.arange(52, 58, 1))
            )

        print(vertices[0])

        self.index_buffer = np.array(indices, dtype=np.uint32)


