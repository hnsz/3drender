from pyrr.matrix44 import create_perspective_projection
import numpy as np
import quaternion as npq
from glfw import *
from OpenGL.GL import *
import math



class MoViPro:
    zoom = 60
    dscroll = 1
    trans = None
    view = None
    proj = None
    lastx = None
    lasty = None
    width, height = 1080, 720
    centerPoint = width/2, height/2
    q0 = None
    qcurrent = None
    qlast = None


    def __init__(s_):
        s_.qcurrent = npq.from_spherical_coords(np.array([0, 0]))
        s_.trans = np.array([1, 0, 0, 0,  0, 1, 0, 0,  0, 0, 1, 0,  0, 0, 0, 1])
        s_.model = np.identity(4)
        s_.eye = np.array([0.0, 1.0, 6.0], dtype=np.float32)
        s_.target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        s_.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        s_.updateModel(s_.qcurrent)
        s_.updateView()
        s_.updateProj()

    def updateView(s_):
        s_.view= s_.constructView(s_.eye, s_.target, s_.up)

    def constructView(s_, eye, target, up):
        def normalise(v):
            norm = np.linalg.norm(v)
            return v / norm if norm else v

        zaxis = normalise(eye - target)
        xaxis = normalise(np.cross(up, zaxis))
        yaxis = np.cross(zaxis, xaxis)
        dots = [-eye @ xaxis, -eye @ yaxis, -eye @ zaxis, 1]

        part = np.vstack((xaxis, yaxis, zaxis, [0,0,0]))
        view = np.vstack((part.transpose(), dots))
        return np.array(view, dtype=np.float32)


    def updateProj(s_):
        s_.proj = create_perspective_projection(s_.zoom, s_.width / s_.height, 0.1, 80.0, dtype=np.float32)

    def updateModel(s_, q):
        m3 = npq.as_rotation_matrix(q)
        B = np.mat('0;0;0')
        C = np.mat('0 0 0')
        D = np.mat('1')
        s_.model = np.bmat([[m3, B], [C, D]])

    def sendData(s_):
        glUniformMatrix4fv(1, 1, GL_FALSE, s_.model)
        glUniformMatrix4fv(2, 1, GL_FALSE, s_.view)
        glUniformMatrix4fv(3, 1, GL_FALSE, s_.proj)


    def callbackMousePos(s_, window, xpos, ypos):
        rad = 3.14159 / 180.0
        w, h = get_window_size(window)
        cw, ch = w / 2, h / 2
        co, si = (xpos-cw)/cw, (ypos-ch)/ch

        if s_.lastx == None or s_.lasty == None:
            s_.lastx, s_.lasty = xpos, ypos
            return

        if s_.d == 0:
            dx = (s_.lastx - xpos)
        else:
            dx = 0
        if s_.d == 1:
            dy = (s_.lasty - ypos)
        else:
            dy = 0

        dx = (s_.lastx - xpos)
        dy = (s_.lasty - ypos)

        q = npq.from_spherical_coords([np.pi/2, 0]).inverse() * \
            npq.from_spherical_coords([np.pi/2, -dy/180]) * \
            npq.from_spherical_coords([dx/180, 0])
        s_.qlast = s_.qcurrent * q
        s_.updateModel(s_.qlast)

        # print(cross)
        s_.sendData()

    def callbackMouseButton(s_, window, button, action, mods):
        if action == PRESS:
            if button == 0:
                s_.d = 0
            elif button == 1:
                s_.d = 1
            else:
                return

            set_cursor_pos_callback(window, s_.callbackMousePos)

        if action == RELEASE and (button == 0 or button == 1):
            s_.lastx, s_.lasty, s_.dx, s_.dy = None, None, None, None
            set_cursor_pos_callback(window, lambda *_: None)
            s_.qcurrent = s_.qlast


    def callbackScroll(s_, window, xoffset, yoffset):
        d = 2.0
        zoom = s_.zoom - d * yoffset
        if zoom < 180.0 - d and zoom > d:
            s_.zoom = zoom

        s_.updateProj()
        s_.sendData()
