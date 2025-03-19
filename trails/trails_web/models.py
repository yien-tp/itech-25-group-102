import os
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible

# --------------------
# Category
# --------------------
class Category(models.Model):
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

# --------------------
# Helper: ProfileImagePath
# --------------------
@deconstructible
class ProfileImagePath:
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        username = instance.user.username.upper()
        # Count existing profile pictures for this user
        existing_files = UserProfile.objects.filter(user=instance.user, personal_image__isnull=False)
        count = existing_files.count() + 1
        # Construct the new filename
        filename = f"{username}_PROFILE_{count}.{ext}"
        return os.path.join('profile_pics/', filename)

# --------------------
# UserProfile
# --------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    personal_image = models.ImageField(upload_to=ProfileImagePath(), blank=True, null=True)
    favorite_trails = models.ManyToManyField('Trail', blank=True, related_name="favorited_by")
    personal_bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

# --------------------
# Helper: TrailImagePath
# --------------------
@deconstructible
class TrailImagePath:
    """
    A callable class that returns the path: 'trail_images/<pk>.<ext>'
    If the trail is not yet saved (pk is None), we temporarily use 'temp_<title>.<ext>'.
    """
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if instance.pk:
            # If the instance is saved, use its primary key
            new_filename = f"{instance.pk}.{ext}"
        else:
            # Fallback if pk is not available yet
            safe_title = instance.title.replace(' ', '_')[:20]
            new_filename = f"temp_{safe_title}.{ext}"
        return os.path.join('trail_images', new_filename)

# --------------------
# Trail
# --------------------
class Trail(models.Model):
    title = models.CharField(max_length=128, unique=True)
    length = models.FloatField(default=0.0)
    estimate_time = models.FloatField(default=0.0)
    level = models.CharField(max_length=128)
    elevation_gain = models.IntegerField()
    address = models.CharField(max_length=128)
    likes = models.IntegerField(default=0)

    # Remove the duplicate category field; keep only one
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="trails")

    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    # Use the custom path function to name the file <pk>.<ext>
    image = models.ImageField(upload_to=TrailImagePath(), blank=True, null=True)

    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="created_trails"
    )

    def save(self, *args, **kwargs):
        # Round estimate_time to 2 decimal places
        if self.estimate_time:
            self.estimate_time = round(self.estimate_time, 2)
        # Round lat/lng to 5 decimal places
        if self.latitude:
            self.latitude = round(self.latitude, 5)
        if self.longitude:
            self.longitude = round(self.longitude, 5)

        super(Trail, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

# --------------------
# Review
# --------------------
class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="reviews")
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE, related_name="reviews")
    pictures = models.ImageField(upload_to='review_pics/', blank=True, null=True)
    comment = models.CharField(max_length=128)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.user.username} on {self.trail.title}"

# --------------------
# TrailLike
# --------------------
class TrailLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="liked_trails")
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE, related_name="liked_by")

    class Meta:
        unique_together = ('user', 'trail')

    def __str__(self):
        return f"{self.user.user.username} likes {self.trail.title}"
    
# --------------------
# ReviewLike
# --------------------
class ReviewLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="liked_reviews")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="liked_by")

    class Meta:
        unique_together = ('user', 'review')  # One like per user per review

    def __str__(self):
        return f"{self.user.user.username} likes review {self.review.id}"