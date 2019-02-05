from datetime import datetime
import os
from OpenGL.GL import *
from PIL import Image


class FrameGrab:
    fileExt = 'tiff'
    destDir = 'assets'
    count = 0
    pbo = None
    bufferSize = 0
    idx = 0
    nextIdx = 0
    fileWriter = None

    def __init__(s):
        _, _, s.width, s.height = glGetIntegerv(GL_VIEWPORT)
        s.pixelformat = {'gl': GL_RGBA, 'image': 'RGBA', 'size': 4}
        s.bufferSize = s.width * s.height * s.pixelformat['size']
        s.fileWriter = FileWriter(s.destDir)


    def create(s):
        s.idx = (s.idx + 1) % 2
        s.nextIdx = (s.idx + 1) % 2

        glBindBuffer(GL_PIXEL_PACK_BUFFER, s.pbo[s.idx])

        #asynch
        try:
            glReadPixels(0, 0, s.width, s.height, s.pixelformat['gl'], GL_UNSIGNED_BYTE, 0)
        except error.GLError as err:
            print(err)
            os.sys.exit()
        except:
            print("Non gl error")

        glBindBuffer(GL_PIXEL_PACK_BUFFER, s.pbo[s.nextIdx])
        bufferdata = glMapBuffer(GL_PIXEL_PACK_BUFFER, GL_READ_ONLY)

        image = Image.frombuffer(s.pixelformat["image"], (s.width, s.height), ctypes.string_at(bufferdata, s.bufferSize), 'raw',s.pixelformat["image"], 0, 1)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

        glUnmapBuffer(GL_PIXEL_PACK_BUFFER)
        glBindBuffer(GL_PIXEL_PACK_BUFFER, 0)

        return image

    def toVideo(s):
        return

    def setupBuffers(s, pbo):
        glBindBuffer(GL_PIXEL_PACK_BUFFER, pbo[0])
        glBufferData(GL_PIXEL_PACK_BUFFER, s.bufferSize , None, GL_STREAM_READ)
        glBindBuffer(GL_PIXEL_PACK_BUFFER, pbo[1])
        glBufferData(GL_PIXEL_PACK_BUFFER, s.bufferSize , None, GL_STREAM_READ)
        glBindBuffer(GL_PIXEL_PACK_BUFFER, 0)

        s.pbo = pbo

    def save(s, img: Image):
        s.fileWriter.writeImage(img)


class FileWriter:
    name = 'img{:04d}.{:s}'
    ext = 'tiff'
    count = 0

    def __init__(s, basedir):
        if not os.path.exists(basedir):
            raise RuntimeError("Directory doesnt exist: ({0})".format(basedir))

        s.basedir = basedir
        s.dt = datetime.now()
        s.nr = 0
        s.dest = s.createDestDir()

    def createDestDir(s):
        capture = os.path.join(s.basedir, "capture{:%m%d}".format(s.dt))
        series = os.path.join(capture, "series".format(s.dt))

        if not os.path.exists(capture):
            os.mkdir(capture)

        for i in range(0,1000):
            destDir = "{:s}{:03d}".format(series, i)
            if not os.path.exists(destDir):
                os.mkdir(destDir)
                return destDir

        raise RuntimeError("Too many directories. Come on...")

    def writeImage(s, img: Image):
        s.count += 1
        img.save(os.path.join(s.dest, s.name.format(s.count, s.ext)), format=s.ext)
