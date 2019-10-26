class Color(object):

    @staticmethod
    def handle(color):
        base = (0, 0, 0, 255)
        _len = len(color)
        if type(color) == tuple:
            if _len != 4 and _len != 3:
                raise FormatError('(R, G, B, A) has wrong amount of elements')
                return base
        elif type(color) == str:
            if _len != 7 and _len != 9:
                raise FormatError('#RRGGBBAA has wrong amount of elements')
                return base
        else:
            raise FormatError('Unrecognized color format')
            return base

        base = [0, 0, 0, 255]
        if type(color) == tuple:
            for index in range(_len):
                base[index] = color[index]
        else:
            color = color[1:]
            _len = len(color) // 2
            for index in range(_len):
                try:
                    base[index] = int(color[index * 2: (index + 1) * 2], 16)
                except ValueError as e:
                    raise FormatError('Unrecognized hex format')

        return tuple(base)


class FormatError(Exception):
    def __init__(self, msg):
        super(FormatError, self).__init__()
        self._msg = msg
