# cv_app/forms.py

from django import forms
from .models import CV

class EmailForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['email']

# cv_app/forms.py

from django import forms

# forms.py
# forms.py

from django import forms
from .models import EmailSettings

class EmailSettingsForm(forms.ModelForm):
    class Meta:
        model = EmailSettings
        fields = ['email_host', 'email_port', 'email_host_user', 'email_host_password', 'email_use_tls']
