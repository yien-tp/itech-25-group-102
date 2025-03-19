from django.urls import path
from .views import home, category_trails, trail_detail, add_review, like_trail, user_profile, update_profile, update_favorite_trail, category_list, add_trail_to_category, edit_trail, like_review, search


app_name = "trails_web"

urlpatterns = [
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('categories/', category_list, name='category_list'),
    path('category/<slug:category_slug>/', category_trails, name='category_trails'),
    path('category/<slug:category_slug>/add_trail/', add_trail_to_category, name='add_trail_to_category'),
    path('trail/<int:trail_id>/', trail_detail, name='trail_detail'),
    path('trail/<int:trail_id>/edit/', edit_trail, name='edit_trail'),
    path('trail/<int:trail_id>/add_review/', add_review, name='add_review'),
    path('trail/<int:trail_id>/like/', like_trail, name='like_trail'),
    path('user/<str:username>/', user_profile, name='user_profile'),
    path('user/<str:username>/update/', update_profile, name='update_profile'),
    path('user/<str:username>/update_favorite/', update_favorite_trail, name='update_favorite_trail'),
    path('trail/<int:trail_id>/like/', like_trail, name='like_trail'),
    path('trail/<int:trail_id>/add_review/', add_review, name='add_review'),
    path('review/<int:review_id>/like/', like_review, name='like_review'),
    
]