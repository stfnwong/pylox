from typing import Any, Sequence
from abc import ABC, abstractmethod

#from loxpy import interpreter as i
#from loxpy.interpreter import Interpreter
from loxpy.environment import Environment
from loxpy.statement import FuncStmt


class LoxReturnException(Exception):
    def __init__(self, value: Any) -> None:
        super(LoxReturnException, self).__init__()
        self.value = value


class LoxCallable(ABC):
    @abstractmethod
    def arity(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def call(self, interp, args: Sequence[Any]) -> Any:
        # NOTE: can't use type hint here due to circular import, maybe use a protocol here?
       raise NotImplementedError


class LoxFunction(LoxCallable):

    def __init__(self, decl: FuncStmt):
        self.decl = decl

    def __str__(self) -> str:
        return f"<fn {self.decl.name.lexeme}>"

    def arity(self) -> int:
        return len(self.decl.params)

    def call(self, interp, args: Sequence[Any]) -> Any:
        env = Environment()

        for param, arg in zip(self.decl.params, args):
            env.define(param.lexeme, arg)
        try:
            interp.execute_block(self.decl.body, env)
        except LoxReturnException as rt:
            return rt.value

        return None
