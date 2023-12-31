from typing import Any, Dict

from loxpy.token import Token
from loxpy.error import LoxRuntimeError


class Environment:
    def __init__(self):
        self.values: Dict[str, Any] = {}

    def __len__(self) -> int:
        return len(self.values)

    def define(self, name: str, value: Any) -> None:
        self.values[name] = value

    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        raise LoxRuntimeError(name, f"Undefined variable {name.lexeme}")

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        raise LoxRuntimeError(name, f"Undefined variable {name.lexeme}")

