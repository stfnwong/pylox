from typing import Sequence
from loxpy.resolver import Resolver
from loxpy.interpreter import Interpreter
from loxpy.scanner import Scanner
from loxpy.parser import Parser
from loxpy.statement import Stmt
from loxpy.util import load_source


VAR_PROGRAM = "programs/op.lox"
FOR_PROGRAM = "programs/for_interp.lox"
FIB_FUNC_PROGRAM = "programs/fib_func.lox"
FUNC_PROGRAM = "programs/func1.lox"



def get_resolver() -> Resolver:
    interp = Interpreter()
    res = Resolver(interp)

    return res


def parse_input(expr_src: str) -> Sequence[Stmt]:
    scanner       = Scanner(expr_src)
    token_list    = scanner.scan()
    parser        = Parser(token_list)
    parsed_output = parser.parse()

    return parsed_output



#def test_resolve_var() -> None:
#    # NOTE: distance of "local" vars should be zero
#    res = get_resolver()
#    parsed_output = parse_input(load_source(VAR_PROGRAM))
#
#    # TODO: what should the state be here? 
#    # If there are no scopes should there be anything in locals?
#    res.resolve(parsed_output)
#    exp_state = {}
#
#    print(res)


def test_resolve_for() -> None:
    res = get_resolver()
    parsed_output = parse_input(load_source(FOR_PROGRAM))

    res.resolve(parsed_output)

    print(parsed_output)


def test_resolve_func() -> None:
    res = get_resolver()
    parsed_output = parse_input(load_source(FUNC_PROGRAM))

    res.resolve(parsed_output)


def test_resolve_fib_func() -> None:
    res = get_resolver()
    parsed_output = parse_input(load_source(FIB_FUNC_PROGRAM))

    res.resolve(parsed_output)
