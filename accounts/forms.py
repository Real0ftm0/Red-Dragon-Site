from django import forms
from accounts.models import CustomUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username',
                  'email', 'home_address')