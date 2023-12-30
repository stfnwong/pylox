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
