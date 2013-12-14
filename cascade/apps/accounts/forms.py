__author__ = 'jbennett'

from userena.forms import EditProfileForm


class CustomEditProfileForm(EditProfileForm):
    """
    Base field overrides userena defaults for fields that are required

    """
    class Meta(EditProfileForm.Meta):

        exclude = EditProfileForm.Meta.exclude + ['privacy', 'sites']

