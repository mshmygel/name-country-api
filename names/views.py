from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Name, Country, NameCountryProbability
from .serializers import NameSerializer
from names.services.external_apis import get_nationalize_data, get_country_details


@extend_schema(
    parameters=[
        OpenApiParameter(name="name", required=True, type=str, location=OpenApiParameter.QUERY),
    ]
)
class NameLookupView(APIView):
    """
    GET /names/?name=<name>

    Returns the most likely countries associated with the given name.
    Data is cached for 24 hours. On cache miss, it fetches from external APIs.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        name_param = request.query_params.get("name")
        if not name_param:
            return Response({"error": "Missing 'name' query parameter."}, status=status.HTTP_400_BAD_REQUEST)

        name_obj, created = Name.objects.get_or_create(name=name_param.lower())

        if not created and name_obj.last_accessed_at > timezone.now() - timedelta(days=1):
            serializer = NameSerializer(name_obj)
            return Response(serializer.data)

        name_obj.request_count += 1
        name_obj.save()

        country_data = get_nationalize_data(name_param)
        if not country_data:
            return Response({"error": "No country data found for this name."}, status=status.HTTP_404_NOT_FOUND)

        for entry in country_data:
            code = entry["country_id"]
            probability = entry["probability"]

            country = Country.objects.filter(alpha2_code=code).first()
            if not country:
                c_data = get_country_details(code)
                if not c_data:
                    continue

                country = Country.objects.create(
                    alpha2_code=code,
                    name=c_data["name"]["official"],
                    common_name=c_data["name"].get("common", ""),
                    region=c_data.get("region", ""),
                    subregion=c_data.get("subregion", ""),
                    capital=c_data.get("capital", [""])[0],
                    latitude=c_data.get("latlng", [None, None])[0],
                    longitude=c_data.get("latlng", [None, None])[1],
                    flag_png=c_data.get("flags", {}).get("png", ""),
                    flag_svg=c_data.get("flags", {}).get("svg", ""),
                    coat_of_arms_png=c_data.get("coatOfArms", {}).get("png", ""),
                    coat_of_arms_svg=c_data.get("coatOfArms", {}).get("svg", ""),
                    borders=",".join(c_data.get("borders", [])),
                    independent=c_data.get("independent", None),
                )

            NameCountryProbability.objects.update_or_create(
                name=name_obj,
                country=country,
                defaults={"probability": probability},
            )

        serializer = NameSerializer(name_obj)
        return Response(serializer.data)


@extend_schema(
    parameters=[
        OpenApiParameter(name="country", required=True, type=str, location=OpenApiParameter.QUERY),
    ]
)
class PopularNamesView(APIView):
    """
    GET /popular-names/?country=<alpha2_code>

    Returns top 5 most requested names for a given country.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        country_code = request.query_params.get("country")
        if not country_code:
            return Response({"error": "Missing 'country' query parameter."}, status=status.HTTP_400_BAD_REQUEST)

        country = Country.objects.filter(alpha2_code__iexact=country_code).first()
        if not country:
            return Response({"error": "Country not found."}, status=status.HTTP_404_NOT_FOUND)

        top_names = (
            Name.objects.filter(country_probabilities__country=country)
            .annotate(link_count=Count("id"))
            .order_by("-request_count")[:5]
        )

        return Response([name.name for name in top_names])
