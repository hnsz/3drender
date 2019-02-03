import math
from datetime import datetime
import os
from OpenGL.GL import *
from PIL import Image


class PixelBufferOut:
    fileExt = 'tiff'
    destDir = './assets'
    images = []
    count = 0
    pbo = None

    def __init__(s):
        if not os.path.exists(s.destDir):
            raise RuntimeError("Directory doesnt exist")

        s.outDir = datetime.now().strftime("%H%M%S")

        os.mkdir("{0}/{1}".format(s.destDir, s.outDir))




    def create(s):
        x, y, width, height = glGetIntegerv(GL_VIEWPORT)


        glReadBuffer(GL_FRONT)
        glPixelStorei(GL_PACK_ALIGNMENT, 1)

        data = glReadPixels(x, y, width, height, GL_RGB, GL_UNSIGNED_BYTE)

        image = Image.frombytes("RGB", (width, height), data)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        path = "{0}/{1}/img{2}.{3}".format(s.destDir, s.outDir, s.count, s.fileExt)
        s.images.append((image, path))
        s.count += 1

    def save(s):
        for image, name in s.images:
            image.save(os.path.join(name), format=s.fileExt)


    def toVideo(s):
        return