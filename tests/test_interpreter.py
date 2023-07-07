# modules under test
from loxpy import Expression, Interpreter, Parser, Scanner, Token


def load_source(filename:str) -> str:
    with open(filename, 'r') as fp:
        source = fp.read()
    return str(source)

#def test_interpret_unary() -> None:
#    # Get an interpreter
#    interp = Interpreter.Interpreter(verbose=True)
#    # Create test expression
#    tok_bang = Token.Token(Token.BANG, "!", None, 1)
#    tok_iden = Token.Token(Token.IDENTIFIER, "a", None, 1)
#    expr     = Expression.Unary(tok_bang, tok_iden)
#    print('Interpreting expression [%s]' % str(expr))
#
#    from pudb import set_trace; set_trace()
#    # interpret the expression
#    value = interp.interpret(expr)
#    print(value)
#    assert value is not None

def test_interpret_unary_from_source() -> None:
    unary_file = 'programs/unary.lox'
    unary_source = load_source(unary_file)

    # Parse the source
    scanner = Scanner.Scanner(unary_source)
    unary_tokens = scanner.scan()
    parser = Parser.Parser(unary_tokens)
    unary_expr = parser.parse()

def test_interpret_binary() -> None:
    interp = Interpreter.Interpreter(verbose=True)
    tok_num1 = Token.Token(Token.NUMBER, "2", None, 1)
    tok_mul  = Token.Token(Token.STAR, "*", None, 1)
    tok_num2 = Token.Token(Token.NUMBER, "4", None, 1)

    expr     = Expression.Binary(tok_num1, tok_mul, tok_num2)
    #print('Interpreting expression [%s]' % str(expr))

    # interpret the expression
    value = interp.interpret(expr)
    print(value)
    assert value is not None
