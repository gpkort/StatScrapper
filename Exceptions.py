class IllegalArgumentError(ValueError):

    def __init__(self, message: str):
        super(IllegalArgumentError, self).__init__(message)