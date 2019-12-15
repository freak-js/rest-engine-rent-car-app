from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from .models import User, Car
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import UserSerializer, UserListSerializer, UserCarsSerializer, CarSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)


class UserChangeView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdminUser, IsAuthenticated)


class UserCarsView(generics.RetrieveAPIView):
    serializer_class = UserCarsSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdminUser, IsAuthenticated)


class CarRentChangeView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    permission_classes = (IsAdminUser, IsAuthenticated)


def index(request):
    if request.method == 'POST':
        if User.user_login(request):
            return redirect('welcome')
        return redirect('login')

    form = CustomAuthenticationForm
    return render(request, 'cars_rent_app/index.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('welcome')
    else:
        form = CustomUserCreationForm
    return render(request, 'cars_rent_app/registration.html', {'form': form})


@login_required
def welcome(request):
    superuser = request.user.is_superuser
    user = request.user
    cars_list = Car.get_cars(user)
    user_cars = Car.get_cars(user, get_my_cars=True)

    if superuser:
        user_list = User.objects.filter(is_staff=False)

    return render(request, 'cars_rent_app/welcome.html', {
        'superuser': superuser,
        'cars_list': cars_list,
        'user_cars': user_cars,
        'user_list': user_list if superuser else None,
        'user': user if not superuser else None
    })


@login_required
def rent_car(request):
    user = request.user
    try:
        car_pk = request.POST.get('car')
    except KeyError:
        return redirect('welcome')

    try:
        car = Car.objects.get(pk=car_pk)
    except Car.DoesNotExist:
        return redirect('welcome')

    car.rent_car(user)
    return redirect('welcome')


@login_required
def return_car(request):
    user = request.user
    try:
        car_pk = request.POST.get('car')
    except KeyError:
        return redirect('welcome')

    try:
        car = Car.objects.get(pk=car_pk)
    except Car.DoesNotExist:
        return redirect('welcome')

    car.return_car(user)
    return redirect('welcome')


def logout_view(request):
    logout(request)
    return redirect('login')
