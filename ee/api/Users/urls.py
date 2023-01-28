from django.urls import path
from .views import Register, ProfileContent

urlpatterns = [
    path('register/', Register.as_view()),
    path('profile/<int:pk>/', ProfileContent.as_view()),
]