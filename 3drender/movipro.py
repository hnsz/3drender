from pyrr import matrix44, vector3, vector4
import numpy as np
from glfw import *
from OpenGL.GL import *
from quaternion import *
import math
from quaternion.numpy_quaternion import quaternion


class MoViPro:
    zoom = 60
    dscroll = 1
    trans = None
    view = None
    proj = None
    lastx = None
    lasty = None
    displayWidth, displayHeight = 1080, 720
    centerPoint = 1080/2, 720/2
    qstart = None


    def __init__(self):
        self.last_rot_quat = from_euler_angles([0, 0, 0])
        self.trans = matrix44.create_from_translation(vector3.create(2.0, 0.0, 0.0, dtype=np.float32))
        self.model = matrix44.create_identity()
        self.eye = vector3.create(0.0, 1.0, 6.0, dtype=np.float32)
        self.target = vector3.create(0.0, 0.0, 0.0, dtype=np.float32)
        self.up = vector3.create(0.0, 10.0, 0.0, dtype=np.float32)
        self.updateView()
        self.updateProj()



    def updateView(s):
        s.view = matrix44.create_look_at(s.eye, s.target, s.up)

    def updateProj(self):
        self.proj = matrix44.create_perspective_projection(self.zoom, self.displayWidth / self.displayHeight, 0.1, 80.0, dtype=np.float32)

    def sendData(self):
        glUniformMatrix4fv(1, 1, GL_FALSE, self.model)
        glUniformMatrix4fv(2, 1, GL_FALSE, self.view)
        glUniformMatrix4fv(3, 1, GL_FALSE, self.proj)


    def callbackMousePos(self, window, xpos, ypos):
        rad = 3.14159 / 180.0
        w, h = get_window_size(window)
        cw, ch = w / 2, h / 2
        co, si = (xpos-cw)/cw, (ypos-ch)/ch
        thy, thz = math.acos(co), math.asin(si)

        # q = quaternion(1, thy, thz, 0)
        # qv = as_rotation_vector(q)
        q = from_spherical_coords([si, co])
        if self.lastx == None or self.lasty == None:
            self.lastx, self.lasty = xpos, ypos
            self.qstart = q
            return

        if self.d == 0:
            dx = (self.lastx - xpos)
        else:
            dx = 0
        if self.d == 1:
            dy = (self.lasty - ypos)
        else:
            dy = 0

        dx = (self.lastx - xpos)
        dy = (self.lasty - ypos)


        # print("({:+.2f})({:+.2f}) ({:+.2f})({:+.2f})".format(co, si, math.acos(co), math.asin(si)))

        startv = as_rotation_vector(self.qstart)

        t = from_spherical_coords([si, co])

        # print(np.cross(as_spinor_array(q), as_spinor_array(self.qstart)))


        # print("x: {:.1f},  y: {:.1f}, z {:.1f}; ".format(*dott))

        rot3 = as_rotation_matrix(t)
        B = np.mat('0;0;0')
        C = np.mat('0 0 0')
        D = np.mat('1')
        rot4 = np.bmat([[rot3, B], [C, D]])
        self.model = rot4
        print(self.model)

        self.sendData()

    def callbackMouseButton(self, window, button, action, mods):
        if action == PRESS:
            if button == 0:
                self.d = 0
            elif button == 1:
                self.d = 1
            else:
                return

            set_cursor_pos_callback(window, self.callbackMousePos)

        if action == RELEASE and (button == 0 or button == 1):
            self.lastx, self.lasty, self.dx, self.dy = None, None, None, None
            set_cursor_pos_callback(window, lambda *_: None)


    def callbackScroll(self, window, xoffset, yoffset):
        d = 2.0
        zoom = self.zoom - d * yoffset
        if zoom < 180.0 - d and zoom > d:
            self.zoom = zoom

        self.updateProj()
        self.sendData()
