import numpy as np
from PIL import Image, ImageSequence

from .Color import Color

#   1 2 3
#  7+---+10
#  8|   |11
#  9+---+12
#   4 5 6
class Position(object):
    topLeft = 1
    top = 2
    topRight = 3
    bottomLeft = 4
    bottom = 5
    bottomRight = 6
    leftTop = 7
    left = 8
    leftBottom = 9
    rightTop = 10
    right = 11
    rightBottom = 12


class Progressor(object):

    def __init__(self, pos=Position.bottom, color=(0, 0, 0, 255), width=2):
        self.setPosition(pos)
        self.setColor(color)
        self.setWidth(width)
        self._frames = None

    def setPosition(self, pos):
        """Set position of progress bar
        :pos: <int>"""
        self._pos = pos
        return self

    def setColor(self, color):
        """Set color with type (R, G, B, A)
        :color: tuple<uint8>[4]
        """
        self._color = Color.handle(color)
        return self

    def setWidth(self, width):
        self._width = width if width >= 1 else 1
        return self

    def _getGeo(self, frame, percent):
        """Get the geometry of the bar on the specific frame
        :frame: <Image>
        :percent: <float> progress percent

        :returns: tuple<int>[4] geometry of bar
        """
        size = frame.size
        geo = [0, 0, 0, 0]

        if (self._pos < 7):
            geo[2] = int(size[0] * percent)
            geo[3] = self._width if self._width < size[1] else size[1]
            geo[1] = 0 if self._pos < 4 else size[1] - geo[3]
            if self._pos % 3 == 1:
                geo[0] = 0
            elif self._pos % 3 == 2:
                geo[0] = (size[0] - geo[2]) // 2
            else:
                geo[0] = size[0] - geo[2]
        else:
            geo[3] = int(size[1] * percent)
            geo[2] = self._width if self._width < size[0] else size[0]
            geo[0] = 0 if self._pos < 10 else size[0] - geo[2]
            if self._pos % 3 == 1:
                geo[1] = 0
            elif self._pos % 3 == 2:
                geo[1] = (size[1] - geo[3]) // 2
            else:
                geo[1] = size[1] - geo[3]

        return tuple(geo)

    def _handleFrame(self, frame, percent):
        """Add bar to a frame
        :frame: <Image> A frame of gif
        :percent: <float> process percent
        """
        geo = self._getGeo(frame, percent)
        bar = np.ones((geo[3], geo[2], 4))
        for i in range(4):
            bar[:, :, i] *= self._color[i]
        frame.paste(
            Image.fromarray(bar.astype(np.uint8)),
            geo[:2],
            mask=Image.fromarray(bar[:, :, -1].astype(np.uint8))
        )

        return frame

    def handle(self, path):
        """Handle image with path
        :path: <str>
        """
        try:
            img = Image.open(path)
        except IOError as e:
            print(e)
            return False

        frames = [frame.convert('RGBA')
                  for frame in ImageSequence.Iterator(img)]
        for index in range(len(frames)):
            frames[index] = self._handleFrame(
                frames[index], (index + 1) / len(frames))

        self._frames = frames
        return True

    def save(self, path):
        if self._frames is None:
            print("No frames!")
            return self

        self._frames[0].save(path, save_all=True, append_images=self._frames)
        return self
