import numpy as np
from PIL import Image, ImageSequence

from .Color import Color

#   0 1 2
#  6+---+9
#  7|   |10
#  8+---+11
#   3 4 5
class Position(object):
    topLeft = 0
    top = 1
    topRight = 2
    bottomLeft = 3
    bottom = 4
    bottomRight = 5
    leftTop = 6
    left = 7
    leftBottom = 8
    rightTop = 9
    right = 10
    rightBottom = 11


class Progressor(object):

    def __init__(self, pos=Position.bottom, color=(0, 0, 0, 255), width=None):
        self.setPosition(pos)
        self.setColor(color)
        self.setWidth(width)
        self.setMinWidth(2)
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
        self._width = width
        return self

    def setMinWidth(self, minWidth):
        self._minWidth = minWidth
        return self

    def _getGeo(self, frame, percent):
        """Get the geometry of the bar on the specific frame
        :frame: <Image>
        :percent: <float> progress percent

        :returns: tuple<int>[4] geometry of bar
        """
        size = frame.size
        geo = [0, 0, 0, 0]

        group = self._pos // 6
        if (self._width is None):
            self._width = size[1 - group] // 20
        if (self._width < self._minWidth):
            self._width = self._minWidth
        if (self._width > size[1 - group]):
            self._width = size[1 - group]

        geo[2 + group] = int(size[group] * percent)
        geo[3 - group] = self._width
        geo[1 - group] = 0 if self._pos < 3 + 6 * group else size[1 - group] - self._width
        if self._pos % 3 == 0:
            geo[group] = 0
        elif self._pos % 3 == 1:
            geo[group] = (size[group] - geo[group + 2]) // 2
        else:
            geo[group] = (size[group] - geo[group + 2])

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
