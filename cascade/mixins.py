from cascade.settings import LOGIN_URL
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginSiteRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            #attempts to get the site from the users profile, if not found exception gives access denied
            site_access = User.objects.get(pk=request.user.id).useraccountprofile.sites.get(id=get_current_site(request).id)
        except:
            return HttpResponseForbidden()

        return super(LoginSiteRequiredMixin, self).dispatch(request, *args, **kwargs)


