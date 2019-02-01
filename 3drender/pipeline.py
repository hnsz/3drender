import ctypes
from builtins import OSError, RuntimeError
import sys
import glfw
import OpenGL.GL as gl
import numpy as np
from movipro import MoViPro


class Pipeline:

    def __init__(self, shape):
        self.shape = shape
        self.mvp = MoViPro()
        self.window = self.initGlfw()
        self.program = gl.glCreateProgram()

    def run(self):
        window = self.window

        ##   main event loop  ##
        while not glfw.window_should_close(window):
            if glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS:
                break

            self.render()
            time = glfw.get_time()
            speed = 100.0
            theta = (time % 360.0) * np.pi / 180.0 * speed

            glfw.swap_buffers(window)
            glfw.poll_events()

        glfw.terminate()

    def initGlfw(self):

        if not glfw.init():
            raise RuntimeError("glfw didn't initialise.")

        glfw.window_hint(glfw.VISIBLE, gl.GL_TRUE)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 5)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
        glfw.window_hint(glfw.DOUBLEBUFFER, gl.GL_TRUE)

        window = glfw.create_window(1080, 720, "3d Rendering", None, None)
        glfw.set_window_pos(window, 1650 - 720, 0)

        if not window:
            glfw.terminate()
            raise RuntimeError("glfw could not create a window")

        # cont = glXGetCurrentContext()
        # glXImportContextEXT()

        glfw.make_context_current(window)
        glfw.swap_interval(1)
        glfw.set_window_size_callback(window, self.callbackResize)
        glfw.set_mouse_button_callback(window, self.mvp.callbackMouseButton)
        glfw.set_scroll_callback(window, self.mvp.callbackScroll)

        #   debug info
        print("glfw ver: {0}".format(glfw.get_version_string().decode()))
        print("glsl ver: {0}".format(gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION).decode()))

        return window

    def render(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glDrawElements(gl.GL_TRIANGLES, 36, gl.GL_UNSIGNED_INT, None)

    def initGl(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        # gl.glEnable(gl.GL_DEPTH_TEST)
        # gl.glDepthFunc(gl.GL_LESS)
        gl.glEnable(gl.GL_BLEND)
        gl.glClearColor(*self.shape.clearColor)

        # gl.glEnable(gl.GL_CULL_FACE)
        # gl.glCullFace(gl.GL_BACK)

        voa = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(voa)

        vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)

        ibo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ibo)

        tex = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)

        ## LINK / USE pipeline program  ##
        self.linkProgram()
        gl.glUseProgram(self.program)

        self.shape.setupBuffers()

    def sendData(self):
        self.shape.sendData()
        self.mvp.sendData()


    def loadShaderFile(self, path, shader_type):
        try:
            fh = open(path, "r")
            shader_text = str(fh.read())
            fh.close()
        except OSError as error:
            raise RuntimeError("Error loading shader: {0}".format(error))
        except:
            raise RuntimeError("Nnknow error reading shaderfile {0}".format(path))

        shader_object = gl.glCreateShader(shader_type)
        gl.glShaderSource(shader_object, shader_text)
        gl.glCompileShader(shader_object)

        if not gl.glGetShaderiv(shader_object, gl.GL_COMPILE_STATUS):
            glsl_error = gl.glGetShaderInfoLog(shader_object)
            raise RuntimeError(glsl_error.decode())

        gl.glAttachShader(self.program, shader_object)

    def linkProgram(self):
        program = self.program

        gl.glLinkProgram(program)

        if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
            link_error = gl.glGetProgramInfoLog(program)
            raise RuntimeError(link_error)

        for shdr in gl.glGetAttachedShaders(program):
            gl.glDetachShader(program, shdr)
            gl.glDeleteShader(shdr)

    def callbackResize(self, window, width, height):
        glfw.set_window_aspect_ratio(window, width, height)
        gl.glViewport(0, 0, width, height)
