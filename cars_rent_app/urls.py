from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views as drf_views
from .views import UserCreateView, UserListView, UserChangeView, UserCarsView, CarRentChangeView

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='cars_rent_app/index.html',
                                                redirect_authenticated_user=True), name="login"),
    path('registration/', views.registration, name='registration'),
    path('welcome/', views.welcome, name='welcome'),
    path('login/', auth_views.LoginView.as_view(template_name='cars_rent_app/index.html',
                                                redirect_authenticated_user=True), name="login"),
    path('logout/', views.logout_view, name='logout_view'),
    path('rent_car/', views.rent_car, name='rent_car'),
    path('return_car/', views.return_car, name='return_car'),
    path('api/v1/cars_rent_app/user/create', UserCreateView.as_view()),
    path('api/v1/cars_rent_app/users/all', UserListView.as_view()),
    path('api/v1/cars_rent_app/user/change/<int:pk>', UserChangeView.as_view()),
    path('api/v1/cars_rent_app/user/cars/<int:pk>', UserCarsView.as_view()),
    path('api/v1/cars_rent_app/car/change/<int:pk>', CarRentChangeView.as_view()),
    path('api/v1/cars_rent_app/user/get_token/',  drf_views.obtain_auth_token)
]
