from .exceptions import RequiredArgumentNotAvailableError


class BasePriceCalculator:
    """
    BasePriceCalculator : BasePriceCalculator is parent class for all price calculators
    """
    def validate_required_argument(self, field, **kwargs):
        value = kwargs.get(field, None)
        if value is None:
            raise RequiredArgumentNotAvailableError(field)
        return value

    def calculate(self, base_day_rental, number_of_days, **kwargs):
        raise NotImplementedError


class CompactCarPriceCalculator(BasePriceCalculator):
    """
    CompactCarPriceCalculator : Price calculator for Compact Cars
    """
    def calculate(self, base_day_rental, number_of_days, **kwargs):
        return base_day_rental * number_of_days


class PremiumCarPriceCalculator(BasePriceCalculator):
    """
    PremiumCarPriceCalculator : Price calculator for Premium Cars
    """
    def calculate(self, base_day_rental, number_of_days, **kwargs):
        per_km_price = self.validate_required_argument('per_km_price', **kwargs)
        number_of_kilo_meters = self.validate_required_argument(
            'number_of_kilo_meters', **kwargs
        )
        return (
            base_day_rental * number_of_days * 1.2
            + per_km_price * number_of_kilo_meters
        )


class MiniVanPriceCalculator(BasePriceCalculator):
    """
    MiniVanPriceCalculator : Price calculator for MiniVans.
    """
    def calculate(self, base_day_rental, number_of_days, **kwargs):
        per_km_price = self.validate_required_argument('per_km_price', **kwargs)
        number_of_kilo_meters = self.validate_required_argument(
            'number_of_kilo_meters', **kwargs
        )
        return base_day_rental * number_of_days * 1.7 + (
            per_km_price * number_of_kilo_meters * 1.5
        )
