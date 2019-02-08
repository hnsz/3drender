from output import FrameGrabber
from pipeline import Pipeline
import OpenGL.GL as gl
from shape import Shape
import numpy

print("Numpy: {:s}".format(numpy.__version__))

fg = FrameGrabber()
shape = Shape()
pipeline = Pipeline(shape, fg)
pipeline.loadShaderFile('shaders/illumination.vert', gl.GL_VERTEX_SHADER)
pipeline.loadShaderFile('shaders/illumination.frag', gl.GL_FRAGMENT_SHADER)
pipeline.initGl()
pipeline.sendData()


pipeline.run()

fg.finish()