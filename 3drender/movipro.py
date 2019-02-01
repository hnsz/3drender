from pyrr import matrix44, vector3, Quaternion, quaternion, vector4, Vector3, quaternion, Vector4
import numpy as np
import glfw
from OpenGL.GL import *
from pyrr.quaternion import rotation_axis


class MoViPro:
    zoom = 60
    dscroll = 1
    trans = None
    view = None
    proj = None
    lastx = None
    lasty = None



    def __init__(self):
        self.last_rot_quat = Quaternion.from_x_rotation(0)
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

        qy = Quaternion.from_eulers(vector3.create(dy * rad, dx * rad, 0, dtype=np.float32))





        res_quat = qy * self.model_quat
        self.last_rot_quat = res_quat.normalised



        v = np.array([1, 0, 0, 1])
        c = np.array([.7, .7, .7, 1.0])
        cross = vector4.create(*self.last_rot_quat.cross(v))
        # cross = np.array(vector4.normalize(cross) )



        print(cross)


        # print("x: {:.1f},  y: {:.1f}, z {:.1f}; ".format(*dott))

        # glBufferSubData(GL_ARRAY_BUFFER, 4672 +(4)*16 , 16, np.array(-1 * cross, dtype=np.float32))
        glBufferSubData(GL_ARRAY_BUFFER, 4672 +(6)*16 , 16, np.array(cross, dtype=np.float32))
        self.model = matrix44.create_from_quaternion(self.last_rot_quat)

        self.sendData()

    def callbackMouseButton(self, window, button, action, mods):
        if action == glfw.PRESS:
            if button == 0:
                self.d = 0
            elif button == 1:
                self.d = 1
            else:
                return

            glfw.set_cursor_pos_callback(window, self.callbackMousePos)

        if action == glfw.RELEASE and (button == 0 or button == 1):
            self.lastx, self.lasty, self.dx, self.dy = None, None, None, None
            glfw.set_cursor_pos_callback(window, lambda *_: None)


    def callbackScroll(self, window, xoffset, yoffset):
        d = 2.0
        zoom = self.zoom - d * yoffset
        if zoom < 180.0 - d and zoom > d:
            self.zoom = zoom

        self.updateProj()
        self.sendData()
