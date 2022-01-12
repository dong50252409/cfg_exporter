from typing import *
from cfg_exporter.tables.base.raw import RawType

StrOrNone = TypeVar('StrOrNone', str, None)
AnyType = TypeVar('DataType', int, float, str, list, tuple, RawType)
Iter = TypeVar('Iter', Iterator[AnyType], Iterator[tuple])

__version__ = "0.1.0"
