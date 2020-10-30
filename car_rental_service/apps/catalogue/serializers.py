from rest_framework import serializers

from .car_categories import CarCategories
from .models import Car


class CarSerializer(serializers.HyperlinkedModelSerializer):
    """
    Car Hyperlinked Model Serializer used for Car listing
    """
    category = serializers.ChoiceField(choices=CarCategories.choices)
    is_hired = serializers.ReadOnlyField()
    class Meta:
        model = Car
        fields = ('url','number','category',
                  'is_hired',
                  'current_milage')


class RentACarSerializer(serializers.Serializer):
    valid_from = serializers.DateTimeField()
