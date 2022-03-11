class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        key = (cls, args.__str__(), kwargs.__str__())
        if key not in cls._instances:
            cls._instances[key] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[key]


class LangType(metaclass=Singleton):
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return self._value

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._value == other.text

    @property
    def text(self):
        return self._value


class RawType(metaclass=Singleton):
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return self._value

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._value == other.text

    @property
    def text(self):
        return self._value


class DefaultValue(metaclass=Singleton):
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return self._value

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._value == other.text

    @property
    def text(self):
        return self._value


__all__ = ('RawType', 'LangType', 'DefaultValue')
