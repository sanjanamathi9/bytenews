from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from news.models import Category, UserPreference

# Registration form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Preferences form
class UserPreferenceForm(forms.ModelForm):
    preferred_categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = UserPreference
        fields = ['preferred_categories']
