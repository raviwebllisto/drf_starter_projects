from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(OTPVerification)
admin.site.register(Friend)
admin.site.register(PersonalChat)
admin.site.register(Employee)