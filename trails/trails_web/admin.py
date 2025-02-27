from django.contrib import admin
from trails_web.models import Category, Trail, UserProfile, Review, TrailLike

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Trail)
class TrailAdmin(admin.ModelAdmin):
    list_display = ('title', 'length', 'estimate_time', 'level', 'elevation_gain', 'address', 'likes', 'category')
    search_fields = ('title', 'address')
    list_filter = ('level', 'category')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'favorite_trail')
    search_fields = ('user__username',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'trail', 'comment', 'likes')
    search_fields = ('user__user__username', 'trail__title')
    list_filter = ('trail',)

@admin.register(TrailLike)
class TrailLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'trail')
    search_fields = ('user__user__username', 'trail__title')