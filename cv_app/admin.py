from django.contrib import admin
from .models import CV

# Register your models here.
@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    pass

from .models import EmailSettings
@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    pass