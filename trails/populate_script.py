import os
import random

# Ensure Django environment is set
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trails.settings')
import django
django.setup()
from trails_web.models import Category, Trail, UserProfile, Review, TrailLike
from django.core.files.base import ContentFile
from django.contrib.auth.models import User

# Sample Data
CATEGORY_NAMES = ['Mountain', 'Forest', 'Coastal', 'Urban', 'Loch Lomond'] 
TRAILS_DATA = [
    {"name": "Conic Hill", "length": 4.2, "estimate_time": 2.5, "level": "Moderate", "elevation_gain": 323, "longitude": -4.53897, "latitude": 56.08501, "category": "Loch Lomond"},
    {"name": "Ben Lomond Mountain Path", "length": 12.4, "estimate_time": 5.32, "level": "Hard", "elevation_gain": 961, "longitude": -4.64176, "latitude": 56.15214, "category": "Loch Lomond"},
    {"name": "Conic Hill via Balmaha Loop", "length": 5.6, "estimate_time": 2.15, "level": "Hard", "elevation_gain": 358, "longitude": -4.53935, "latitude": 56.0852, "category": "Loch Lomond"},
    {"name": "Ben Lomond via Ptarmigan Ridge Path", "length": 12.1, "estimate_time": 4.2, "level": "Hard", "elevation_gain": 960, "longitude": -4.64299, "latitude": 56.15344, "category": "Loch Lomond"},
    {"name": "The Cobbler (Ben Arthur)", "length": 11.6, "estimate_time": 5.1, "level": "Hard", "elevation_gain": 850, "longitude": -4.7509, "latitude": 56.2058, "category": "Loch Lomond"},
    {"name": "Ben A'an", "length": 3.9, "estimate_time": 2.1, "level": "Moderate", "elevation_gain": 345, "longitude": -4.40605, "latitude": 56.23241, "category": "Loch Lomond"},
    {"name": "West Highland Way: Drymen to Rowardennan", "length": 23.5, "estimate_time": 6.39, "level": "Hard", "elevation_gain": 699, "longitude": -4.64192, "latitude": 56.15187, "category": "Loch Lomond"},
    {"name": "West Highland Way: Tyndrum to Inveroran", "length": 14.3, "estimate_time": 4.17, "level": "Moderate", "elevation_gain": 476, "longitude": -4.71344, "latitude": 56.43835, "category": "Loch Lomond"},
    {"name": "West Highland Way: Inverarnan to Tyndrum", "length": 20.3, "estimate_time": 5.39, "level": "Hard", "elevation_gain": 705, "longitude": -4.72199, "latitude": 56.3283, "category": "Loch Lomond"},
    {"name": "Ben Ledi Circular", "length": 10.0, "estimate_time": 4.3, "level": "Hard", "elevation_gain": 782, "longitude": -4.28287, "latitude": 56.25423, "category": "Loch Lomond"},
    {"name": "Ben Vane", "length": 11.9, "estimate_time": 5.0, "level": "Hard", "elevation_gain": 1043, "longitude": -4.70933, "latitude": 56.25161, "category": "Loch Lomond"},
    {"name": "Ben Vorlich", "length": 13.7, "estimate_time": 5.3, "level": "Hard", "elevation_gain": 1001, "longitude": -4.70856, "latitude": 56.25209, "category": "Loch Lomond"},
    {"name": "Rob Roy's Cave via Loch Ard Sculpture Trail", "length": 7.1, "estimate_time": 1.46, "level": "Moderate", "elevation_gain": 147, "longitude": -4.41964, "latitude": 56.1785, "category": "Loch Lomond"},
    {"name": "The West Highland Way: Rowardennan to Inverarnan", "length": 23.2, "estimate_time": 7.4, "level": "Hard", "elevation_gain": 490, "longitude": -4.72191, "latitude": 56.32809, "category": "Loch Lomond"},
    {"name": "Drymen to Balmaha Via West Highland Way", "length": 11.9, "estimate_time": 3.75, "level": "Hard", "elevation_gain": 448, "longitude": -4.44047, "latitude": 56.06833, "category": "Loch Lomond"},
    {"name": "Loch Earn to Ben Vorlich", "length": 9.8, "estimate_time": 4.75, "level": "Hard", "elevation_gain": 877, "longitude": -4.21622, "latitude": 56.38139, "category": "Loch Lomond"},
    {"name": "Beinn Dubh", "length": 7.6, "estimate_time": 3.5, "level": "Hard", "elevation_gain": 625, "longitude": -4.63958, "latitude": 56.10261, "category": "Loch Lomond"},
    {"name": "Ben Vorlich and Stùc a' Chroin", "length": 14.5, "estimate_time": 5.0, "level": "Hard", "elevation_gain": 1170, "longitude": -4.21486, "latitude": 56.38139, "category": "Loch Lomond"},
    {"name": "Balmaha to Rowardennan", "length": 11.9, "estimate_time": 3.0, "level": "Moderate", "elevation_gain": 291, "longitude": -4.63954, "latitude": 56.1469, "category": "Loch Lomond"},
    {"name": "Beinn Narnain and Beinn Ime", "length": 14.2, "estimate_time": 5.0, "level": "Hard", "elevation_gain": 1257, "longitude": -4.75033, "latitude": 56.20614, "category": "Loch Lomond"},
    {"name": "West Highland Way: Rowardennan to Inversnaid", "length": 11.7, "estimate_time": 3.0, "level": "Moderate", "elevation_gain": 238, "longitude": -4.68512, "latitude": 56.24316, "category": "Loch Lomond"},
    {"name": "Balloch Castle Country Park Circular", "length": 3.5, "estimate_time": 0.8, "level": "Easy", "elevation_gain": 64, "longitude": -4.58116, "latitude": 56.00608, "category": "Loch Lomond"},
    {"name": "Ben More and Stob Binnein", "length": 10.5, "estimate_time": 6.4, "level": "Hard", "elevation_gain": 1260, "longitude": -4.57057, "latitude": 56.3987, "category": "Loch Lomond"},
    {"name": "Beinn Narnain Circular", "length": 10.3, "estimate_time": 5.0, "level": "Hard", "elevation_gain": 910, "longitude": -4.75034, "latitude": 56.20615, "category": "Loch Lomond"},
    {"name": "Puck's Glen Gorge Trail", "length": 2.6, "estimate_time": 1.0, "level": "Moderate", "elevation_gain": 132, "longitude": -4.9743, "latitude": 56.01217, "category": "Loch Lomond"},
    {"name": "Ben Venue", "length": 14.3, "estimate_time": 5.0, "level": "Hard", "elevation_gain": 736, "longitude": -4.41198, "latitude": 56.23099, "category": "Loch Lomond"}
]

USERNAMES = ['alice', 'bob', 'charlie']
REVIEWS = [
    "Amazing trail! Loved it!",
    "Pretty good, but quite challenging.",
    "Not bad, but needs better maintenance.",
    "Fantastic views!",
    "Would definitely hike again!"
]

def populate():
    print("Creating categories...")
    categories = []
    for name in CATEGORY_NAMES:
        category, created = Category.objects.get_or_create(name=name, slug=name.lower().replace(" ", "-"))
        categories.append(category)
    loch_lomond_category, created = Category.objects.get_or_create(name="Loch Lomond", slug="loch-lomond")

    print("Creating trails...")
    trails = []
    for trail_data in TRAILS_DATA:
        category = random.choice(categories)
        print(category)
        trail, created = Trail.objects.get_or_create(
            title=trail_data["name"],
            length=trail_data["length"],
            estimate_time=trail_data["estimate_time"],
            level=trail_data["level"],
            elevation_gain=trail_data["elevation_gain"],
            longitude=trail_data["longitude"],
            latitude=trail_data["latitude"],
            category=loch_lomond_category
        )
        trails.append(trail)

    print("Creating users and profiles...")
    users = []
    for username in USERNAMES:
        user, created = User.objects.get_or_create(username=username, email=f"{username}@example.com")
        user.set_password("password123")  # Set a default password
        user.save()

        # Ensure UserProfile is created only if it doesn't already exist
        profile, created = UserProfile.objects.get_or_create(user=user)

        # Only update favorite_trail if the profile was newly created
        if created:
            profile.favorite_trail = random.choice(trails)
            profile.save()
        users.append(profile)

    print("Creating reviews...")
    for user_profile in users:
        for _ in range(random.randint(5, 8)):  # Each user writes 1-3 reviews
            trail = random.choice(trails)
            Review.objects.create(
                user=user_profile,
                trail=trail,
                comment=random.choice(REVIEWS),
                likes=random.randint(0, 10)
            )

    print("Creating trail likes...")
    for user_profile in users:
        liked_trails = random.sample(trails, random.randint(1, len(trails)))  # Each user likes 1+ trails
        for trail in liked_trails:
            TrailLike.objects.get_or_create(user=user_profile, trail=trail)

    print("Database population complete!")

if __name__ == "__main__":
    populate()