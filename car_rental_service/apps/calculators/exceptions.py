
class RequiredArgumentNotAvailableError(Exception):
    """RequiredArgumentNotAvailableError is raised while calculate
       method is not provided with required keyword arguments.
    Attributes:
        argument_name -- name of the keyword argument that is required.
    """

    def __init__(self, argument_name, message='Could not find the required argument.'):
        self.argument_name = argument_name
        self.message = message
        super().__init__(self.message)
