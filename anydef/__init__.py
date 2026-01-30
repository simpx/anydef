"""AnyDef: A Python library to auto-generate function implementations using AI."""

from .core import anydef, anydef_async
from .version import __version__

__all__ = ["anydef", "anydef_async", "__version__"]