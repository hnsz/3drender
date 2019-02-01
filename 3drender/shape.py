from math import *
from OpenGL.GL import *
import numpy as np
from pyrr import matrix44 as m4
np.set_printoptions(formatter={'float':lambda f: "{:.1f}".format(f)})

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
        glDrawArrays(GL_TRIANGLE_FAN, 0, 13)
        glDrawArrays(GL_TRIANGLE_STRIP, 13, 96)
        glDrawArrays(GL_TRIANGLE_FAN, 133, 13)
        glDrawArrays(GL_LINES, 133+13, 6)

    def setupBuffers(self):
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(16))

        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)

    def sendData(self):
        glBufferData(GL_ARRAY_BUFFER, self.vertex_buffer.nbytes, self.vertex_buffer, GL_STATIC_DRAW)

    def initData(self):
        ry = m4.create_from_y_rotation
        transl = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, -0.5, 0, 1]
        ])
        def scale(*v):
            return np.array([
            [v[0], 0, 0, 0],
            [0, v[1], 0, 0],
            [0, 0, v[2], 0],
            [0, 0, 0, 1]
            ])
        pt = np.array([0, 1, 1, 1])
        half = np.array([
            pt,
            ry(np.pi/5) @ pt,
            ry(np.pi/5*2) @ pt,
            ry(np.pi/5*3) @ pt,
            ry(np.pi/5*4) @ pt,
            ry(np.pi) @ pt
            ])

        fst = np.vstack((half, half @ ry(np.pi)))
        snd = fst @ ry(-np.pi/10) @ transl

        strip1 = np.hstack((fst, snd)).reshape(24, 4)
        strip2 = strip1 @ transl @ ry(-np.pi/10)
        strip3 = strip2 @ transl @ ry(-np.pi/10)
        strip4 = strip3 @ transl @ ry(-np.pi/10)
        strip5 = strip4 @ transl @ ry(-np.pi/10)



        strip3 = strip3 @ scale(1.7, 1, 1.7)
        strip1[1::2] = strip1[1::2] @ scale(1.5, 1, 1.5)
        strip2[0::2] = strip2[0::2] @ scale(1.5, 1, 1.5)
        strip2[1::2] = strip2[1::2] @ scale(1.7, 1, 1.7)
        strip4[0::2] = strip4[0::2] @ scale(1.7, 1, 1.7)
        strip4[1::2] = strip4[1::2] @ scale(1.5, 1, 1.5)

        fantop = np.vstack (([0, 1.3, 0, 1], strip1[::2]))
        fanbtm = np.vstack (([0, -1.3, 0, 1], strip4[1::2]))



        lines = np.array([
            [-4, 0, 0, 1],  [.4, .4, .4, 1],
            [4, 0, 0, 1],   [1, 1, 1, 1],
            [0, 0, 0, 1],  [1, .5, .9, 1],
            [0, 4, 0, 1],   [1, 1, 1, 1],
            [0, 0, -2, 1],  [.4, .4, .4, 1],
            [0, 0, 4, 1],   [1, 1, 1, 1],
        ]).reshape(6, 8)

        vectors = np.vstack((fantop, strip1, strip2, strip3, strip4, strip5, fanbtm))
        n = vectors.shape[0]
        colors = np.vstack((
            np.sin(np.linspace(np.pi, np.pi*(13+24*10+13), n)),
            np.sin(np.linspace(0, np.pi*(13+24*10+13), n)),
            np.cos(np.linspace(np.pi, np.pi*(13+24*10+13), n)),
            np.ones(n)
            ),
        ).transpose() / 2 + .5
        data = np.hstack((vectors, colors))

        buffer = np.vstack((data, lines))
        self.vertex_buffer = np.array(buffer, dtype=np.float32)

        print(self.vertex_buffer.nbytes)
