from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate, login
import json
from django.core.mail import send_mail
from rent.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from django.dispatch import receiver
from django.db.models.signals import pre_save


class Language(models.Model):
    language = models.CharField('User language', max_length=3)

    def __str__(self):
        return self.language


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email', max_length=100, unique=True)
    language = models.ForeignKey(
        Language, models.SET_NULL, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.email

    def get_user_cars(self):
        return self.cars.all()

    @staticmethod
    def user_login(request):
        try:
            email = request.POST['email']
            password = request.POST['password']
        except KeyError:
            return False

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return True
        return False


class Car(models.Model):
    name = models.TextField('Название автомобиля', default='{"eng": "", "rus": ""}')
    year_of_issue = models.DateField('Дата выпуска')
    add_date = models.DateField('Дата добавления', auto_now_add=True)
    status = models.BooleanField('Машина занята?', default=False)
    renter = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name='cars')

    def __str__(self):
        try:
            name = json.loads(self.name)['eng']
        except KeyError:
            name = json.loads(self.name)['rus']
        return name

    def rent_car(self, user_object):
        self.renter = user_object
        self.save()

    def return_car(self, user_object):
        self.renter = None
        self.status = False
        self.save()

    def car_name(self):

        if not self.renter:
            return json.loads(self.name)['eng']
        else:
            renter_id = self.renter.pk

            if renter_id:
                renter = User.objects.get(pk=renter_id)
                renter_lang = renter.language

                try:
                    car_name = json.loads(self.name)[f'{renter_lang}']
                except KeyError:
                    return json.loads(self.name)['eng']
                return car_name

    @staticmethod
    def get_cars(user_object, get_my_cars=False):
        user_lang = user_object.language

        if get_my_cars:
            cars = user_object.get_user_cars()
        else:
            cars = Car.objects.all()

        cars_list = list()

        for car in cars:
            try:
                car_name = json.loads(car.name)[f'{user_lang}']
            except KeyError:
                car_name = json.loads(car.name)['eng']
            car.name = car_name
            car.year_of_issue = car.year_of_issue.strftime("%Y")
            cars_list.append(car)

        return cars_list


'''
Check change rent field in Car class object
'''
@receiver(pre_save, sender=Car)
def sand_email_renter(sender, **kwargs):
    car = kwargs.get('instance')

    if car.renter:
        old_renter_id = Car.objects.get(pk=car.pk).renter
        renter = User.objects.get(pk=car.renter.pk)

        if old_renter_id is None:
            car.status = True
            send_mail(
                'Тема',
                'Шаблон письма',
                EMAIL_HOST_USER,
                [renter.email],
                fail_silently=False
            )
    elif car.renter is None:
        car.status = False