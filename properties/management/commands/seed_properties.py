from django.core.management.base import BaseCommand

from agency.models.agent_model import Specialization
from properties.models.basic_info import Amenity, Currency, PropertyTag
from properties.models.property_feature import PropertyFeature


class Command(BaseCommand):
    help = "Seed initial property data"

    def handle(self, *args, **kwargs):
        # 🏷️ Property Tags
        property_tags = [
            "Luxury",
            "Affordable",
            "Beachfront",
            "Mountain View",
            "Family Friendly",
            "Newly Built",
            "Pet Friendly",
            "Smart Home",
            "Eco Friendly",
            "Investment",
        ]
        for name in property_tags:
            PropertyTag.objects.get_or_create(name=name)

        # 🏡 Amenities
        amenities = [
            "Swimming Pool",
            "Gym",
            "Wi-Fi",
            "Parking",
            "Air Conditioning",
            "24/7 Security",
            "Playground",
            "Garden",
            "Lift",
            "Backup Power",
        ]
        for name in amenities:
            Amenity.objects.get_or_create(name=name)

        # 💰 Currencies
        currencies = [
            {"currency": "USD"},
            {"currency": "EUR"},
            {"currency": "GBP"},
            {"currency": "AED"},
            {"currency": "BDT"},
            {"currency": "INR"},
        ]
        for cur in currencies:
            Currency.objects.get_or_create(currency=cur["currency"])

        # 🏗️ Specializations
        specializations = [
            {
                "name": "Residential",
                "description": "Homes, apartments, and villas for living.",
            },
            {
                "name": "Commercial",
                "description": "Office spaces, shops, and retail properties.",
            },
            {
                "name": "Industrial",
                "description": "Warehouses, factories, and production facilities.",
            },
            {
                "name": "Land",
                "description": "Plots and land parcels for development or investment.",
            },
            {
                "name": "Mixed-Use",
                "description": "Properties combining residential and commercial use.",
            },
            {
                "name": "Luxury",
                "description": "High-end, premium residential or commercial assets.",
            },
        ]
        for spec in specializations:
            Specialization.objects.get_or_create(
                name=spec["name"], defaults={"description": spec["description"]}
            )

            features = [
                # 🏠 Indoor
                {"name": "Air Conditioning", "category": "indoor"},
                {"name": "Heating", "category": "indoor"},
                {"name": "Fully Furnished", "category": "indoor"},
                {"name": "Modular Kitchen", "category": "indoor"},
                {"name": "Smart Home System", "category": "indoor", "is_premium": True},
                # 🌳 Outdoor
                {"name": "Private Garden", "category": "outdoor"},
                {"name": "Balcony or Terrace", "category": "outdoor"},
                {"name": "Rooftop Lounge", "category": "outdoor", "is_premium": True},
                {"name": "Barbecue Area", "category": "outdoor"},
                # 🧯 Safety
                {"name": "24/7 Security", "category": "safety"},
                {"name": "CCTV Surveillance", "category": "safety"},
                {"name": "Smoke Detector", "category": "firesafety"},
                {"name": "Fire Alarm", "category": "firesafety"},
                {"name": "Emergency Exit", "category": "safety"},
                # 🏋️ Fitness
                {"name": "Gym", "category": "fitness"},
                {"name": "Swimming Pool", "category": "fitness"},
                {"name": "Sauna", "category": "fitness", "is_premium": True},
                {"name": "Yoga Studio", "category": "fitness"},
                # 🐕 Pets
                {"name": "Pet Friendly", "category": "pets"},
                {"name": "Pet Play Area", "category": "pets", "is_premium": True},
                # 🚗 Parking
                {"name": "Covered Parking", "category": "parking"},
                {"name": "Visitor Parking", "category": "parking"},
                {
                    "name": "Electric Car Charging",
                    "category": "parking",
                    "is_premium": True,
                },
                # 🏡 Amenities
                {"name": "Clubhouse", "category": "amenities"},
                {"name": "Children’s Play Area", "category": "amenities"},
                {"name": "Community Hall", "category": "amenities"},
                {"name": "Cinema Room", "category": "amenities", "is_premium": True},
                # 💎 Other / Premium
                {"name": "Infinity Pool", "category": "other", "is_premium": True},
                {"name": "Panoramic View", "category": "other", "is_premium": True},
                {"name": "Servant Quarters", "category": "other"},
                {"name": "Backup Generator", "category": "other"},
            ]

            for feature in features:
                PropertyFeature.objects.get_or_create(
                    name=feature["name"],
                    defaults={
                        "category": feature.get("category"),
                        "is_premium": feature.get("is_premium", False),
                    },
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded property tags, amenities, specializations, features, and currencies."
            )
        )
