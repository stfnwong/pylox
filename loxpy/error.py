from loxpy.token import Token


class LoxParseError(Exception):
    def __init__(self, token: Token, msg:str) -> None:
        self.token   :Token = token
        self.message :str = msg


class LoxInterpreterError(Exception):
    def __init__(self, token: Token, msg: str) -> None:
        super(LoxInterpreterError, self).__init__(msg)
        self.token = token
        self.message = msg


class LoxRuntimeError(Exception):
    def __init__(self, token: Token, msg: str) -> None:
        super(LoxRuntimeError, self).__init__(msg)
        self.token = token
        self.message = msg


#class LoxResolverWarning(Exception):
#    def __init__(self, token: Token, msg: str) -> None:
#        super(LoxResolverWarning, self).__init__(msg)
#        self.token = token
#        self.message = msg
#
