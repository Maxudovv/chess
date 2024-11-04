from django.urls import path

from app.api.user.views.login_view import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]
