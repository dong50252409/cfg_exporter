class RawType:
    def __init__(self, value):
        self._value = str(value)

    def __str__(self):
        return self._value
