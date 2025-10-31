from django.core.management.base import BaseCommand

from properties.models.basic_info import Amenity, PropertyTag
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
        amenity_icon_map = {
            "Swimming Pool": "SwimmingPool",
            "Gym": "Gym",
            "High‑Speed WiFi (500 Mbps)": "Wifi",
            "Parking": "Parking",
            "Air Conditioning": "AirConditioning",
            "24/7 Security": "ShieldCheck",
            "Playground": "Playground",
            "Garden": "Garden",
            "Lift": "Lift",
            "Backup Power": "Zap",
        }
        for name, icon_name in amenity_icon_map.items():
            Amenity.objects.get_or_create(
                name=name,
                defaults={"icon": icon_name}
            )

        # 🏠 Property Features with category and is_premium
        features = [
            # 🏠 Indoor
            {"name": "Air Conditioning", "category": "indoor"},
            {"name": "Heating", "category": "indoor"},
            {"name": "Fully Furnished", "category": "indoor"},
            {"name": "Modular Kitchen", "category": "indoor"},
            {"name": "Smart Home System", "category": "indoor", "is_premium": True},
            {"name": "Hardwood Floors", "category": "indoor"},
            {"name": "Walk-in Closet", "category": "indoor"},
            {"name": "Open Floor Plan", "category": "indoor"},
            {"name": "Home Office", "category": "indoor"},
            {"name": "In-unit Laundry", "category": "indoor"},
            {"name": "Mudroom", "category": "indoor"},
            {"name": "Wine Cellar", "category": "indoor"},
            {"name": "Home Theater", "category": "indoor"},
            {"name": "Ergonomic Furniture", "category": "indoor"},
            # 🌳 Outdoor
            {"name": "Private Garden", "category": "outdoor"},
            {"name": "Balcony", "category": "outdoor"},
            {"name": "Rooftop Terrace", "category": "outdoor"},
            {"name": "Rooftop Lounge", "category": "outdoor", "is_premium": True},
            {"name": "Barbecue Area", "category": "outdoor"},
            {"name": "Community BBQ Area", "category": "outdoor"},
            {"name": "Large Windows", "category": "outdoor"},
            {"name": "Skylights", "category": "outdoor"},
            {"name": "Garden", "category": "outdoor"},
            # 🧯 Safety
            {"name": "24/7 Security", "category": "safety"},
            {"name": "CCTV Surveillance", "category": "safety"},
            {"name": "Smoke Detector", "category": "firesafety"},
            {"name": "Fire Alarm", "category": "firesafety"},
            {"name": "Emergency Exit", "category": "safety"},
            {"name": "Advanced Security System", "category": "safety"},
            {"name": "Smart Thermostat", "category": "safety"},
            # 🏋️ Fitness
            {"name": "Gym", "category": "fitness"},
            {"name": "Swimming Pool", "category": "fitness"},
            {"name": "Sauna", "category": "fitness", "is_premium": True},
            {"name": "Yoga Studio", "category": "fitness"},
            {"name": "Gym Room", "category": "fitness"},
            {"name": "Hot Tub", "category": "fitness"},
            {"name": "Tennis Court", "category": "fitness"},
            {"name": "Basketball Court", "category": "fitness"},
            {"name": "Golf Course Access", "category": "fitness"},
            # 🐕 Pets
            {"name": "Pet Friendly", "category": "pets"},
            {"name": "Pet Play Area", "category": "pets", "is_premium": True},
            {"name": "Pet Wash Station", "category": "pets"},
            # 🚗 Parking
            {"name": "Covered Parking", "category": "parking"},
            {"name": "Visitor Parking", "category": "parking"},
            {"name": "Private Parking", "category": "parking"},
            {
                "name": "Electric Vehicle Charging Station",
                "category": "parking",
                "is_premium": True,
            },
            # 🏡 Amenities
            {"name": "Clubhouse", "category": "amenities"},
            {"name": "Children’s Play Area", "category": "amenities"},
            {"name": "Community Hall", "category": "amenities"},
            {"name": "Cinema Room", "category": "amenities", "is_premium": True},
            {"name": "Lift", "category": "amenities"},
            {"name": "Backup Power", "category": "amenities"},
            # 💎 Premium / Other
            {"name": "Infinity Pool", "category": "other", "is_premium": True},
            {"name": "Panoramic View", "category": "other", "is_premium": True},
            {"name": "Servant Quarters", "category": "other"},
            {"name": "Backup Generator", "category": "other"},
            {"name": "Helipad", "category": "other"},
            {"name": "Private Elevator", "category": "other"},
            {"name": "Solar Panels", "category": "other"},
            {"name": "Energy Efficient Appliances", "category": "other"},
            {"name": "Smart Home Integration", "category": "other"},
            {"name": "Automated Lighting", "category": "other"},
            {"name": "Climate Control", "category": "other"},
            {"name": "Water Filtration System", "category": "other"},
            {"name": "Green Roof", "category": "other"},
            {"name": "Rainwater Harvesting System", "category": "other"},
            {"name": "Composting Facility", "category": "other"},
            {"name": "Community Garden", "category": "other"},
            {"name": "High-speed Internet", "category": "other"},
            {"name": "Cable TV", "category": "other"},
            {"name": "Satellite TV", "category": "other"},
            {"name": "Starlink Access", "category": "other"},
            {"name": "Fiber Optic Connection", "category": "other"},
            {"name": "Dedicated Workspace", "category": "other"},
        ]

        # Seed PropertyFeature
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
                "Successfully seeded property tags, amenities, and features."
            )
        )
