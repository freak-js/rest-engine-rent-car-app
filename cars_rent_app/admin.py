from django.contrib import admin
from .models import User, Car, Language


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'language')
    fields = ('email', 'first_name', 'language')


class CarAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'year_of_issue', 'add_date', 'status', 'renter')


admin.site.register(User, UserAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Language)
