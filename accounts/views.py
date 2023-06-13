from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.views.generic import FormView, View
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string, RANDOM_STRING_CHARS

from random import randint
from accounts.models import EmailConfirmation
from accounts.forms import ProfileForm



def login_view(request):
    print("Gorbe0")
    if not request.user.is_authenticated:
        print("Gorbe10")
        if request.method == 'POST':
            form = AuthenticationForm(request=request,data=request.POST)
            print("Gorbe20")
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request,user)
                    print("Gorbe30")
                    return redirect('/')

        form = AuthenticationForm()
        context = {'form':form}
        print("Gorbe40")
        return render(request,'account/login.html',context)
    else:
        return redirect('/')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            User = get_user_model()

            if not User.objects.filter(username=username).exists():
                random_code = randint(10000, 99999)
                token = get_random_string(length=30)

                subject = 'رستوران اژدهای سرخ'
                message = f"""
                        سلام {username} عزیز، به رستوران اژدهای سرخ خوش آمدید.
                        برای ورود کد تایید {random_code} وارد کنید.
                        """
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email,]
                send_mail( subject, message, email_from, recipient_list )

                EmailConfirmation.objects.create(email=email, code=random_code, token=token, password=password, username=username)

                return redirect(reverse('confirm_email') + f'?token={token}')
        
            return redirect('/') 
        
        
        return render(request,'account/login.html')
    else:
        return redirect('/')
    
    
class ConfirmEmail(View):
    template_name = 'account/confirm.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, self.template_name)
    
    def post(self, request):
        code = request.POST.get('confirm-code')
        token = request.GET.get('token')
        email_conf = EmailConfirmation.objects.get(token=token)
        User = get_user_model()
        if EmailConfirmation.objects.filter(code=code, token=token).exists():
            user = User.objects.create_user(username=email_conf.username , email=email_conf.email, password=email_conf.password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
        return redirect('login')
    
        return render(request, self.template_name)

class EditProfileView(FormView):
    template_name = 'account/profile.html'
    form_class = ProfileForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated != True:
            return redirect('website:index')
        user = request.user
        form = self.form_class(instance=user)
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('website:index')
        return render(request, self.template_name, context={'form': form})