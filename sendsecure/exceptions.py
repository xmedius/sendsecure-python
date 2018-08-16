class SendSecureException(Exception):
    def __init__(self, code, message, details):
        self.code = code
        self.message = message
        self.details = details
    def __str__(self):
        return str(self.code) + ': ' + self.message

class UnexpectedServerResponseException(SendSecureException):
    def __init__(self, code, message, details):
        SendSecureException.__init__(self, code, message, details)
