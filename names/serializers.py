from rest_framework import serializers
from .models import Name, Country, NameCountryProbability


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            "alpha2_code",
            "name",
            "common_name",
            "region",
            "subregion",
            "capital",
            "latitude",
            "longitude",
            "flag_png",
            "flag_svg",
            "coat_of_arms_png",
            "coat_of_arms_svg",
            "borders",
            "independent",
        ]


class NameCountryProbabilitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = NameCountryProbability
        fields = [
            "country",
            "probability",
        ]


class NameSerializer(serializers.ModelSerializer):
    country_probabilities = NameCountryProbabilitySerializer(many=True, read_only=True)

    class Meta:
        model = Name
        fields = [
            "name",
            "last_accessed_at",
            "request_count",
            "country_probabilities",
        ]
