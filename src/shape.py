import ctypes
from OpenGL.GL import *
import numpy as np

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
        nrestartvalues = 4
        strip = 88 + nrestartvalues
        glDrawElements(GL_TRIANGLE_FAN, fan, GL_UNSIGNED_INT, ctypes.c_void_p(0))
        glDrawElements(GL_TRIANGLE_STRIP, strip, GL_UNSIGNED_INT, ctypes.c_void_p(fan * 4))
        glDrawElements(GL_TRIANGLE_FAN, fan, GL_UNSIGNED_INT, ctypes.c_void_p((fan + strip) * 4))
        # glDrawElements(GL_LINES, 6, GL_UNSIGNED_INT, ctypes.c_void_p((fan + strip + fan) * 4))

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
        ry = lambda t: np.array([np.cos(t),0,np.sin(t),0, 0,1,0,0, -np.sin(t),0,np.cos(t),0, 0,0,0,1]).reshape(4,4)

        pt = np.array([0, 1.5, 1, 1])
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
        ffth = frst @ ry(-np.pi / 10 * 4) + [0, -2.5, 0, 0]


        northFan = np.vstack(([0, 1.9, 0, 1], frst))
        southFan = np.vstack(([0, -1.9, 0, 1], ffth))

        vertices = np.vstack(
            (northFan,
             frst,
             scnd,
             cntr,
             frth,
             ffth,
             southFan)
        )

        normals = np.vstack(
            ([0, 1, 0],
            frst[:, :3],

            cntr[:, :3],
            cntr[:, :3],
            cntr[:, :3],
            cntr[:, :3],
            cntr[:, :3],

            ffth[:, :3],
            [0, -1, 0])
        )

        colors = np.vstack(
            (np.array([.3, .4, .3, .7]).repeat(11).reshape(4, 11).transpose(),
             np.array([.3, .4, .3, .7]).repeat(10).reshape(4, 10).transpose(),
             np.array([.3, .4, .3, .7]).repeat([30]).reshape(4, 30).transpose(),
             np.array([.3, .4, .3, .7]).repeat(10).reshape(4, 10).transpose(),
             np.array([.3, .4, .3, .7]).repeat(11).reshape(4, 11).transpose()
             ))


        shape = np.hstack(
            (vertices, colors, normals)
        )

        lines = np.array([
            3, 0, 0, 1, 1, 1, 1, 1,  0, 0, 0,
            -3, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0,
            0, 3, 0, 1, 1, 1, 1, 1,  0, 0, 0,
            0, -3, 0, 1, 1, 1, 1, 1, 0, 0, 0,
            0, 0, 3, 1, 1, 1, 1, 1,  0, 0, 0,
            0, 0, -3, 1, 1, 1, 1, 1, 0, 0, 0
        ]).reshape(6, 11)

        buffer = np.vstack(
            (shape, lines)
        )

        self.vertex_buffer = np.array(buffer, dtype=np.float32)

        glEnable(GL_PRIMITIVE_RESTART_FIXED_INDEX)
        strip_element = np.array(
            [1, 11, 2, 12, 3,
             13, 4, 14, 5, 15,
             6, 16, 7, 17, 8,
             18, 9, 19, 10, 20,
             1, 11, 2])
        indices = np.hstack((
                np.arange(11), [1],
                strip_element[:-1] + 10, [0xFFFFFF],
                strip_element[1:] + 20, [0xFFFFFF],
                strip_element[:-1] + 30, [0xFFFFFF],
                strip_element[1:] + 40, [0xFFFFFF],
                [61,62,71,70,69,68,67,66,65,64,63,62],
                # np.arange(12 + 88 + 12, 12 + 88 + 12 + 6)
        ))
        print(vertices)


        self.index_buffer = np.array(indices, dtype=np.uint32)
