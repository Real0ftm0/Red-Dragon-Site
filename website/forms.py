from django import forms
from website.models import Contact
from allauth.account.forms import SignupForm, LoginForm
from django import forms
from allauth.account.forms import SignupForm


class ContactForm(forms.ModelForm):

    class Meta: 
        model = Contact
        fields = ['name', 'email', 'message']
        #'__all__' - #['name','email'] - #exclude = ['name']

