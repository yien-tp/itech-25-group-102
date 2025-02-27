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
CATEGORY_NAMES = ['Mountain', 'Forest', 'Coastal', 'Urban']
TRAILS_DATA = [
    {"title": "Rocky Ridge", "length": 5.4, "estimate_time": 120, "level": "Moderate", "elevation_gain": 450, "address": "Colorado, USA"},
    {"title": "Sunset Valley", "length": 3.2, "estimate_time": 90, "level": "Easy", "elevation_gain": 120, "address": "California, USA"},
    {"title": "Forest Whisper", "length": 8.0, "estimate_time": 180, "level": "Hard", "elevation_gain": 700, "address": "Oregon, USA"},
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

    print("Creating trails...")
    trails = []
    for trail_data in TRAILS_DATA:
        category = random.choice(categories)
        trail, created = Trail.objects.get_or_create(
            title=trail_data["title"],
            length=trail_data["length"],
            estimate_time=trail_data["estimate_time"],
            level=trail_data["level"],
            elevation_gain=trail_data["elevation_gain"],
            address=trail_data["address"],
            category=category
        )
        trails.append(trail)

    print("Creating users and profiles...")
    users = []
    for username in USERNAMES:
        user, created = User.objects.get_or_create(username=username, email=f"{username}@example.com")
        user.set_password("password123")  # Set a default password
        user.save()

        profile, created = UserProfile.objects.get_or_create(
            user=user,
            favorite_trail=random.choice(trails)
        )
        users.append(profile)

    print("Creating reviews...")
    for user_profile in users:
        for _ in range(random.randint(1, 3)):  # Each user writes 1-3 reviews
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