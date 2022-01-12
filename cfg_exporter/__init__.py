from typing import *

StrOrNone = TypeVar('StrOrNone', str, None)
from cfg_exporter.tables.base.raw import RawType

AnyType = TypeVar('DataType', int, float, str, list, tuple, RawType)
Iter = TypeVar('Iter', Iterator[AnyType], Iterator[tuple])

__version__ = "0.1.0"
