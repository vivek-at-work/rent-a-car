from django.db import models


class CarCategories(models.IntegerChoices):
   """
   Car Categories:
      It defines what type to car categories we are serving as present.
   """
   COMPACT = 1
   PREMIUM = 2
   MINIVAN = 3
