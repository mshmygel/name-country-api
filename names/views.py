import requests
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Name, Country, NameCountryProbability
from .serializers import NameSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated

@extend_schema(
    parameters=[
        OpenApiParameter(name="name", required=True, type=str, location=OpenApiParameter.QUERY),
    ]
)
class NameLookupView(APIView):
    """
    GET /names/?name=<name>

    This view receives a name as a query parameter and returns the most likely countries
    associated with that name based on data from nationalize.io and REST Countries API.

    - If the name exists in the database and was accessed within the last 24 hours,
      the stored data is returned.
    - Otherwise, it fetches data from external APIs, saves/updates it in the database,
      and returns the updated result.

    Response includes:
    - Name information
    - Request count
    - Last access time
    - List of related countries with probability and full country info
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        name_param = request.query_params.get("name")
        if not name_param:
            return Response({"error": "Missing 'name' query parameter."}, status=status.HTTP_400_BAD_REQUEST)

        # Try to get the name object or create it if not found
        name_obj, created = Name.objects.get_or_create(name=name_param.lower())

        # Return cached data if updated within the last 24 hours
        if not created and name_obj.last_accessed_at > timezone.now() - timedelta(days=1):
            serializer = NameSerializer(name_obj)
            return Response(serializer.data)

        # Otherwise increment request count and fetch new data
        name_obj.request_count += 1
        name_obj.save()

        # Request prediction data from nationalize.io
        response = requests.get(f"https://api.nationalize.io/?name={name_param}")
        if response.status_code != 200 or not response.json().get("country"):
            return Response({"error": "No country data found for this name."}, status=status.HTTP_404_NOT_FOUND)

        country_data = response.json()["country"]

        for entry in country_data:
            code = entry["country_id"]
            probability = entry["probability"]

            # Check if country already exists
            country = Country.objects.filter(alpha2_code=code).first()
            if not country:
                # Request country details from REST Countries API
                country_resp = requests.get(f"https://restcountries.com/v3.1/alpha/{code}")
                if country_resp.status_code != 200:
                    continue
                c_data = country_resp.json()[0]

                # Create new Country object
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

            # Create or update link between name and country with probability
            NameCountryProbability.objects.update_or_create(
                name=name_obj,
                country=country,
                defaults={"probability": probability},
            )

        # Serialize and return the final result
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

    This view returns the top 5 most frequently requested names associated
    with a given country code, sorted by request count (descending).

    If the country code is missing → returns 400.
    If no data is found for that country → returns 404.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        country_code = request.query_params.get("country")
        if not country_code:
            return Response({"error": "Missing 'country' query parameter."}, status=status.HTTP_400_BAD_REQUEST)

        country = Country.objects.filter(alpha2_code__iexact=country_code).first()
        if not country:
            return Response({"error": "Country not found."}, status=status.HTTP_404_NOT_FOUND)

        # Find top 5 names linked to this country, ordered by request_count
        top_names = (
            Name.objects.filter(country_probabilities__country=country)
            .annotate(link_count=Count("id"))
            .order_by("-request_count")[:5]
        )

        return Response([name.name for name in top_names])
