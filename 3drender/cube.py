from OpenGL.GL import *
import numpy as np
from PIL import Image


class Cube:
    clearColor = 0.2, 0.3, 0.4, 1.0
    image_file = "asset/evaperspectivetool.jpg"
    texture = None
    vertex_buffer = None
    indices = None


    def __init__(self):
        self.initData()

    def draw(self):
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)

    def settings(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)



    def setupBuffers(self):

        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 40, ctypes.c_void_p(0))
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 40,ctypes.c_void_p(16))
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 40, ctypes.c_void_p(32))

        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)

        glUniform1i(0, 0)   # texture

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)



    def sendData(self):
        glBufferData(GL_ARRAY_BUFFER, self.vertex_buffer.nbytes, self.vertex_buffer, GL_STATIC_DRAW)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RG8, 1200, 1599, 0, GL_RGB, GL_UNSIGNED_BYTE, self.texture)



    def initData(self):
        self.vertex_buffer = np.array([
            1.0, -1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.3, 1.0, 0.0,  # 0
            1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.3, 1.0, 1.0,  # 1
            -1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.3, 0.0, 1.0,  # 2
            -1.0, -1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.3, 0.0, 0.0,  # 3
            1.0, -1.0, -1.0, 1.0, 0.0, 1.0, 0.0, 0.3, 0.0, 0.0,  # 4
            1.0, 1.0, -1.0, 1.0, 0.0, 0.0, 1.0, 0.3, 0.0, 1.0,  # 5
            -1.0, 1.0, -1.0, 1.0, 1.0, 0.0, 0.0, 0.3, 1.0, 1.0,  # 6
            -1.0, -1.0, -1.0, 1.0, 0.0, 1.0, 0.0, 0.3, 1.0, 0.0  # 7
        ], dtype=np.float32)


        self.indices = np.array([
            0, 1, 2,
            0, 2, 3,
            3, 2, 6,
            6, 7, 3,
            5, 6, 7,
            5, 7, 4,

            1, 4, 5,
            0, 4, 1,
            0, 4, 7,
            7, 3, 0,
            1, 5, 6,
            6, 2, 1

        ], dtype=np.uint32)

        self.texture = np.array(Image.open(self.image_file, "r"), dtype=np.uint8)

