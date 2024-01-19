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
    def ancestor(self, dist: int) -> Self:
        env = self
        for _ in range(dist):
            # TODO: review this, I did it to shut the linter up
            env = env.enclosing if env.enclosing is not None else env

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



# Utils for debugging environments 
def env_chain(env: Environment) -> str:
    """
    Print the current environment and its closures/ancestors.
    """

    dist = 0;
    cur_env = env
    s = ""

    while cur_env is not None:
        s += f"Env({dist}) :\n\t"
        s +=",\n\t".join(f"{key} : {val}" for key, val in cur_env.values.items())
        s += "\n"

        if cur_env.enclosing is not None:
            cur_env = cur_env.enclosing
        else:
            break

        dist = dist + 1

    return s


