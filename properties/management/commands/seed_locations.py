from django.core.management.base import BaseCommand

from properties.models.location_model import Location


class Command(BaseCommand):
    help = "Seed initial location data"

    def handle(self, *args, **kwargs):
        # Define countries
        countries = ["Dubai", "Bangladesh", "Turkey", "Germany"]
        city_data = {
            "Dubai": ["Dubai City", "Marina", "Jumeirah", "Deira", "Bur Dubai"],
            "Bangladesh": ["Dhaka", "Chittagong", "Sylhet", "Khulna", "Rangpur"],
            "Turkey": ["Istanbul", "Ankara", "Izmir", "Antalya", "Bursa"],
            "Germany": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne"],
        }

        created_count = 0
        # Create countries
        for country_name in countries:
            country_obj, _ = Location.objects.get_or_create(
                name=country_name,
                location_type=Location.LocationType.COUNTRY,
                parent_location=None,
            )

            # Create cities
            for city_name in city_data.get(country_name, []):
                city_obj, _ = Location.objects.get_or_create(
                    name=city_name,
                    location_type=Location.LocationType.CITY,
                    parent_location=country_obj,
                )
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {created_count} neighborhood locations successfully!"
            )
        )
