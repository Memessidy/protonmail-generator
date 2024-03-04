class NoEmailVerification(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotAvailableDomainException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class GettingVerificationCodeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
