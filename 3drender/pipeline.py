import ctypes
from builtins import OSError, RuntimeError
import sys
import glfw
import OpenGL.GL as gl
import numpy as np

from pyrr import vector3, Quaternion
from pyrr import matrix44
from PIL import Image
from pyrr.matrix44 import create_identity

model_quat: Quaternion = Quaternion()
last_rot_quat: Quaternion
rotM = None
modelM = None
modelM_p = None
viewM_p = None
projM_p = None
dx = 0.0
dy = 0.0
lastx = None
lasty = None
zoom = 40.0

def run():
    global window

    ##   main event loop  ##
    while not glfw.window_should_close(window):
        if glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS:
            break

        render()
        time = glfw.get_time()
        speed = 100.0
        theta = (time % 360.0) * np.pi/180.0 * speed





        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

def initGlfw():
    if not glfw.init():
        raise RuntimeError("glfw didn't initialise.")


    glfw.window_hint(glfw.VISIBLE, gl.GL_TRUE)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 5)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
    glfw.window_hint(glfw.DOUBLEBUFFER, gl.GL_TRUE)


    window = glfw.create_window(720, 720, "3d Rendering", None, None)
    glfw.set_window_pos(window, 1650-720, 0)

    if not window:
        glfw.terminate()
        raise RuntimeError("glfw could not create a window")

    # cont = glXGetCurrentContext()
    # glXImportContextEXT()

    glfw.make_context_current(window)
    glfw.swap_interval(1)
    glfw.set_window_size_callback(window, callbackResize)
    glfw.set_mouse_button_callback(window, callbackMouseButton)
    glfw.set_scroll_callback(window, callbackScroll)


    #   debug info
    print("glfw ver: {0}".format(glfw.get_version_string().decode()))
    print("glsl ver: {0}".format(gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION).decode()))

    return window


def render():

    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glDrawElements(gl.GL_TRIANGLES, 36, gl.GL_UNSIGNED_INT, None)

def initGl():
    global program, modelM_p, viewM_p, projM_p


    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    # gl.glEnable(gl.GL_DEPTH_TEST)
    # gl.glDepthFunc(gl.GL_LESS)
    gl.glEnable(gl.GL_BLEND)
    gl.glClearColor(0.2, 0.3, 0.4, 1.0)

    # gl.glEnable(gl.GL_CULL_FACE)
    # gl.glCullFace(gl.GL_BACK)

    image_file = "asset/evaperspectivetool.jpg"
    image = Image.open(image_file, "r")

    voa = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(voa)

    vbo = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)

    ibo = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ibo)

    tex = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, tex)

    ## LINK / USE pipeline program  ##
    linkProgram(program)
    gl.glUseProgram(program)


    position_p = gl.glGetAttribLocation(program, "position")
    gl.glVertexAttribPointer(position_p, 4, gl.GL_FLOAT, gl.GL_FALSE, 40, ctypes.c_void_p(0))
    gl.glEnableVertexAttribArray(position_p)

    color_p = gl.glGetAttribLocation(program, "color")
    gl.glVertexAttribPointer(color_p, 4, gl.GL_FLOAT, gl.GL_FALSE, 40,ctypes.c_void_p(16))
    gl.glEnableVertexAttribArray(color_p)

    texcoord_p = gl.glGetAttribLocation(program, "texCoord")
    gl.glVertexAttribPointer(texcoord_p, 2, gl.GL_FLOAT, gl.GL_FALSE, 40, ctypes.c_void_p(32))
    gl.glEnableVertexAttribArray(texcoord_p)

    tex_p = gl.glGetUniformLocation(program, "tex")
    gl.glUniform1i(tex_p, 0)

    modelM_p = gl.glGetUniformLocation(program, "model")
    viewM_p = gl.glGetUniformLocation(program, "view")
    projM_p = gl.glGetUniformLocation(program, "proj")

    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)


    img_data = np.array(image, dtype=np.uint8)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RG8, 1200, 1599, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img_data)





def sendData(vertex_buffer, indices):
    global program
    global posx, posy
    global modelM_p
    global modelM
    global zoom
    global model_quat, last_rot_quat

    eye = vector3.create(0.0, 2.0, 6.0, dtype=np.float32)
    target = vector3.create(0.0, 0.0, 0.0, dtype=np.float32)
    up = vector3.create(0.0, 1.0, 0.0, dtype=np.float32)


    transM = matrix44.create_from_translation(vector3.create(0.0, 0.0, 0.0, dtype=np.float32))
    viewM = matrix44.create_from_translation(vector3.create(0.0, 0.0, -3.0, dtype=np.float32))
    projM = matrix44.create_perspective_projection(zoom, 1080.0/720.0, 0.1, 80.0, dtype=np.float32)
    viewM = matrix44.create_look_at(eye, target, up)

    # send model data
    gl.glBufferData(gl.GL_ARRAY_BUFFER, vertex_buffer.nbytes, vertex_buffer, gl.GL_STATIC_DRAW)
    gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, gl.GL_STATIC_DRAW)


    id = matrix44.create_identity()


    model_quat = Quaternion.from_matrix(id)
    last_rot_quat = Quaternion.from_matrix(id)

    modelM = id

    updateModelMatrix(modelM)
    gl.glUniformMatrix4fv(viewM_p, 1, gl.GL_FALSE, viewM)
    gl.glUniformMatrix4fv(projM_p, 1, gl.GL_FALSE, projM)

def printQ(quat: Quaternion):
    print("qid: {0}\ntheta: {1}\nqaxis: {2}\n".format(quat, quat.angle, quat.axis))

def updateModelMatrix(matrix):
    global modelM_p
    gl.glUniformMatrix4fv(modelM_p, 1, gl.GL_FALSE, matrix)

def loadShaderFile(path, shader_type):
    global program

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

    gl.glAttachShader(program, shader_object)


def linkProgram(program):
    # link
    gl.glLinkProgram(program)

    if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
        link_error = gl.glGetProgramInfoLog(program)
        raise RuntimeError(link_error)

    # detach shaders
    for shdr in gl.glGetAttachedShaders(program):
        gl.glDetachShader(program, shdr)
        gl.glDeleteShader(shdr)

def callbackResize(window, width, height):
    glfw.set_window_aspect_ratio(window, width, height)
    gl.glViewport(0, 0, width, height)

def callbackMousePos(window, xpos, ypos):
    global modelM, model_quat, last_rot_quat, lastx, lasty, dx, dy, rotM
    rad = 3.14159 / 180.0

    if lastx == None or lasty == None:
        lastx, lasty = xpos, ypos
        model_quat = last_rot_quat

        return

    elif dx == None or dy == None:
        dx, dy = 0.0, 0.0

    dx = (lastx - xpos)
    dy = (lasty - ypos)


    # print("({0},{1} dx: {2}, dy: {3})".format(xpos,ypos,dx,dy))

    qy = Quaternion.from_eulers(vector3.create(dy * rad, dx * rad, 0, dtype=np.float32))

    res_quat = qy * model_quat
    last_rot_quat = res_quat.normalised
    printQ(last_rot_quat)

    rotM = matrix44.create_from_quaternion(last_rot_quat)
    modelM = rotM
    #  conjugate
    updateModelMatrix(modelM)




def callbackMouseButton(window, button, action, mods):
    global lastx, lasty, xpos, ypos, dx, dy
    if button == 0 and action == glfw.PRESS:
        glfw.set_cursor_pos_callback(window, callbackMousePos)

    if button == 0 and action == glfw.RELEASE:
        print("({0},{1} dx: {2}, dy: {3})".format(lastx, lasty, dx,dy))

        lastx, lasty, dx, dy = None, None, None, None
        glfw.set_cursor_pos_callback(window, lambda *_: None)


def callbackScroll(window, xoffset, yoffset):
    global zoom
    zoom = zoom + yoffset
    print("zoom: ", zoom)



window = initGlfw()
program = gl.glCreateProgram()
