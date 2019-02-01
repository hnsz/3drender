from pyrr import matrix44, vector3, Quaternion
import numpy as np
import glfw
from OpenGL.GL import *


class MoViPro:
    zoom = 60
    dscroll = 1
    trans = None
    view = None
    proj = None
    lastx = None
    lasty = None



    def __init__(self):
        self.last_rot_quat = Quaternion.from_x_rotation(0.1)
        self.trans = matrix44.create_from_translation(vector3.create(2.0, 0.0, 0.0, dtype=np.float32))
        self.model = matrix44.create_identity()
        self.eye = vector3.create(0.0, 2.0, 6.0, dtype=np.float32)
        self.target = vector3.create(0.0, 0.0, 0.0, dtype=np.float32)
        self.up = vector3.create(0.0, 1.0, 0.0, dtype=np.float32)
        self.updateView()
        self.updateProj()


    def updateView(s):
        s.view = matrix44.create_look_at(s.eye, s.target, s.up)

    def updateProj(self):
        self.proj = matrix44.create_perspective_projection(self.zoom, 1080.0 / 720.0, 0.1, 80.0, dtype=np.float32)

    def sendData(self):
        glUniformMatrix4fv(1, 1, GL_FALSE, self.model)
        glUniformMatrix4fv(2, 1, GL_FALSE, self.view)
        glUniformMatrix4fv(3, 1, GL_FALSE, self.proj)


    def callbackMousePos(self, window, xpos, ypos):
        rad = 3.14159 / 180.0


        if self.lastx == None or self.lasty == None:
            self.lastx, self.lasty = xpos, ypos
            self.model_quat = self.last_rot_quat
            return

        dx = (self.lastx - xpos)
        dy = (self.lasty - ypos)

        # print("({0},{1} dx: {2}, dy: {3})".format(xpos,ypos,dx,dy))

        qy = Quaternion.from_eulers(vector3.create(dy * rad, dx * rad, 0, dtype=np.float32))

        res_quat = qy * self.model_quat
        self.last_rot_quat = res_quat.normalised

        self.model = matrix44.create_from_quaternion(self.last_rot_quat)

        self.sendData()

    def callbackMouseButton(self, window, button, action, mods):
        if button == 0 and action == glfw.PRESS:
            glfw.set_cursor_pos_callback(window, self.callbackMousePos)

        if button == 0 and action == glfw.RELEASE:
            self.lastx, self.lasty, self.dx, self.dy = None, None, None, None
            glfw.set_cursor_pos_callback(window, lambda *_: None)

    def callbackScroll(self, window, xoffset, yoffset):
        d = 2.0
        zoom = self.zoom + d * yoffset
        if zoom < 180.0 - d and zoom > d:
            self.zoom = zoom

        self.updateProj()
        self.sendData()
