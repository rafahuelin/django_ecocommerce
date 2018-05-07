from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.views.generic import UpdateView, View
from django.shortcuts import render, redirect

from .forms import MarketingPreferenceForm
from .mixins import CsrfExemptMixin
from .models import MarketingPreference
from .utils import Mailchimp

MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)


class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'base/forms.html'
    success_url = '/settings/email/'
    success_message = "Your email preferences have been updated. Thank you."

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect("/login/?next=/settings/email/")  # HttpResponse("Not allowed", status=400)
        return super(MarketingPreferenceUpdateView, self).dispatch(request,*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Email Preferences'
        return context

    def get_object(self, queryset=None):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj


"""
POST /inspect/01ccxw6a93j0nznha35cv6zxqy HTTP/1.1
requestinspector.com
User-Agent: MailChimp.com
Accept: */*
Content-Type: application/x-www-form-urlencoded
Content-Length: 403
Accept-Encoding: gzip

POST METHOD

type=subscribe&
fired_at=2018-05-07 18:08:03&
data[id]=f218150ce6&
data[email]=msi@msi.com&
data[email_type]=html&
data[ip_opt]=2.154.209.21&
data[web_id]=6193231&
data[merges][EMAIL]=msi@msi.com&
data[merges][FNAME]=&
data[merges][LNAME]=&
data[merges][ADDRESS]=&
data[merges][PHONE]=&
data[merges][BIRTHDAY]=&
data[list_id]=52770f0a07

"""


class MailchimpWebhookView(CsrfExemptMixin, View):  # HTTP GET -- def get()
    # def get(self, request, *args, **kwargs):
    #     return HttpResponse("Thank you", status=200)

    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            hook_type = data.get('type')
            email = data.get('data[email]')
            response_status, response = Mailchimp().check_subscription_status(email)
            sub_status = response['status']
            is_subbed = None
            mailchimp_subbed = None
            if sub_status == 'subscribed':
                is_subbed, mailchimp_subbed = (True, True)
            elif sub_status == 'unsubscribed':
                is_subbed, mailchimp_subbed = (False, False)
            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(subscribed=is_subbed, mailchimp_subscribed=mailchimp_subbed, mailchimp_msg=str(data))
        return HttpResponse("Thank you", status=200)


# def mailchimp_webhook_view(request):
#     data = request.POST
#     list_id = data.get('data[list_id]')
#     if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
#         hook_type = data.get('type')
#         email = data.get('data[email]')
#         response_status, response = Mailchimp().check_subscription_status(email)
#         sub_status = response['status']
#         is_subbed = None
#         mailchimp_subbed = None
#         if sub_status == 'subscribed':
#             is_subbed, mailchimp_subbed = (True, True)
#         elif sub_status == 'unsubscribed':
#             is_subbed, mailchimp_subbed = (False, False)
#         if is_subbed is not None and mailchimp_subbed is not None:
#             qs = MarketingPreference.objects.filter(user__email__iexact=email)
#             if qs.exists():
#                 qs.update(subscribed=is_subbed, mailchimp_subscribed=mailchimp_subbed, mailchimp_msg=str(data))
#     return HttpResponse("Thank you", status=200)
