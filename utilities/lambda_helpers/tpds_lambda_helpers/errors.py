class RetryError(Exception):
    '''
    Class to handle exceptions that need the job to be retried
    '''
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'{self.__class__.__name__}({self.message})'

    def __repr__(self):
        return str(self)


class DeleteError(Exception):
    '''
    Class to handle exceptions that allow for message deletion from the queue
    '''
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'{self.__class__.__name__}({self.message})'

    def __repr__(self):
        return str(self)