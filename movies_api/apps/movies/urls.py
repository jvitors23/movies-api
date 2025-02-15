from django.urls import (
    path,
)

from movies_api.apps.movies import views

urlpatterns = [
    path("ratings", views.CreateListMovieRatingAPIView.as_view(), name="ratings"),
    path("ratings/<pk>", views.RetrieveUpdateDestroyMovieRatingAPIView.as_view(), name="manage_ratings"),
    path("", views.SearchMoviesAPIView.as_view(), name="search_movies"),
]
