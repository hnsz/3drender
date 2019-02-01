from pipeline import Pipeline
import OpenGL.GL as gl
from shape import Shape


shape = Shape()

pipeline = Pipeline(shape)
pipeline.loadShaderFile('shaders/default.vert', gl.GL_VERTEX_SHADER)
pipeline.loadShaderFile('shaders/default.frag', gl.GL_FRAGMENT_SHADER)
pipeline.initGl()
pipeline.sendData()


pipeline.run()
