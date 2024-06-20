from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LanguageModel(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=50)


class MovieModel(TimestampedModel):
    name = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    release_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)]
    )
    language = models.ForeignKey(LanguageModel, on_delete=models.SET_DEFAULT, default='hi')
    rating = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return self.name
