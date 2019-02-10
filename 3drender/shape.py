import ctypes
from math import *
from OpenGL.GL import *
import numpy as np
from pyrr import matrix44 as m4

np.set_printoptions(formatter={'float': lambda f: "{:.1f}".format(f)})


class Shape:
    clearColor = 45/255.0, 57/255.0, 56/255.0, 1
    enable = [GL_BLEND]
    texture = None
    vertex_buffer = None
    indices = None

    def __init__(self):
        self.initData()

    def settings(self):
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        # glEnable(GL_BLEND)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

    def draw(self):
        fan = 12
        stopvalues = 4
        strip = 88 + stopvalues
        glDrawElements(GL_TRIANGLE_FAN, fan, GL_UNSIGNED_INT, ctypes.c_void_p(0))
        glDrawElements(GL_TRIANGLE_STRIP, strip, GL_UNSIGNED_INT, ctypes.c_void_p(fan * 4))
        glDrawElements(GL_TRIANGLE_FAN, fan, GL_UNSIGNED_INT, ctypes.c_void_p((fan + strip) * 4))
        glDrawElements(GL_LINES, 6, GL_UNSIGNED_INT, ctypes.c_void_p((fan + strip + fan) * 4))

    def setupBuffers(self):
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(0))
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_TRUE, 44, ctypes.c_void_p(16))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(32))

        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)

    def sendData(self):
        glBufferData(GL_ARRAY_BUFFER, self.vertex_buffer.nbytes, self.vertex_buffer, GL_STATIC_DRAW)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.index_buffer.nbytes, self.index_buffer, GL_STATIC_DRAW)

    def initData(self):
        ry = m4.create_from_y_rotation

        pt = np.array([0, 1.5, 1.5, 1])
        half = np.array([
            pt,
            ry(np.pi / 5) @ pt,
            ry(np.pi / 5 * 2) @ pt,
            ry(np.pi / 5 * 3) @ pt,
            ry(np.pi / 5 * 4) @ pt,
        ])

        frst = np.vstack((half, half @ ry(np.pi)))
        scnd = frst @ ry(-np.pi / 10) + [0, -0.5, 0, 0]
        cntr = (frst @ ry(-np.pi / 10 * 2) + [0, -1.0, 0, 0])
        frth = frst @ ry(-np.pi / 10 * 3) + [0, -2.0, 0, 0]
        ffth = frst*[.7,1.1,.7,1] @ ry(-np.pi / 10 * 4) + [0, -2.5, 0, 0]
        frst = frst * [.7, 1, .7, 1]

        north = np.array([0, 1.9, 0, 1])
        south = np.array([0, -1.1, 0, 1])

        vertices = np.vstack(
            (north, frst,
             scnd,
             cntr,
             frth,
             ffth, south)
        )

        normals = np.vstack(
            ([0, 1, 0],
            frst[:,:3],
            scnd[:,:3],
            cntr[:,:3],
            frth[:,:3],
            ffth[:,:3],
            [0, -1, 0])
        )

        colors = np.vstack(
            ([.1, .6, .9, .7],
             np.array([.1, .6, .9, .7]).repeat(10).reshape(4, 10).transpose(),
             np.array([.1, .6, .9, .7]).repeat([30]).reshape(4, 30).transpose(),
             np.array([.1, .6, .9, .7]).repeat(10).reshape(4, 10).transpose(),
             [.1, .6, .9, .7])
        )


        shape = np.hstack(
            (vertices, colors, normals)
        )

        lines = np.array([
            -4, 0, 0, 1, 1, 1, 1, 1, -1, 1, 0,
            4, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0,
            0, -4, 0, 1, 1, 1, 1, 1, 0, -1, 0,
            0, 4, 0, 1, 1, 1, 1, 1, 0, 1, 0,
            0, 0, -4, 1, 1, 1, 1, 1, 0, 0, -1,
            0, 0, 4, 1, 1, 1, 1, 1, 0, 0, 1
        ]).reshape(6, 11)

        buffer = np.vstack(
            (shape, lines)
        )

        self.vertex_buffer = np.array(buffer, dtype=np.float32)

        glEnable(GL_PRIMITIVE_RESTART_FIXED_INDEX)
        strip_element = np.array(
            [10, 20, 1, 11, 2, 12, 3, 13, 4, 14, 5, 15,
             6, 16, 7, 17, 8, 18, 9, 19, 10, 20, 1])
        indices = np.hstack(
            (
                np.arange(11), [1],
                strip_element[:-1], [0xFFFFFF],
                strip_element[1:] + 10, [0xFFFFFF],
                strip_element[:-1] + 20, [0xFFFFFF],
                strip_element[1:] + 30, [0xFFFFFF],
                np.arange(51, 40, -1),
                [50],
                np.arange(52, 58, 1))
        )


        self.index_buffer = np.array(indices, dtype=np.uint32)
