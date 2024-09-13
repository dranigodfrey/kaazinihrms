from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django import forms

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['email', 'username', 'sex', 'first_name', 'second_name', 'user_role']
        exclude = ['password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'email@company.com'}),
            'username': forms.TextInput(attrs={'placeholder': 'username' }),
            'sex': forms.RadioSelect(),
            'user_role':forms.RadioSelect
        }
        # Explicitly exclude password fields
        
   
    def save(self, commit=True):
        user = super().save(commit=False)
        # Generate a random password
        password = User.objects.make_random_password()
        user.set_password(password)
        if commit:
            user.save()
        # Return both the user and the password
        return user, password
    

class AdminUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'username', 'sex', 'first_name', 'second_name', 'user_role']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class UserGroupForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User")
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple, label="Select Groups")

class EditUserForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Groups"
    )
    class Meta:
        model = User
        # fields = '__all__' # ['username', 'email', 'first_name', 'second_name', 'groups']
        fields = ['username', 'email', 'first_name', 'middle_name', 'second_name', 'sex', 'user_role','groups', 'is_active']