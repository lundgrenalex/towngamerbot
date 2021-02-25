class GameError(Exception):

    def __init__(self, message=None):
        self.message = message or self.message
        assert self.message, 'Message not implemented!'
        super(GameError, self).__init__(message)

    def __str__(self):
        if self.internal_message:
            return f'{self.message}, {self.internal_message}'
        return self.message
