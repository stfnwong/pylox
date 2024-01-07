# Interactive prompt for loxpy
# TODO: command history

from sys import argv, version_info

from loxpy.error import LoxRuntimeError, LoxParseError
from loxpy.token import Token, TokenType
# components 
from loxpy.interpreter import Interpreter
from loxpy.scanner import Scanner
from loxpy.parser import Parser
from loxpy.resolver import Resolver


USAGE = "Usage: lox [file]" 
LOX_VERSION = "0.1.0"


class Lox:
    had_error = False       # had_parse_error?
    had_runtime_error = False
    interp = Interpreter()

    def _repl_header(self) -> str:
        py_version = ".".join(str(i) for i in version_info[:3])
        lox_version = f"{LOX_VERSION}"
        s = f"Lox repl [Python {py_version}, Lox {lox_version}]\nType 'exit' or Ctrl-D to quit\n"
        return s

    def report(self, line: int, where: str, message: str) -> None:
        print(f"[line {line}]: Error {where}, {message}")

    def error(self, token: Token, message: str) -> None:
        if token.token_type == TokenType.LOX_EOF:
            self.report(token.line, " at end ", message)
        else:
            self.report(token.line, f" at [{token.lexeme}]", message)

    def run(self, source: str) -> None:
        try:
            scanner = Scanner(source)
            tokens = scanner.scan()
            parser = Parser(tokens)
            stmts = parser.parse()

            # Only resolve if we parsed correctly
            if self.had_error or not stmts:
                exit(-1)

            resolver = Resolver(self.interp)
            resolver.resolve(stmts)

            self.interp.interpret(stmts)

        except LoxParseError as parse_error:
            self.error(parse_error.token, str(parse_error))
        except LoxRuntimeError as runtime_error:
            print(f"{runtime_error}: [line {runtime_error.token.line}]")
            self.had_runtime_error = True

    def run_file(self, filename: str) -> None:
        with open(filename, "r") as fp:
            source = fp.read()

        self.run(source)

        if self.had_error:
            exit(-1)
        elif self.had_runtime_error:
            exit(-2)

    def prompt(self) -> None:
        print(self._repl_header())

        while True:
            try:
                print(">> ", end=" ")

                expr = input()
                if expr.split(" ")[0] == "exit":
                    exit(0)

                self.run(expr)
                self.had_error = False
                self.had_runtime_error = False

            except KeyboardInterrupt as k:
                print(f"\n{k.__class__.__name__}")
            except EOFError:
                exit(0)


def main(args):

    lox = Lox()
    if len(args) == 1:
        lox.run_file(args[0])
    else:
        lox.prompt()


if __name__ == "__main__":
    main(argv[1:])
