from django.db import models


class AvailabelCarQuerySet(models.QuerySet):
    def all(self):
        return self.filter(is_hired=False)
