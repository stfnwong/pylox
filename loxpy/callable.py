from typing import Any, Dict, Optional, Sequence
from abc import ABC, abstractmethod

#from loxpy.interpreter import Interpreter   # TODO: protocol?
from loxpy.environment import Environment
from loxpy.statement import FuncStmt
from loxpy.token import Token, Str2Token
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
    """
    LoxInstance

    Runtime representation of a LoxClass. 
        
    """

    def __init__(self, lox_class: "LoxClass"):
        self.lox_class = lox_class
        self.fields: Dict[str, Any] = {}

    def __str__(self) -> str:
        fields = ",".join(f"{fname}" for fname in self.fields.keys())
        return f"LoxInstance({self.lox_class.name}) [{fields}]"

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
    def __init__(self, decl: FuncStmt, closure: Environment, is_init: bool):
        self.decl = decl
        self.closure = closure
        self.is_initializer = is_init

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
            if self.is_initializer:
                return self.closure.get_at(0, Str2Token("this"))

            return rt.value

        if self.is_initializer:
            return self.closure.get_at(0, Str2Token("this"))

        return None

    def bind(self, instance: LoxInstance) -> "LoxFunction":
        env = Environment(self.closure)
        env.define("this", instance)

        return LoxFunction(self.decl, env, self.is_initializer)


class LoxClass(LoxCallable):
    def __init__(self, name: str, superclass: "LoxClass", methods: Dict[str, LoxFunction]):
        self.name = name
        self.superclass: "LoxClass" = superclass
        self.methods: Dict[str, LoxFunction] = methods

    def __str__(self) -> str:
        return f"LoxClass({self.name})"

    def arity(self) -> int:
        initializer = self.find_method("init")
        if initializer is not None:
            return initializer.arity()

        return 0;

    def call(self, interp, args: Sequence[Any]) -> Any:
        instance = LoxInstance(self)

        # When we call check for an init function. If we have one then 
        # bind and call it, forwarding the argument list..
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interp, args)

        return instance

    def find_method(self, name: str) -> Optional[LoxFunction]:
        if name in self.methods:
            return self.methods[name]

        if self.superclass is not None:
            return self.superclass.find_method(name)

        return None

