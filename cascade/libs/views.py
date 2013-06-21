__author__ = 'jbennett'

from cascade.libs.forms import RegisterUsersForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.core.mail import mail_admins, send_mail

def register_user(request):
    args = {}
    if request.method == 'POST':
        form = RegisterUsersForm(request.POST)
        username = request.POST.get('username', 'unknown')
        test=  mail_admins('New user: %s needs activation!' % username, "Activate %s please!" % username, fail_silently=False)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('success/')
    else:
        form = RegisterUsersForm()
    args.update(csrf(request))
    args['form'] = form

    return render_to_response("registration/registration_form.html", args, context_instance=RequestContext(request))

def register_success(request):
    return render_to_response("registration/registration_success.html", context_instance=RequestContext(request))



