class ReturnDataNotAvailableError(Exception):
    """ReturnDateNotAvailableError should be raised while trying
       to any data that we are suppored to access
       last_milage , returned_at , payable_amount
       of a booking and they are set to None

    Attributes:
        booking -- booking object that caused this exception.
    """

    def __init__(
        self, booking, message='Could not find the return information for the booking.'
    ):
        self.booking = booking
        self.message = message
        super().__init__(self.message)


class BookingClosedError(Exception):
    """BookingClosedError should be raised while trying close and
       already closed booking.

    Attributes:
        booking -- booking object that caused the exception
    """

    def __init__(
        self,
        booking,
        message='Can not close a booking that is already in closed state.',
    ):
        self.booking = booking
        self.message = message
        super().__init__(self.message)
