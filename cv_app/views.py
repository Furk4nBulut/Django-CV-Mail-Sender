from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from .forms import EmailForm, EmailSettingsForm
from .models import CV, EmailSettings

from django.urls import reverse

# Diğer importlar...

from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import EmailForm, EmailSettingsForm
from .models import CV, EmailSettings

from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from .forms import EmailForm, EmailSettingsForm
from .models import CV, EmailSettings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from .forms import EmailForm, EmailSettingsForm
from .models import CV, EmailSettings
from django.urls import reverse

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from .forms import EmailForm, EmailSettingsForm
from .models import CV, EmailSettings
from django.urls import reverse

from django.core.exceptions import ObjectDoesNotExist

# Gönderme işlemini gerçekleştiren fonksiyon
from django.core.exceptions import ObjectDoesNotExist

# Gönderme işlemini gerçekleştiren fonksiyon
def send_cv(request):
    current_settings = EmailSettings.objects.all()
    form = EmailSettingsForm()

    if request.method == 'POST':
        # E-posta gönderme formunu kontrol et
        email_form = EmailForm(request.POST)
        if email_form.is_valid():
            email_address = email_form.cleaned_data['email']

            # Seçilen SMTP ayarlarını al
            selected_settings_id = request.POST.get('selected_settings')
            if selected_settings_id:
                email_settings = EmailSettings.objects.get(id=selected_settings_id)
                if not email_settings:
                    messages.error(request, 'SMTP ayarları tanımlanmamış.')
                    return redirect('send_cv')

                # SMTP ayarlarını güncelle
                settings.EMAIL_HOST = email_settings.email_host
                settings.EMAIL_PORT = email_settings.email_port
                settings.EMAIL_HOST_USER = email_settings.email_host_user
                settings.EMAIL_HOST_PASSWORD = email_settings.email_host_password
                settings.EMAIL_USE_TLS = email_settings.email_use_tls

                # E-posta göndermeden önce aynı dosyaların daha önce gönderilip gönderilmediğini kontrol et
                file_names = ['FurkanBulutEN.pdf', 'FurkanBulutTR.pdf']  # Gönderilmek istenen dosya adları
                existing_cv = CV.objects.filter(email=email_address, file_name__in=file_names).exists()
                if existing_cv:
                    messages.error(request, 'Belirtilen e-posta adresine aynı dosyalar daha önce gönderilmiş.')
                    return redirect('send_cv')

                # E-posta oluşturma ve gönderme işlemi
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

                    # CV bilgilerini veritabanına kaydet
                    cv = CV.objects.create(email=email_address, file_name=file_names)  # Dosya adını düzenle
                    cv.save()

                except Exception as e:
                    messages.error(request, f'E-posta gönderirken bir hata oluştu: {str(e)}')
            else:
                messages.error(request, 'SMTP ayarlarını seçin.')

            return redirect(reverse('send_cv'))

        else:
            messages.error(request, 'Lütfen geçerli bir e-posta adresi girin.')
    else:
        email_form = EmailForm()
        messages.error(request, 'CV gönderme işlemi başarısız oldu.')

    cvs = CV.objects.all()

    return render(request, 'cv_app/send_cv.html',
                  {'email_form': email_form, 'cvs': cvs, 'form': form, 'settings': current_settings})

def email_settings(request):
    current_settings = EmailSettings.objects.all()

    if request.method == 'POST':
        form = EmailSettingsForm(request.POST)
        if form.is_valid():
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
