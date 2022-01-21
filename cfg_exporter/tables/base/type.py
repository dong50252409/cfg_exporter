class RawType:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return self._value

    @property
    def text(self):
        return self._value


class LangType:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return self._value

    @property
    def text(self):
        return self._value


__all__ = ('RawType', 'LangType')
