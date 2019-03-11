import math
import pyquaternion



class Trackball:

    def __init__(self, x, y, radius, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.setFrom(x, y)

    def setFrom(self, x, y):
        self.from_pos = self.mouseToSphere(x, y)

    def setTo(self,x ,y):
        self.to_pos = self.mouseToSphere(x, y)

    def getRotation(self):
        fr = self.from_pos
        to = self.to_pos
        r = (fr[0] * to[0]) + (fr[1] * to[1]) + (fr[2] * to[2])

        i = (fr[1] * to[2]) - (to[1] * fr[2])
        j = (fr[2] * to[0]) - (to[2] * fr[0])
        k = (fr[0] * to[1]) - (to[0] * fr[1])

        rotation = pyquaternion.Quaternion(r, i, j, k)

        print("                          {}, {}, {}".format(rotation, tuple(map(lambda x: round(x, 2), fr)), tuple(map(lambda x: round(x, 2), to))))
        print(rotation.transformation_matrix)

        return rotation

    def mouseToSphere(self, x, y):
        sphere_x = (x - self.center_x) / self.radius
        sphere_y = -(y - self.center_y) / self.radius

        magnitude = sphere_x ** 2 + sphere_y ** 2

        if magnitude > 1.0:
            scale = 1.0 / math.sqrt(magnitude)
            sphere_x = sphere_x * scale
            sphere_y = sphere_y * scale
            sphere_z = 0.0
        else:
            sphere_z = -math.sqrt(1 - magnitude)

        sphere_w = 0.0


        return (sphere_x, sphere_y, sphere_z, sphere_w)
