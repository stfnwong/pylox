from loxpy.expr import Expr, BinaryExpr, LiteralExpr
from loxpy.token import Token, TokenType
from loxpy.scanner import Scanner
from loxpy.parser import Parser
from loxpy.interpreter import Interpreter
from loxpy.util import float_equal


def load_source(filename:str) -> str:
    with open(filename, 'r') as fp:
        source = fp.read()
    return str(source)

def parse_source(expr_src: str) -> Expr:
    scanner       = Scanner(expr_src)
    token_list    = scanner.scan()
    parser        = Parser(token_list)
    parsed_output = parser.parse()

    return parsed_output



#def test_interpret_unary() -> None:
#    # Get an interpreter
#    interp = Interpreter.Interpreter(verbose=True)
#    # Create test expression
#    tok_bang = Token(Token.BANG, "!", None, 1)
#    tok_iden = Token(Token.IDENTIFIER, "a", None, 1)
#    expr     = Expression.Unary(tok_bang, tok_iden)
#    print('Interpreting expression [%s]' % str(expr))
#
#    from pudb import set_trace; set_trace()
#    # interpret the expression
#    value = interp.interpret(expr)
#    print(value)
#    assert value is not None

#def test_interpret_unary_from_source() -> None:
#    unary_file = 'programs/unary.lox'
#    parsed_output = parse_source(load_source(unary_file))
#

def test_interpret_binary() -> None:
    interp = Interpreter(verbose=True)
    tok_num1 = Token(TokenType.NUMBER, "2", None, 1)
    tok_mul  = Token(TokenType.STAR, "*", None, 1)
    tok_num2 = Token(TokenType.NUMBER, "4", None, 1)

    expr     = BinaryExpr(tok_mul, LiteralExpr(tok_num1), LiteralExpr(tok_num2))

    exp_value = 8.0
    value = interp.interpret(expr)
    assert float_equal(value, exp_value)
