# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from .forms import EmailForm, EmailSettingsForm
from .models import CV, EmailSettings

def send_cv(request):
    current_settings = EmailSettings.objects.all()
    form = EmailSettingsForm()

    if request.method == 'POST':
        email_form = EmailForm(request.POST)
        if email_form.is_valid():
            email_address = email_form.cleaned_data['email']

            email_settings = EmailSettings.objects.first()
            if not email_settings:
                messages.error(request, 'SMTP ayarları tanımlanmamış.')
                return redirect('send_cv')

            email = EmailMessage()
            email.subject = 'Furkan Bulut CV'
            email.body = 'Merhaba, CV ekte bulunmaktadır.'
            email.from_email = email_settings.email_host_user
            email.to = [email_address]
            email.attach_file('FurkanBulutEN.pdf')
            email.attach_file('FurkanBulutTR.pdf')

            try:
                email.send()
                messages.success(request, 'CV başarıyla gönderildi.')
            except Exception as e:
                messages.error(request, f'E-posta gönderirken bir hata oluştu: {str(e)}')

            return redirect('send_cv')

        else:
            messages.error(request, 'Lütfen geçerli bir e-posta adresi girin.')
    else:
        email_form = EmailForm()
        messages.error(request, 'CV gönderme işlemi başarısız oldu.')

    cvs = CV.objects.all()

    return render(request, 'cv_app/send_cv.html', {'email_form': email_form, 'cvs': cvs, 'form': form, 'settings': current_settings})


def email_settings(request):
    current_settings = EmailSettings.objects.all()

    if request.method == 'POST':
        form = EmailSettingsForm(request.POST)
        if form.is_valid():
            # Mevcut ayarları kontrol et
            existing_settings = EmailSettings.objects.first()
            if existing_settings:
                messages.error(request, 'SMTP ayarları zaten kaydedilmiş. Yalnızca güncelleme yapabilirsiniz.')
                return redirect('send_cv')

            form.save()
            messages.success(request, 'SMTP ayarları başarıyla kaydedildi.')
            return redirect('send_cv')
        else:
            messages.error(request, 'Formda geçersiz veri var. Lütfen tekrar deneyin.')
    else:
        form = EmailSettingsForm()
        messages.error(request, 'SMTP ayarları kaydedilemedi.')

    return render(request, 'cv_app/send_cv.html', {'form': form, 'settings': current_settings})
