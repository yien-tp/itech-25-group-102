from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Category, Trail, UserProfile, Review, TrailLike
from .forms import ReviewForm, UserProfileForm


def home(request):
    """Homepage showing trail categories."""
    categories = Category.objects.all()
    return render(request, 'trails_web/home.html', {'categories': categories})

def category_trails(request, category_slug):
    """List trails under a specific category."""
    category = get_object_or_404(Category, slug=category_slug)
    trails = category.trails.all()  # Related name in the model
    return render(request, 'trails_web/category_trails.html', {'category': category, 'trails': trails})

def trail_detail(request, trail_id):
    """Show trail details and reviews."""
    trail = get_object_or_404(Trail, id=trail_id)
    reviews = trail.reviews.all()  # Related name in the model
    return render(request, 'trails_web/trail_detail.html', {'trail': trail, 'reviews': reviews})

@login_required
def add_review(request, trail_id):
    """Allow users to add a review."""
    trail = get_object_or_404(Trail, id=trail_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = UserProfile.objects.get(user=request.user)
            review.trail = trail
            review.save()
            return redirect('trail_detail', trail_id=trail.id)
    else:
        form = ReviewForm()
    return render(request, 'trails_web/add_review.html', {'form': form, 'trail': trail})

@login_required
def like_trail(request, trail_id):
    """Handle trail likes with AJAX."""
    trail = get_object_or_404(Trail, id=trail_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if TrailLike.objects.filter(user=user_profile, trail=trail).exists():
        TrailLike.objects.filter(user=user_profile, trail=trail).delete()
        liked = False
    else:
        TrailLike.objects.create(user=user_profile, trail=trail)
        liked = True

    return JsonResponse({'liked': liked, 'total_likes': trail.liked_by.count()})

@login_required
def user_profile(request, username):
    """Show user profile and their favorite trail."""
    profile = get_object_or_404(UserProfile, user__username=username)
    return render(request, 'trails_web/user_profile.html', {'profile': profile})

@login_required
def update_profile(request, username):
    """Allow users to update their profile."""
    if request.user.username != username:
        return redirect('trails_web:user_profile', username=request.user.username)  # Prevent editing others' profiles

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('trails_web:user_profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'trails_web/update_profile.html', {'form': form, 'profile': profile})

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Trail, UserProfile, TrailLike

@login_required
def like_trail(request, trail_id):
    """Handle trail like/unlike feature with AJAX."""
    trail = get_object_or_404(Trail, id=trail_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Check if the user already liked the trail
    liked = TrailLike.objects.filter(user=user_profile, trail=trail).exists()

    if liked:
        # Unlike the trail
        TrailLike.objects.filter(user=user_profile, trail=trail).delete()
        liked = False
    else:
        # Like the trail
        TrailLike.objects.create(user=user_profile, trail=trail)
        liked = True

    return JsonResponse({'liked': liked, 'total_likes': trail.liked_by.count()})


@login_required
def add_review(request, trail_id):
    """Allow authenticated users to add a review to a trail."""
    trail = get_object_or_404(Trail, id=trail_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = user_profile
            review.trail = trail
            review.save()
            return redirect('trails_web:trail_detail', trail_id=trail.id)
    else:
        form = ReviewForm()

    return render(request, 'trails_web/add_review.html', {'form': form, 'trail': trail})