from builtins import OSError, RuntimeError
import glfw
import OpenGL.GL as gl
from movipro import MoViPro
import numpy as np

class Pipeline:


    def __init__(s, shape, frameGrabber):
        s.shape = shape
        s.mvp = MoViPro()
        s.width, s.height = 1280, 960
        s.window = s.initGlfw()
        s.program = gl.glCreateProgram()
        s.frameGrabber = frameGrabber

    def run(s):
        window = s.window
        s.printInfo(window)
        ##   main event loop  ##
        while not glfw.window_should_close(window):
            if glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS:
                break

            s.render()

            glfw.swap_buffers(window)
            if s.frameGrabber:
                s.frameGrabber.saveFrame()

            glfw.poll_events()

        glfw.terminate()


    def initGlfw(s):

        if not glfw.init():
            raise RuntimeError("glfw didn't initialise.")

        glfw.window_hint(glfw.VISIBLE, gl.GL_TRUE)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 5)
        glfw.window_hint(glfw.OPENGL_DEBUG_CONTEXT, gl.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
        glfw.window_hint(glfw.DOUBLEBUFFER, gl.GL_TRUE)

        window = glfw.create_window(s.width, s.height, "3d Rendering", None, None)
        glfw.set_window_pos(window, 0, 0)

        if not window:
            glfw.terminate()
            raise RuntimeError("glfw could not create a window")

        glfw.make_context_current(window)
        glfw.set_window_size_callback(window, s.callbackResize)
        glfw.set_mouse_button_callback(window, s.mvp.callback_mouse_button)
        glfw.set_scroll_callback(window, s.mvp.callback_scroll)

        return window

    def render(s):
        gl.glClearColor(*s.shape.clearColor)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        s.shape.draw()

    def initGl(s):
        voa = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(voa)

        vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)

        ibo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ibo)

        if s.frameGrabber:
            pbo = gl.glGenBuffers(2)
            s.frameGrabber.setPBO(pbo)

        tex = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)

        ## LINK / USE pipeline program  ##
        s.linkProgram()
        gl.glUseProgram(s.program)

        if s.frameGrabber:
            s.frameGrabber.setupBuffers()

        s.shape.setupBuffers()
        s.shape.settings()

    def sendData(s):
        s.shape.sendData()
        s.mvp.sendData()


    def loadShaderFile(s, path, shader_type):
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

        gl.glAttachShader(s.program, shader_object)

    def linkProgram(s):
        program = s.program

        gl.glLinkProgram(program)

        if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
            link_error = gl.glGetProgramInfoLog(program)
            raise RuntimeError(link_error)

        for shdr in gl.glGetAttachedShaders(program):
            gl.glDetachShader(program, shdr)
            gl.glDeleteShader(shdr)

    def callbackResize(s, window, width, height):
        glfw.set_window_aspect_ratio(window, width, height)
        gl.glViewport(0, 0, width, height)


    def printInfo(s, window):
        #   debug info
        info = {}
        info["glfw ver:"] = glfw.get_version_string()
        info["glsl ver:"] = gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)
        info["fb size"] = glfw.get_framebuffer_size(window)
        info["window size"] = glfw.get_window_size(window)
        mon = glfw.get_primary_monitor()
        info["monitor physical size"] = glfw.get_monitor_physical_size(mon)
        info["monitor pos"] = glfw.get_monitor_pos(mon)
        info["display mode"] = glfw.get_video_mode(mon)

        for k in info.keys():
            print("{0}, {1}".format(k, info[k]))



