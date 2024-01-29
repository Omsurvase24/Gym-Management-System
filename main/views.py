from django.shortcuts import render
from . import models
from . import forms
# Create your views here.

# Home


def home(request):
    banners = models.Banners.objects.all()
    services = models.Service.objects.all()[:3]
    return render(request, 'home.html', {'banners': banners, 'services': services})


def page_detail(request, id):
    page = models.Page.objects.get(id=id)
    return render(request, 'page.html', {'page': page})


def faq_list(request):
    faq = models.Faq.objects.all()
    return render(request, 'faq.html', {'faqs': faq})


def enquiry(request):
    msg = ''
    if request.method == 'POST':
        form = forms.EnquiryForm(request.POST)
        if form.is_valid:
            form.save()
            msg = 'Data has been saved'
    form = forms.EnquiryForm
    return render(request, 'enquiry.html', {'form': form, 'msg': msg})
