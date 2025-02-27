from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    NAME_MAX_LENGTH = 128 # Attribute to hold the max length
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

class Trail(models.Model):
    title = models.CharField(max_length=128, unique=True)
    length = models.FloatField()
    estimate_time = models.IntegerField()
    level = models.CharField(max_length=128)
    elevation_gain = models.IntegerField()
    address = models.CharField(max_length=128)
    likes = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="trails")

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    personal_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    favorite_trail = models.ForeignKey(Trail, on_delete=models.SET_NULL, null=True, blank=True, related_name="favorite_users")

    def __str__(self):
        return self.user.username

class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="reviews")
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE, related_name="reviews")
    pictures = models.ImageField(upload_to='review_pics/', blank=True, null=True)
    comment = models.CharField(max_length=128)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"Review by {self.user.user.username} on {self.trail.title}"

class TrailLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="liked_trails")
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE, related_name="liked_by")

    class Meta:
        unique_together = ('user', 'trail')

    def __str__(self):
        return f"{self.user.user.username} likes {self.trail.title}"
    
 