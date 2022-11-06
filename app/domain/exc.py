class CustomException(Exception):
    message: str | None = "Some exception"

    def __init__(self, *args):
        super().__init__(args)

        self.message = args and str(args[0])


class BadRequest(CustomException):
    message = "bad request"


class NotFound(CustomException):
    message = "not found"


class NotAuth(CustomException):
    message = "user not auth"


class AccessDenied(CustomException):
    message = "access denied"
