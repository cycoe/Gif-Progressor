from PIL import Image, ImageSequence
import imageio
from GifProgressor import Progressor, Position

progressor = Progressor().setPosition(Position.bottom).setColor((255, 0, 0, 100))
progressor.handle('test.gif')
if progressor:
    progressor.save('output.gif')
