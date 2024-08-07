from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Profile


class Settingform(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Settingform, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        #self.fields['username'].required = True
        #self.fields['username'].help_text = '<small id="emailHelp" class="form-text text-muted">Required. 150 characters or fewer. Letters, digits and ./+/-/_ only.</small>'
        self.fields['first_name'].widget = forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
        self.fields['last_name'].widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
        '''
        self.fields['username'].widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
        '''
    class Meta:
        model = User
        #fields = ('username', 'first_name', 'last_name',)
        fields = ('first_name', 'last_name')

class Settingform1(forms.ModelForm):
    online_now = forms.BooleanField(required=False)
    def __init__(self, *args, **kwargs):
        super(Settingform1, self).__init__(*args, **kwargs)
        self.fields['bio'].widget = forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    class Meta:
        model = Profile
        #fields = ('username', 'first_name', 'last_name',)
        fields = ('bio', 'avatar','online_now')

################################################################################

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control'
                }
            )
        self.fields['username'].widget = forms.TextInput(
            attrs={
                'class': 'form-control'
                }
            )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control'
                }
            )
        self.fields['password1'].required = True
        self.fields['password2'].required = True
    email = forms.EmailField(max_length=200, help_text='Required', required=True, widget=forms.TextInput(
            attrs={
                'class': 'form-control'
                }
            ))
    first_name = forms.CharField(max_length=30, help_text='Required', required=True, widget=forms.TextInput(
            attrs={
                'class': 'form-control'
                }
            ))
    last_name = forms.CharField(max_length=30, help_text='Required', required=True, widget=forms.TextInput(
            attrs={
                'class': 'form-control'
                }
            ))
    number = forms.IntegerField( max_value=99999999999999999999,required=False, widget=forms.TextInput(
            attrs={
                'type':'tel',
                'pattern':'[0-9]{10}',
                'class': 'form-control'
                }
            ))

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        data = data.capitalize()
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        data = data.capitalize()
        return data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

############################################################################################

class ChangeUsernameform(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChangeUsernameform, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['username'].help_text = '<small id="emailHelp" class="form-text text-muted">Required. 150 characters or fewer. Letters, digits and ./+/-/_ only.</small>'

        self.fields['username'].widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
        
    class Meta:
        model = User
        fields = ('username',)

class ChangePasswordform(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordform, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )
        self.fields['new_password1'].widget = forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )
        self.fields['new_password2'].widget = forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )
    
    class Meta:
        model = User
        fields= ('old_password', 'new_password1', 'new_password2')

class ResetPasswordform(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )
    class Meta:
        model = User
        fields= ('email')

class SetPasswordConfirm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget = forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )
        self.fields['new_password2'].widget = forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )
    class Meta:
        model = User
        fields= ('new_password1', 'new_password2')
