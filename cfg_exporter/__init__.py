import gettext
import locale
from typing import *
from cfg_exporter.tables.base.type import RawType

lang, _localename = locale.getdefaultlocale()
gettext.translation('resource', './locale', languages=[lang], fallback=True).install()

StrOrNone = TypeVar('StrOrNone', str, None)
AnyType = TypeVar('DataType', int, float, str, list, tuple, RawType)
Iter = TypeVar('Iter', Iterator[AnyType], Iterator[tuple])

__version__ = "0.1.0"
