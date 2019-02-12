from builtins import OSError, RuntimeError
from glfw import *
import OpenGL.GL as gl
from src.movipro import MoViPro


class Pipeline:

    def __init__(s, shape, frameGrabber):
        s.shape = shape
        s.mvp = MoViPro()
        s.width, s.height = 1080, 720
        s.window = s.initGlfw()
        s.program = gl.glCreateProgram()
        s.frameGrabber = frameGrabber

    def run(s):
        window = s.window
        s.printInfo(window)

        #   main event loop
        while not window_should_close(window):
            if get_key(window, KEY_Q) == PRESS:
                break

            s.render()

            swap_buffers(window)
            if s.frameGrabber:
                s.frameGrabber.saveFrame()

            poll_events()

        terminate()

    def initGlfw(s):

        if not init():
            raise RuntimeError("glfw didn't initialise.")

        window_hint(VISIBLE, gl.GL_TRUE)
        window_hint(CONTEXT_VERSION_MAJOR, 4)
        window_hint(CONTEXT_VERSION_MINOR, 5)
        window_hint(OPENGL_DEBUG_CONTEXT, gl.GL_TRUE)
        window_hint(OPENGL_PROFILE, OPENGL_CORE_PROFILE)
        window_hint(OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
        window_hint(DOUBLEBUFFER, gl.GL_TRUE)

        window = create_window(s.width, s.height, "3d Rendering", None, None)
        set_window_pos(window, 1920 - s.width, 0)

        if not window:
            terminate()
            raise RuntimeError("glfw could not create a window")

        make_context_current(window)
        set_window_size_callback(window, s.callbackResize)
        set_mouse_button_callback(window, s.mvp.callback_mouse_button)
        set_scroll_callback(window, s.mvp.callback_scroll)

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
        set_window_aspect_ratio(window, width, height)
        gl.glViewport(0, 0, width, height)

    def printInfo(s, window):
        #   debug info
        info = {}
        info["glfw ver:"] = get_version_string()
        info["glsl ver:"] = gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)
        info["fb size"] = get_framebuffer_size(window)
        info["window size"] = get_window_size(window)
        mon = get_primary_monitor()
        info["monitor physical size"] = get_monitor_physical_size(mon)
        info["monitor pos"] = get_monitor_pos(mon)
        info["display mode"] = get_video_mode(mon)

        # for k in info.keys():
        #     print("{0}, {1}".format(k, info[k]))
