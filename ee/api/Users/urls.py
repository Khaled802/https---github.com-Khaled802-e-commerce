from django.urls import path
from .views import Register, ImageUploadObject, UserProfileCreation, UserProfileObject\
    , CountryCodes, UserProfileObject2


urlpatterns = [
    path('register/', Register.as_view()),
    path('profile/image_upload/', ImageUploadObject.as_view()),
    path('profile/create/', UserProfileCreation.as_view()),
    path('profile/my/', UserProfileObject.as_view()),
    path('profile/<int:user_id>/', UserProfileObject2.as_view()),
    path('country_code/', CountryCodes.as_view()),
]