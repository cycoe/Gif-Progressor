from PIL import Image, ImageSequence
import imageio
from GifProgressor import Progressor, Postion

progressor = Progressor().setPosition(Postion.bottom).setColor((255, 0, 0, 100))
progressor.handle('test.gif')
if progressor:
    progressor.save('output.gif')
