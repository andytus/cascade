from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext
from userena.models import UserenaBaseProfile
from django.contrib.sites.managers import CurrentSiteManager


class Profile(UserenaBaseProfile):
    user = models.OneToOneField(User, unique=True, verbose_name=ugettext('user'), related_name='profile')
    sites = models.ManyToManyField(Site)
    company = models.CharField(max_length=50, blank=True)
    objects = models.Manager()
    on_site = CurrentSiteManager()



# class UserAccountProfile(models.Model):
#     user = models.OneToOneField(User)
#     sites = models.ManyToManyField(Site)
#     company = models.CharField(max_length=50, null=True)
#     objects = models.Manager()
#     on_site = CurrentSiteManager()