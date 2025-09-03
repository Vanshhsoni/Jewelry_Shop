from django.urls import path
from . import views

app_name = "core"   # 👈 this prevents NoReverseMatch

urlpatterns = [
    path("", views.landing_page, name="landing"),
    path("profile/", views.profile_page, name="profile"),
    path("profile/update/", views.update_profile_field, name="update_profile_field"),
]
