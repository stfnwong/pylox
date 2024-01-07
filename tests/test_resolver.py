from typing import Sequence
from loxpy.resolver import Resolver
from loxpy.interpreter import Interpreter
from loxpy.scanner import Scanner
from loxpy.parser import Parser
from loxpy.statement import Stmt
from loxpy.token import Token, TokenType
from loxpy.expr import AssignmentExpr, BinaryExpr, LiteralExpr, VarExpr
from loxpy.util import load_source


VAR_PROGRAM      = "programs/op.lox"
FOR_PROGRAM      = "programs/for_interp.lox"
FIB_FUNC_PROGRAM = "programs/fib_func.lox"
FUNC_PROGRAM     = "programs/func1.lox"



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

    # No scopes or functions, so we expect the interpreter to have no locals()
    assert res.interp.locals == {}


def test_resolve_func() -> None:
    res = get_resolver()
    parsed_output = parse_input(load_source(FUNC_PROGRAM))

    res.resolve(parsed_output)
    
    # We expect the variables "first" and "last" to end
    # up resolved in locals
    exp_locals = [
        VarExpr(name=Token(TokenType.IDENTIFIER, lexeme="first", literal="first", line=2, col=21)),
        VarExpr(name=Token(TokenType.IDENTIFIER, lexeme="last", literal="last", line=2, col=34)),
    ]

    assert len(res.interp.locals) == len(exp_locals)

    for local in exp_locals:
        assert local in res.interp.locals


def test_resolve_fib_func() -> None:
    res = get_resolver()
    parsed_output = parse_input(load_source(FIB_FUNC_PROGRAM))

    res.resolve(parsed_output)

    exp_locals = [
        (VarExpr(name=Token(TokenType.IDENTIFIER, lexeme="n", literal="n", line=2, col=6)),  0),
        (VarExpr(name=Token(TokenType.IDENTIFIER, lexeme="n", literal="n", line=2, col=20)), 0),
        (VarExpr(name=Token(TokenType.IDENTIFIER, lexeme="n", literal="n", line=4, col=14)), 0),
        (VarExpr(name=Token(TokenType.IDENTIFIER, lexeme="n", literal="n", line=4, col=27)), 0),
        (VarExpr(name=Token(TokenType.IDENTIFIER, lexeme="i", literal="i", line=7, col=17)), 0),
        (VarExpr(name=Token(TokenType.IDENTIFIER, lexeme="i", literal="i", line=8, col=13)), 2),
        (VarExpr(name=Token(TokenType.IDENTIFIER, lexeme="i", literal="i", line=7, col=29)), 1),
        (AssignmentExpr(
            name=Token(TokenType.IDENTIFIER, lexeme="i", literal="i", line=7, col=25),
            value=BinaryExpr(
                op=Token(TokenType.PLUS, lexeme="+", literal=None, line=7, col=31),
                left=VarExpr(name=Token(TokenType.IDENTIFIER, lexeme="i", literal="i", line=7, col=29)),
                right=LiteralExpr(value=Token(TokenType.NUMBER, lexeme="1", literal=1.0, line=7, col=33))
            )
        ), 1)
    ]

    assert len(res.interp.locals) == len(exp_locals)

    for local, dist in exp_locals:
        assert local in res.interp.locals
        assert res.interp.locals[local] == dist


def test_resolve_error() -> None:
    pass
