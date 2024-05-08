from django.contrib import admin
from .models import CV, EmailSettings, EmailTemplate

# Register your models here.
@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    pass

from .models import EmailSettings
@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    pass

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    pass