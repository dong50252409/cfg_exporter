import gettext
import locale
import typing
from cfg_exporter.tables.base.type import LangType, RawType, DefaultValue

_lang, _localename = locale.getdefaultlocale()
gettext.translation('resource', './locale', languages=[_lang], fallback=True).install()
StrOrNone = typing.Union[str, type(None)]
AnyType = typing.Union[int, float, str, typing.List, typing.Tuple, LangType, RawType, DefaultValue]
Iter = typing.Union[typing.Iterator[AnyType], typing.Iterator[typing.Tuple]]
__version__ = "0.1.0"

__all__ = ('StrOrNone', 'AnyType', 'Iter')
