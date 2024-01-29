from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('pagedetail/<int:id>', views.page_detail, name='pagedetail'),
    path('faq', views.faq_list, name='faq'),
    path('enquiry', views.enquiry, name='enquiry'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
