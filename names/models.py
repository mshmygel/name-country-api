from django.db import models


class Country(models.Model):
    """Stores data about a country from the REST Countries API."""
    alpha2_code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=128)
    common_name = models.CharField(max_length=128, blank=True)
    region = models.CharField(max_length=64)
    subregion = models.CharField(max_length=64, blank=True)
    capital = models.CharField(max_length=64, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    flag_png = models.URLField(blank=True)
    flag_svg = models.URLField(blank=True)
    coat_of_arms_png = models.URLField(blank=True)
    coat_of_arms_svg = models.URLField(blank=True)
    borders = models.TextField(blank=True)
    independent = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.alpha2_code} — {self.name}"


class Name(models.Model):
    """Stores each unique name with last accessed timestamp and request count."""
    name = models.CharField(max_length=64, unique=True)
    last_accessed_at = models.DateTimeField(auto_now=True)
    request_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class NameCountryProbability(models.Model):
    """Links a name to a country with a probability score from Nationalize.io."""
    name = models.ForeignKey(Name, on_delete=models.CASCADE, related_name="country_probabilities")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="name_probabilities")
    probability = models.FloatField()

    class Meta:
        unique_together = ("name", "country")

    def __str__(self):
        return f"{self.name.name} → {self.country.alpha2_code}: {self.probability}"
