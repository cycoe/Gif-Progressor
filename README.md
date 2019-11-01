## GifProgressor
GifProgressor is a tool to add a progress bar to gif images, which can prompt the progress.

## Usages
Import and instant a progressor object like this
```python
from GifProgressor import Progressor, Position
progressor = Progressor()
```

Set position of progress bar
```python
progressor.setPosition(Position.topLeft)
```

Set color
```python
progressor.setColor('#FF0000FF')
```

Or with tuple
```python
progressor.setColor((255, 0, 0, 255))
```

Set width of progress bar
```python
progressor.setWidth(10)
```

Handle with a gif image
```python
result = progressor.handle('test.gif')
```

Save the new gif
```python
if result:
    progressor.save('output.gif')
```

## Requirements
- PIL for gif image handling
- numpy for progress bar generation
