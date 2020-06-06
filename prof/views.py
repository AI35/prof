from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from django.urls import reverse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from prof.forms import Settingform, SignupForm, ChangeUsernameform, ChangePasswordform, ResetPasswordform, SetPasswordConfirm
from prof.tokens import account_activation_token


def base(request):
    return render(request, 'base.html', {})


@login_required
def profile(request, username=''):
    # Need Edit
    if username == '' and request.user.is_authenticated:
        return render(request, 'profile.html',{'u':request.user.username})
    else:
        return render(request, 'profile.html',{'u':username})


###### signin  #######
def signin(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile/')
    elif request.method == 'GET':
        return render(request, 'login.html',{})
    elif request.method == 'POST':
        try:
            e = request.POST['email']
            p = request.POST['password']
            if '@' in e:
                user = User.objects.get(email=e)
            else:
                user = User.objects.get(username=e)
            re = authenticate(username=user.username, password=p)
            if re is not None:
                login(request, re)
                link = '/profile/'+str(re)
                return HttpResponseRedirect(link)
            else:
                return render(request, 'login.html', {'error_msg': 'Wrong Password or User not active'})
        except:
            return render(request, 'login.html', {'error_msg': 'User not found'})

###### signup ##########
'''
def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile/')
    elif request.method == 'GET':
        return render(request, 'signup_backup.html',{})
    elif request.method == 'POST':
        try:
            if '@' in request.POST['username']:
                return render(request, 'signup_backup.html', {'error_msg': 'invaild username'})
            else:
                user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
                print(user)
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.save()
                return render(request, 'base.html',{})
        except Exception as e:
            print(e)
            return render(request, 'signup_backup.html', {'error_msg': 'User is exist'})
'''
######  end signup  #####


@login_required
def Logout(request):
    logout(request)
    return redirect('/login/')


@login_required
def settings(request):
    if request.POST:
        form = Settingform(request.POST)
        #form.fields['usernaem'].value = request.user.username
        #print(request.user.username)
        #print(form.data['username'])
        #print(form.is_valid())
        #if request.user.username == form.data['username']:
        if form.is_valid():
                f = User.objects.get(username=request.user.username)
                form = Settingform(request.POST, instance=f)
                form.save()  # cleaned indenting, but would not save unless I added at least 6 characters.
                return redirect('/profile/')
        else:
            i = form.errors
            f = User.objects.get(username=request.user.username)
            form = Settingform(instance=f)
            return render(request, 'settings.html', {'form': form, 'error_msg': i})
    else:
        f = User.objects.get(username=request.user.username)
        form = Settingform(instance=f)
        return render(request, 'settings.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordform(request.user, request.POST)
        form.fields['old_password'].widget = forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was updated successfully!')
            return redirect('/')
        else:
            return render(request, 'change_password.html', {'form': form, 'error_msg': form.errors})
    else:
        form = ChangePasswordform(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

@login_required
def change_username(request):
    if request.POST:
        form = ChangeUsernameform(request.POST)
        #form.fields['usernaem'].value = request.user.username
        #print(request.user.username)
        #print(form.data['username'])
        #print(form.is_valid())
        if request.user.username == form.data['username']:
            messages.success(request, 'Your username hasn\'t changed!')
            return redirect('/')
        elif form.is_valid():
                f = User.objects.get(username=request.user.username)
                form = ChangeUsernameform(request.POST, instance=f)
                form.save()  # cleaned indenting, but would not save unless I added at least 6 characters.
                messages.success(request, 'Your username was updated successfully!')
                return redirect('/')
        else:
            f = User.objects.get(username=request.user.username)
            form = ChangeUsernameform(instance=f)
            return render(request, 'change_username.html', {'form': form, 'error_msg': form.errors})
    else:
        f = User.objects.get(username=request.user.username)
        form = ChangeUsernameform(instance=f)
        return render(request, 'change_username.html', {'form': form})

####### New Signup ######
def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile/')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email = form.data['email']).exists():
                form.add_error('email', 'Email already exists.')
                return render(request, 'signup.html', {'form': form, 'error_msg':form.errors})
            user = form.save(commit=False)

            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), #.decode()
                'token': account_activation_token.make_token(user),
            })
            # Sending activation link in terminal
            # user.email_user(subject, message)
            mail_subject = 'Activate your account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'confirm.html', {})
            #return HttpResponse('Please confirm your email address to complete the registration.')
            # return render(request, 'acc_active_sent.html')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Thank you for your email confirmation.')
        return redirect('/')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
    
#########    Password Reset Classes   ##########
class PassReset(PasswordResetView):
    form_class = ResetPasswordform

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect('/profile/')
        else:
            return super().dispatch(*args, **kwargs)

class PassResetDone(PasswordResetDoneView):

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        reset_url = str(self.request.META.get('HTTP_REFERER'))[:-1]
        check = str(self.request.build_absolute_uri()).rsplit("/", 2)[0]
        if check != reset_url:
            return HttpResponseRedirect(reverse('base'))
        if self.request.user.is_authenticated:
            return HttpResponseRedirect('/profile/')
        else:
            return super().dispatch(*args, **kwargs)

class PassResetComplete(PasswordResetCompleteView):
    
    def dispatch(self, *args, **kwargs):
        reset_url = str(self.request.META.get('HTTP_REFERER')).rsplit("/", 3)[0]
        check = str(self.request.build_absolute_uri()).rsplit("/", 2)[0]
        if reset_url != check:
        #if 'reset' not in check:
            return HttpResponseRedirect(reverse('base'))
        else:
            return super().dispatch(*args, **kwargs)

class PassResetConfirm(PasswordResetConfirmView):
    form_class = SetPasswordConfirm
