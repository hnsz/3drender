#!./venv/bin/python
import sys
import numpy as np
from pyrr import vector3
from pyrr.vector import normalise
from pyrr.vector3 import cross

import pipeline
import OpenGL.GL as gl

print(sys.version)

indices = np.array([
        0, 1, 2,
        2, 3, 0,
        3, 2, 6,
        6, 7, 3,
        4, 5, 6,
        6, 7, 4,
        1, 0, 4,
        4, 5, 1,
        0, 4, 7,
        7, 3, 0,
        1, 5, 6,
        6, 2, 1

        ], dtype=np.uint32)

vertex_buffer = np.array([
1.0, -1.0, 1.0, 1.0,        1.0, 0.0, 0.0, 0.3,   1.0, 0.0,       #0
1.0, 1.0, 1.0, 1.0,         0.0, 1.0, 0.0, 0.3,   1.0, 1.0,       #1
-1.0, 1.0, 1.0, 1.0,        0.0, 0.0, 1.0, 0.3,   0.0, 1.0,       #2
-1.0, -1.0, 1.0, 1.0,       1.0, 0.0, 0.0, 0.3,   0.0, 0.0,       #3
1.0, -1.0, -1.0, 1.0,       0.0, 1.0, 0.0, 0.3,   0.0, 0.0,       #4
1.0, 1.0, -1.0, 1.0,        0.0, 0.0, 1.0, 0.3,   0.0, 1.0,       #5
-1.0, 1.0, -1.0, 1.0,       1.0, 0.0, 0.0, 0.3,   1.0, 1.0,      #6
-1.0, -1.0, -1.0, 1.0,      0.0, 1.0, 0.0, 0.3,   1.0, 0.0      #7
], dtype=np.float32)



#######   Klooierij
####
# print("")
buffer =vertex_buffer.reshape(8, 10)
vertices3 = buffer[:, :3][indices].reshape(12,3,3)
print("")

for (v0,v1,v2) in vertices3:
    e0 = v1 - v0
    e1 = v2 - v0
    trianorm = normalise(cross(e0, e1))

vert = buffer[:, :4]
col = buffer[:, 4:8]
tex = buffer[:, 8:]
ex = np.concatenate((vert,col,tex),1)
####
#######   Klooierij



pipeline.loadShaderFile('shaders/normal.vert', gl.GL_VERTEX_SHADER)
pipeline.loadShaderFile('shaders/default.frag', gl.GL_FRAGMENT_SHADER)
pipeline.initGl()
pipeline.sendData(vertex_buffer, indices)


pipeline.run()
