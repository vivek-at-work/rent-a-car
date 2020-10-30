
class IncorrectBaseRateError(Exception):
    """Exception is raised while trying to parse the Base Rate value to float.
    Attributes:
        base_rate_value -- base rate value that caused the exception
    """

    def __init__(self, base_rate_value, message='Could not parse the base rate value.'):
        self.base_rate_value = base_rate_value
        self.message = message
        super().__init__(self.message)


class IncorrectParKilometerPriceError(Exception):
    """Exception is raised while trying to parse the per kilometer price value to float.
    Attributes:
        per_km_price -- per km price value that caused the exception
    """

    def __init__(self, per_km_price, message='Could not parse the par km meter price value.'):
        self.per_km_price = per_km_price
        self.message = message
        super().__init__(self.message)


class PriceCalculatorNotFoundError(Exception):
    """Exception is raised while access price calculator for a car.
    Attributes:
        car_type -- car_type that caused the exception
    """

    def __init__(self, car_type, message='Could not find the caluclator for the car.'):
        self.car_type = car_type
        self.message = message
        super().__init__(self.message)
