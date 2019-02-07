from output import FrameGrabber
from pipeline import Pipeline
import OpenGL.GL as gl
from shape import Shape
import numpy

print("Numpy: {:s}".format(numpy.__version__))

shape = Shape()
pipeline = Pipeline(shape, None)
pipeline.loadShaderFile('shaders/default.vert', gl.GL_VERTEX_SHADER)
pipeline.loadShaderFile('shaders/default.frag', gl.GL_FRAGMENT_SHADER)
pipeline.initGl()
pipeline.sendData()


pipeline.run()
