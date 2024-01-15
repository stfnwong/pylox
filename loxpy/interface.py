from typing import Any, Protocol, Sequence

from loxpy.environment import Environment
from loxpy.statement import Stmt


class Interprets(Protocol):
    def execute(self, stmt: Stmt) -> Any:
        ...

    def execute_block(self, stmts: Sequence[Stmt], env: Environment) -> Any:
        ...
