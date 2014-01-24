__author__ = 'jbennett'
from rest_framework import serializers
from cascade.apps.accounts.models import Profile
from django.contrib.sites.models import Site


class ProfileSerializer(serializers.ModelSerializer):
    sites = serializers.SlugRelatedField(source='sites', read_only=True, many=True, slug_field='domain')
    username = serializers.SlugRelatedField(source='user', read_only=True, slug_field='username')
    class Meta:
        model = Profile
        fields = ('username', 'sites', 'company', 'mugshot')



