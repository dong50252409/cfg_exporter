import cfg_exporter.util as util


class RawType:
    def __init__(self, value):
        self._value = util.escape(str(value))

    def __str__(self):
        return self._value
