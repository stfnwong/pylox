# Built-in functions.

from typing import Any, Sequence
import time
from loxpy.callable import LoxCallable


class BuiltinFunction(LoxCallable):
    shortname: str

    def __str__(self) -> str:
        return f"<builtin {self.shortname}"


class Clock(BuiltinFunction):
    shortname = "clock"

    def arity(self) -> int:
        return 0

    # pylint: disable=unused-argument
    def call(self, interp, args: Sequence[Any]) -> float:
        return time.time()


BUILTIN_MAP = {
    "clock": Clock()
}
