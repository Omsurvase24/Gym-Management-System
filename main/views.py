from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Count
from . import models
from . import forms
import stripe
from django.core.mail import EmailMessage

from datetime import timedelta
# Create your views here.

# Home


def home(request):
    banners = models.Banners.objects.all()
    services = models.Service.objects.all()[:3]
    gimgs = models.GalleryImage.objects.all().order_by('-id')[:9]
    return render(request, 'home.html', {'banners': banners, 'services': services, 'gimgs': gimgs})


def page_detail(request, id):
    page = models.Page.objects.get(id=id)
    return render(request, 'page.html', {'page': page})


def faq_list(request):
    faq = models.Faq.objects.all()
    return render(request, 'faq.html', {'faqs': faq})


def contact_page(request):
    return render(request, 'contact_us.html')


def enquiry(request):
    msg = ''
    if request.method == 'POST':
        form = forms.EnquiryForm(request.POST)
        if form.is_valid:
            form.save()
            msg = 'Data has been saved'
    form = forms.EnquiryForm
    return render(request, 'enquiry.html', {'form': form, 'msg': msg})


def gallery(request):
    gallery = models.Gallery.objects.all().order_by('-id')
    return render(request, 'gallery.html', {'gallerys': gallery})


def gallery_detail(request, id):
    gallery = models.Gallery.objects.get(id=id)
    gallery_imgs = models.GalleryImage.objects.filter(
        gallery=gallery).order_by('-id')
    return render(request, 'gallery_imgs.html', {'gallery_imgs': gallery_imgs, 'gallery': gallery})


def pricing(request):
    pricing = models.SubPlan.objects.annotate(
        total_members=Count('subscription__id')).all().order_by('price')
    distinct_features = models.SubPlanFeature.objects.all()
    return render(request, 'pricing.html', {'plans': pricing, 'distinct_features': distinct_features})


def signup(request):
    msg = ''
    if request.method == 'POST':
        form = forms.SignUp(request.POST)
        if form.is_valid():
            form.save()
            msg = 'Thank you for registration.'
    form = forms.SignUp
    return render(request, 'registration/signup.html', {'form': form, 'msg': msg})


def checkout(request, plan_id):
    planDetail = models.SubPlan.objects.get(pk=plan_id)
    return render(request, 'checkout.html', {'plan': planDetail})


stripe.api_key = 'sk_test_51OgWWoSHp53uEV6C5jqZxeFmicfqeVjGm1I9OBhILRWxJDuP1YHv4x6jad2RWzYOYUgnK8hMRLaTE2Yegz6XNdzD00dmnfB4lH'


def checkout_session(request, plan_id):
    plan = models.SubPlan.objects.get(pk=plan_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': plan.title,
                },
                'unit_amount': plan.price*100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/pay_success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://127.0.0.1:8000/pay_cancel',
        client_reference_id=plan_id
    )
    return redirect(session.url, code=303)


def pay_success(request):
    session = stripe.checkout.Session.retrieve(request.GET['session_id'])
    plan_id = session.client_reference_id
    plan = models.SubPlan.objects.get(pk=plan_id)
    user = request.user
    models.Subscription.objects.create(
        plan=plan,
        user=user,
        price=plan.price
    )
    subject = 'Order Email'
    html_content = get_template(
        'orderemail.html').render({'title': plan.title})
    from_email = 'omsurvase24@gmail.com'
    msg = EmailMessage(subject, html_content, from_email, ['mikka@gmail.com'])
    msg.content_subtype = "html"
    msg.send()

    return render(request, 'success.html')


def pay_cancel(request):
    return render(request, 'cancel.html')


def user_dashboard(request):
    current_plan = models.Subscription.objects.get(user=request.user)
    my_trainer = models.AssignSubscriber.objects.get(user=request.user)
    enddate = current_plan.reg_date + \
        timedelta(days=current_plan.plan.validity_days)

    data = models.Notify.objects.all().order_by('-id')
    notifyStatus = False
    jsonData = []
    totalUnread = 0
    for d in data:
        try:
            notifyStatusData = models.NotifyUserStatus.objects.get(
                user=request.user, notify=d)
            if notifyStatusData:
                notifyStatus = True
        except models.NotifyUserStatus.DoesNotExist:
            notifyStatus = False
        if not notifyStatus:
            totalUnread = totalUnread+1

    return render(request, 'user/dashboard.html', {
        'current_plan': current_plan,
        'my_trainer': my_trainer,
        'total_unread': totalUnread,
        'enddate': enddate,
    })


def update_profile(request):
    msg = None
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            msg = 'Data has been saved'
    form = forms.ProfileForm(instance=request.user)
    return render(request, 'user/update-profile.html', {'form': form, 'msg': msg})


def trainerlogin(request):
    msg = ''
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['pwd']
        trainer = models.Trainer.objects.filter(
            username=username, pwd=pwd).count()
        if trainer > 0:
            trainer = models.Trainer.objects.filter(
                username=username, pwd=pwd).first()
            request.session['trainerLogin'] = True
            request.session['trainerid'] = trainer.id
            return redirect('/trainer_dashboard')
        else:
            msg = 'Invalid!!'
    form = forms.TrainerLoginForm
    return render(request, 'trainer/login.html', {'form': form, 'msg': msg})


def trainerlogout(request):
    del request.session['trainerLogin']
    return redirect('/trainerlogin')


def trainer_dashboard(request):
    return render(request, 'trainer/dashboard.html')


def trainer_profile(request):
    t_id = request.session['trainerid']
    trainer = models.Trainer.objects.get(pk=t_id)
    msg = None
    if request.method == 'POST':
        form = forms.TrainerProfileForm(
            request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            form.save()
            msg = 'Profile has been updated'
    form = forms.TrainerProfileForm(instance=trainer)
    return render(request, 'trainer/profile.html', {'form': form, 'msg': msg})


def notify(request):
    data = models.Notify.objects.all().order_by('-id')
    return render(request, 'notify.html', {'data': data})


def get_notify(request):
    data = models.Notify.objects.all().order_by('-id')
    notifyStatus = False
    jsonData = []
    totalUnread = 0
    for d in data:
        try:
            notifyStatusData = models.NotifyUserStatus.objects.get(
                user=request.user, notify=d)
            if notifyStatusData:
                notifyStatus = True
        except models.NotifyUserStatus.DoesNotExist:
            notifyStatus = False
        if not notifyStatus:
            totalUnread = totalUnread+1
        jsonData.append({
            'pk': d.id,
            'notify_detail': d.notify_detail,
            'notifyStatus': notifyStatus
        })
    # jsonData=serializers.serialize('json', data)
    return JsonResponse({'data': jsonData, 'totalUnread': totalUnread})

# Mark Read by User


def mark_read_notify(request):
    notify = request.GET['notify']
    notify = models.Notify.objects.get(pk=notify)
    user = request.user
    models.NotifyUserStatus.objects.create(
        notify=notify, user=user, status=True)
    return JsonResponse({'bool': True})


def trainer_subscribers(request):
    trainer = models.Trainer.objects.get(pk=request.session['trainerid'])
    trainer_subs = models.AssignSubscriber.objects.filter(
        trainer=trainer).order_by('-id')
    return render(request, 'trainer/trainer_subscribers.html', {'trainer_subs': trainer_subs})


def trainer_payments(request):
    trainer = models.Trainer.objects.get(pk=request.session['trainerid'])
    trainer_pays = models.TrainerSalary.objects.filter(
        trainer=trainer).order_by('-id')
    return render(request, 'trainer/trainer_payments.html', {'trainer_pays': trainer_pays})


def trainer_changepassword(request):
    msg = None
    if request.method == 'POST':
        new_password = request.POST['new_password']
        updateRes = models.Trainer.objects.filter(
            pk=request.session['trainerid']).update(pwd=new_password)
        if updateRes:
            del request.session['trainerLogin']
            return redirect('/trainerlogin')
        else:
            msg = 'Something is wrong!!'
    form = forms.TrainerChangePassword
    return render(request, 'trainer/trainer_changepassword.html', {'form': form})


def trainer_notifs(request):
    data = models.TrainerNotification.objects.all().order_by('-id')
    trainer = models.Trainer.objects.get(id=request.session['trainerid'])
    jsonData = []
    totalUnread = 0
    for d in data:
        try:
            notifStatusData = models.NotifTrainerStatus.objects.get(
                trainer=trainer, notif=d)
            if notifStatusData:
                notifStatus = True
        except models.NotifTrainerStatus.DoesNotExist:
            notifStatus = False
        if not notifStatus:
            totalUnread = totalUnread+1
        jsonData.append({
            'pk': d.id,
            'notify_detail': d.notif_msg,
            'notifStatus': notifStatus
        })
    return render(request, 'trainer/notifs.html', {'notifs': jsonData, 'totalUnread': totalUnread})


def mark_read_trainer_notif(request):
    notif = request.GET['notif']
    notif = models.TrainerNotification.objects.get(pk=notif)
    trainer = models.Trainer.objects.get(id=request.session['trainerid'])
    models.NotifTrainerStatus.objects.create(
        notif=notif, trainer=trainer, status=True)

    # Count Unread
    totalUnread = 0
    data = models.TrainerNotification.objects.all().order_by('-id')
    for d in data:
        try:
            notifStatusData = models.NotifTrainerStatus.objects.get(
                trainer=trainer, notif=d)
            if notifStatusData:
                notifStatus = True
        except models.NotifTrainerStatus.DoesNotExist:
            notifStatus = False
        if not notifStatus:
            totalUnread = totalUnread+1

    return JsonResponse({'bool': True, 'totalUnread': totalUnread})


def trainer_msgs(request):
    data = models.TrainerMsg.objects.all().order_by('-id')
    return render(request, 'trainer/msgs.html', {'msgs': data})


def report_for_user(request):
    trainer = models.Trainer.objects.get(id=request.session['trainerid'])
    msg = ''
    if request.method == 'POST':
        form = forms.ReportForUserForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.report_from_trainer = trainer
            new_form.save()
            msg = 'Data has been saved'
        else:
            msg = 'Invalid Response!!'
    form = forms.ReportForUserForm
    return render(request, 'report_for_user.html', {'form': form, 'msg': msg})


def report_for_trainer(request):
    user = request.user
    msg = ''
    if request.method == 'POST':
        form = forms.ReportForTrainerForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.report_from_user = user
            new_form.save()
            msg = 'Data has been saved'
        else:
            msg = 'Invalid Response!!'
    form = forms.ReportForTrainerForm
    return render(request, 'report_for_trainer.html', {'form': form, 'msg': msg})
