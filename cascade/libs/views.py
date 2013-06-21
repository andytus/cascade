__author__ = 'jbennett'

from cascade.libs.forms import RegisterUsersForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

def register_user(request):
    args = {}
    if request.method == 'POST':
        form = RegisterUsersForm(request.POST)
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



