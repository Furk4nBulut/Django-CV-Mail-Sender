# cv_app/models.py
from django.db import models

class CV(models.Model):
    email = models.EmailField()
    file_name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
# models.py

from django.db import models

class EmailSettings(models.Model):
    email_host = models.CharField(max_length=100)
    email_port = models.IntegerField()
    email_host_user = models.EmailField()
    email_host_password = models.CharField(max_length=100)
    email_use_tls = models.BooleanField()

    def __str__(self):
        return self.email_host_user
