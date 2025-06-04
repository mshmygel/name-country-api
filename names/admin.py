from django.contrib import admin
from .models import Name, Country, NameCountryProbability


@admin.register(Name)
class NameAdmin(admin.ModelAdmin):
    list_display = ("name", "request_count", "last_accessed_at")
    search_fields = ("name",)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("alpha2_code", "name", "region", "capital")
    search_fields = ("alpha2_code", "name", "region", "capital")


@admin.register(NameCountryProbability)
class NameCountryProbabilityAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "probability")
    search_fields = ("name__name", "country__alpha2_code")
