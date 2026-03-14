from django.urls import path

from .views import dashboard_view, login_view, logout_view

urlpatterns = [
    path('', login_view, name='main-login'),
    path('dashboard/', dashboard_view, name='main-dashboard'),
    path('logout/', logout_view, name='main-logout'),
]
