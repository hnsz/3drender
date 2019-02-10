import math
import time
from queue import Queue
from threading import *

from datetime import datetime
import os
from OpenGL.GL import *
from PIL import Image


class FrameGrabber:
    fileExt = 'tiff'
    destDir = 'assets'
    count = 0
    pbo = None
    bufferSize = 0
    idx = 0
    nextIdx = 0
    fileWriter = None

    def __init__(s):
        s.width = 1280
        s.height = 960

        s.pixelformat = {'gl': GL_RGB, 'image': 'RGB', 'size': 3}
        s.bufferSize = s.width * s.height * s.pixelformat['size']
        s.fileWriter = FileWriter(s.destDir)


    def saveFrame(s):
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

        image = Image.frombuffer(s.pixelformat["image"], (s.width, s.height), ctypes.string_at(bufferdata, s.bufferSize), 'raw', s.pixelformat['image'], 0, 1)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

        glUnmapBuffer(GL_PIXEL_PACK_BUFFER)
        glBindBuffer(GL_PIXEL_PACK_BUFFER, 0)

        s.fileWriter.writeImage(image)


    def toVideo(s):
        return

    def setPBO(s, pbo):
        s.pbo = pbo

    def setupBuffers(s):
        glBindBuffer(GL_PIXEL_PACK_BUFFER, s.pbo[0])
        glBufferData(GL_PIXEL_PACK_BUFFER, s.bufferSize , None, GL_STREAM_READ)
        glBindBuffer(GL_PIXEL_PACK_BUFFER, s.pbo[1])
        glBufferData(GL_PIXEL_PACK_BUFFER, s.bufferSize , None, GL_STREAM_READ)
        glBindBuffer(GL_PIXEL_PACK_BUFFER, 0)

    def finish(s):
        s.fileWriter.finish()


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
        s.q = Queue()
        s.c = Condition()
        s.e = Event()
        s.consumer = Consumer(s.q, s.c, s.e)
        s.consumer.start()

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
        filename = os.path.join(s.dest, s.name.format(s.count, s.ext))
        s.q.put_nowait((img, filename, s.ext))
        s.c.acquire()
        s.c.notify()
        s.c.release()

    def finish(s):
        s.e.set()
        s.q.join()
        s.q.put_nowait((None, None, None))
        s.c.acquire()
        s.c.notify()
        s.c.release()
        s.consumer.join()



class Consumer(Thread):

    def __init__(s, q, c, e):
        s.q = q
        s.c = c
        super(Consumer, s).__init__()
        s.finish = e
        s.finish.clear()


    def run(s):
        while True:
            if s.finish.isSet():
                pass
            elif s.q.qsize() > 0:
                sleeptime = .5 / math.exp(s.q.qsize()/50)
                time.sleep(sleeptime)

            if not s.q.empty():
                img, filename, ext = s.q.get()
                if not img:
                    break
                else:
                    img.save(filename, format=ext)
                    s.q.task_done()
            else:
                s.c.acquire()
                s.c.wait()
                s.c.release()

