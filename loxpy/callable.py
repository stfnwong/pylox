from typing import Any, Dict, Optional, Sequence
from abc import ABC, abstractmethod

#from loxpy.interpreter import Interpreter   # TODO: protocol?
from loxpy.environment import Environment
from loxpy.statement import FuncStmt
from loxpy.token import Token
from loxpy.error import LoxRuntimeError


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
        # NOTE: can't use type hint here for interp due to circular import, 
        # maybe use a protocol here?
       raise NotImplementedError



class LoxInstance:
    def __init__(self, lox_class: "LoxClass"):
        self.lox_class = lox_class
        self.fields: Dict[str, Any] = {}

    def __str__(self) -> str:
        return f"LoxInstance({self.lox_class.name})"

    def get(self, name: Token) -> Any:
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method = self.lox_class.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)

        raise LoxRuntimeError(name, f"Undefined property '{name.lexeme}' on class '{self.lox_class.name}'")

    def set(self, name: Token, value: Any) -> None:
        self.fields[name.lexeme] = value


class LoxFunction(LoxCallable):
    def __init__(self, decl: FuncStmt, closure: Environment):
        self.decl = decl
        self.closure = closure

    def __str__(self) -> str:
        return f"<fn {self.decl.name.lexeme}>"

    def arity(self) -> int:
        return len(self.decl.params)

    def call(self, interp, args: Sequence[Any]) -> Any:
        env = Environment(self.closure)

        for param, arg in zip(self.decl.params, args):
            env.define(param.lexeme, arg)
        try:
            interp.execute_block(self.decl.body, env)
        except LoxReturnException as rt:
            return rt.value

        return None

    def bind(self, instance: LoxInstance) -> "LoxFunction":
        env = Environment(self.closure)
        env.define("this", instance)

        return LoxFunction(self.decl, env)


class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: Dict[str, LoxFunction]):
        self.name = name
        self.methods = methods

    def __str__(self) -> str:
        return f"LoxClass({self.name})"

    def arity(self) -> int:
        return 0;

    def call(self, interp, args: Sequence[Any]) -> Any:
        instance = LoxInstance(self)
        return instance

    def find_method(self, name: str) -> Optional[LoxFunction]:
        if name in self.methods:
            return self.methods[name]

        return None

