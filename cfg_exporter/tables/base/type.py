class LangType:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return self._value

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._value == other.text

    @property
    def text(self):
        return self._value


class RawType:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return self._value

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._value == other.text

    @property
    def text(self):
        return self._value


class IgnoreValue:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return self._value

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._value == other.text

    @property
    def text(self):
        return self._value


class ReferenceValue:
    def __init__(self, ref_value, value):
        self._ref_value = ref_value
        self._value = value

    def __str__(self):
        return self._ref_value

    def __repr__(self):
        return self._ref_value

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._value == other.text

    @property
    def text(self):
        return self._ref_value

    @property
    def raw_value(self):
        return self._value


__all__ = ('RawType', 'LangType', 'IgnoreValue', 'ReferenceValue')
