from src.pipeline import Pipeline
import OpenGL.GL as gl
from src.shape import Shape
import numpy

print("Numpy: {:s}".format(numpy.__version__))

# fg = FrameGrabber()
shape = Shape()
pipeline = Pipeline(shape, None)
pipeline.loadShaderFile('shaders/diffuse.vert', gl.GL_VERTEX_SHADER)
pipeline.loadShaderFile('shaders/diffuse.frag', gl.GL_FRAGMENT_SHADER)
pipeline.initGl()
pipeline.sendData()


pipeline.run()

# fg.finish()