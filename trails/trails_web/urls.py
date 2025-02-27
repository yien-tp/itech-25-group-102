# from django.urls import path
# from trails_web import views

# app_name = "trails_web"

# urlpatterns = [
#     path("", views.index, name="index"),
# ]
from django.urls import path
from .views import home, category_trails, trail_detail, add_review, like_trail, user_profile, update_profile

app_name = "trails_web"

urlpatterns = [
    path('', home, name='home'),
    path('category/<slug:category_slug>/', category_trails, name='category_trails'),
    path('trail/<int:trail_id>/', trail_detail, name='trail_detail'),
    path('trail/<int:trail_id>/add_review/', add_review, name='add_review'),
    path('trail/<int:trail_id>/like/', like_trail, name='like_trail'),
    path('user/<str:username>/', user_profile, name='user_profile'),
    path('user/<str:username>/update/', update_profile, name='update_profile'),
    path('trail/<int:trail_id>/like/', like_trail, name='like_trail'),
    path('trail/<int:trail_id>/add_review/', add_review, name='add_review'),
]