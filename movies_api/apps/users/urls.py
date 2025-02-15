from django.urls import path

from movies_api.apps.users import views

urlpatterns = [
    path("register/", views.CreateUserView.as_view(), name="register_user"),
]
