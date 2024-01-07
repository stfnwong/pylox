from typing import Any, Dict, Optional, Self

from loxpy.token import Token
from loxpy.error import LoxRuntimeError


class Environment:
    def __init__(self, enclosing: Optional[Self]=None):
        self.enclosing: Optional[Self] = enclosing
        self.values: Dict[str, Any] = {}

    def __len__(self) -> int:
        return len(self.values)

    def __str__(self) -> str:
        num_anc = 0
        anc = self.enclosing
        while anc is not None:
            num_anc += 1
            anc = anc.enclosing

        vals = "  \n".join(f"[{name}: {value}]" for name, value in self.values.items())
        return f"Environment({vals}) ({num_anc} ancestor(s))"

    # TODO: is there a better type hint trick than just using quotes?
    def ancestor(self, dist: int) -> "Environment":
        env = self
        for _ in range(dist):
            # TODO: review this, I did it to shut the linter up
            env = env.enclosing 

        return env

    def define(self, name: str, value: Any) -> None:
        self.values[name] = value

    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise LoxRuntimeError(name, f"Undefined variable {name.lexeme}")

    def assign_at(self, dist: int, name: Token, value: Any) -> None:
        env = self.ancestor(dist)
        env.values[name.lexeme] = value

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise LoxRuntimeError(name, f"Undefined variable {name.lexeme}")

    def get_at(self, dist: int, name: Token) -> Any:
        return self.ancestor(dist).get(name)

