from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from .models import Category, Trail, UserProfile, Review, TrailLike
from .forms import ReviewForm, UserProfileForm, TrailForm
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Count


def home(request):
    # Top 5 liked
    top_liked_trails = (Trail.objects.annotate(num_likes=Count('liked_by')).order_by('-num_likes')[:5])

    # Top 5 commented
    top_commented_trails = (Trail.objects.annotate(num_reviews=Count('reviews')).order_by('-num_reviews')[:5])

    # 2 most recent reviews (including trail info)
    recent_reviews = Review.objects.select_related('trail').order_by('-created_at')[:2]

    return render(request, 'trails_web/home.html', {
        'top_liked_trails': top_liked_trails,
        'top_commented_trails': top_commented_trails,
        'recent_reviews': recent_reviews,
    })

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'trails_web/category_list.html', {'categories': categories})

def category_trails(request, category_slug):
    """List trails under a specific category."""
    category = get_object_or_404(Category, slug=category_slug)
    trails = category.trails.all()  # Related name in the model
    return render(request, 'trails_web/category_trails.html', {'category': category, 'trails': trails})

def trail_detail(request, trail_id):
    """Display trail details and user's like status."""
    trail = get_object_or_404(Trail, id=trail_id)
    reviews = trail.reviews.all()

    # Check if the user has liked this trail
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = TrailLike.objects.filter(user=request.user.userprofile, trail=trail).exists()

    return render(request, 'trails_web/trail_detail.html', {
        'trail': trail,
        'reviews': reviews,
        'user_has_liked': user_has_liked
    })

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
    profile = get_object_or_404(UserProfile, user__username=username)

    # Get all categories
    categories = Category.objects.all()

    # Get IDs of the user's favorite trails
    favorite_ids = profile.favorite_trails.values_list('id', flat=True)

    # Build a dict mapping each category to the subset of its trails that are favorited
    cat_favs = {}
    for cat in categories:
        # Filter the category's trails to only those in favorite_ids
        fav_trails = cat.trails.filter(id__in=favorite_ids)
        cat_favs[cat] = fav_trails

    return render(request, 'trails_web/user_profile.html', {
        'profile': profile,
        'cat_favs': cat_favs,
    })


@login_required
def update_profile(request, username):
    """Allow users to update their profile information and password separately."""
    if request.user.username != username:
        return redirect('trails_web:user_profile', username=request.user.username)

    profile = get_object_or_404(UserProfile, user=request.user)
    user = request.user

    profile_form = UserProfileForm(instance=profile, initial={'first_name': user.first_name, 'last_name': user.last_name})
    password_form = PasswordChangeForm(user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:  # Check which form was submitted
            profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                user.first_name = profile_form.cleaned_data['first_name']
                user.last_name = profile_form.cleaned_data['last_name']
                profile.personal_bio = profile_form.cleaned_data['personal_bio']
                user.save()
                profile.save()
                return redirect('trails_web:user_profile', username=request.user.username)

        elif 'change_password' in request.POST:  # Password change form submitted
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Keep user logged in
                return redirect('trails_web:user_profile', username=request.user.username)

    return render(request, 'trails_web/update_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'profile': profile
    })

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


@login_required
def update_favorite_trail(request, username):
    if request.user.username != username:
        return redirect('trails_web:user_profile', username=request.user.username)

    profile = get_object_or_404(UserProfile, user=request.user)
    # Fetch all categories with their related trails (one query)
    categories = Category.objects.prefetch_related('trails').all()

    if request.method == 'POST':
        # Get the list of trail IDs from checkboxes
        selected_trail_ids = request.POST.getlist('favorite_trails')
        # Update the ManyToMany relation
        profile.favorite_trails.set(selected_trail_ids)
        return redirect('trails_web:user_profile', username=request.user.username)

    return render(request, 'trails_web/update_favorite_trail.html', {
        'profile': profile,
        'categories': categories,  # Pass categories to the template
    })

@login_required
def add_trail_to_category(request, category_slug):
    # 1) Get the category or return 404 if not found
    category = get_object_or_404(Category, slug=category_slug)

    if request.method == 'POST':
        form = TrailForm(request.POST)
        if form.is_valid():
            # 2) Create a new trail but don’t commit yet
            new_trail = form.save(commit=False)
            # 3) Assign the category from the URL
            new_trail.category = category
            new_trail.save()
            # 4) Redirect back to the category trails page
            return redirect('trails_web:category_trails', category_slug=category.slug)
    else:
        form = TrailForm()

    return render(request, 'trails_web/add_trail.html', {
        'form': form,
        'category': category,
    })