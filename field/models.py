from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.gis.db import models as gis_models

from django.utils.translation import gettext_lazy as _

from users.models import User


class FootballField(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=100)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fields')
    location = gis_models.PointField(srid=4326, null=True, blank=True)


def __str__(self):
    return f"{self.name}"

class FieldImage(models.Model):
    field = models.ForeignKey(FootballField, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='field_images/')

class Reservation(models.Model):
    field = models.ForeignKey(FootballField, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)


    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_time__gt=models.F('start_time')),
                name='check_end_time_after_start_time'
            )
        ]

    def save(self, *args, **kwargs):
        duration = Decimal((self.end_time - self.start_time).total_seconds() / 3600)
        self.total_price = self.field.price_per_hour * duration.quantize(Decimal('0.01'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.field.name}"



class Review(models.Model):
    field = models.ForeignKey(FootballField, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)