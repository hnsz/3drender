import glm as glm
import numpy as np

from pipeline import Pipeline
import OpenGL.GL as gl
from cube import Cube




cube = Cube()
pipeline = Pipeline(cube)

pipeline.loadShaderFile('shaders/normal.vert', gl.GL_VERTEX_SHADER)
pipeline.loadShaderFile('shaders/default.frag', gl.GL_FRAGMENT_SHADER)
pipeline.initGl()
pipeline.sendData()


pipeline.run()
