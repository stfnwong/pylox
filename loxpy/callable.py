from typing import Any, Sequence
from abc import ABC, abstractmethod

#from loxpy import interpreter as i
#from loxpy.interpreter import Interpreter 


class LoxCallable(ABC):
    @abstractmethod
    def arity(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def call(self, interp, args: Sequence[Any]) -> Any:
        # NOTE: can't use type hint here due to circular import
       raise NotImplementedError 
