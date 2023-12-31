import pytest

from loxpy.error import LoxRuntimeError
from loxpy.environment import Environment
from loxpy.token import Token, TokenType
from loxpy.util import float_equal


def test_init_env() -> None:
    env = Environment()

    assert len(env) == 0

    # Add some variables 
    var_name = "a"
    var_value = 10.0

    env.define(var_name, var_value)

    var_token = Token(TokenType.VAR, var_name, None, 1)

    env_ret = env.get(var_token)
    assert float_equal(env_ret, var_value)

    # If we ask for a variable that does not exist we 
    # throw LoxRuntimeError.

    with pytest.raises(LoxRuntimeError):
        bad_token = Token(TokenType.VAR, "junk", None, 1)
        env.get(bad_token)


def test_enclosing_env() -> None:
    # Create outer vars 
    outer_env = Environment()
    outer_vars = [("a", 1.0), ("b", 2.0)]

    for oname, oval in outer_vars:
        outer_env.define(oname, oval)
        assert outer_env.get(
            Token(TokenType.VAR, oname, None, 1)
        )

    # Create inner vars 
    inner_env = Environment(outer_env)
    inner_vars = (("c", 3.0), ("d", 4.0))

    for iname, ival in inner_vars:
        inner_env.define(iname, ival)
        assert inner_env.get(
            Token(TokenType.VAR, iname, None, 1)
        )

    # Assert we can reach the outer variables from 
    # the inner scope 
    for oname, oval in outer_vars:
        assert inner_env.get(
            Token(TokenType.VAR, oname, None, 1)
        )

    # Test shadowing ?
