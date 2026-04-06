from django.urls import path
from .api_views import RegisterApiView, LoginApiView, ProfileApiView
from .views import login_page, signup_page, logout_page

urlpatterns = [
    path('login/', login_page, name='login_page'),
    path('signup/', signup_page, name='signup_page'),
    path('logout/', logout_page, name='logout_page'),
    path('api/register/', RegisterApiView.as_view(), name='api_register'),
    path('api/login/', LoginApiView.as_view(), name='api_login'),
    path('api/profile/', ProfileApiView.as_view(), name='api_profile'),
]
