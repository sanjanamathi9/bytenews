from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserPreferenceForm
from news.models import UserPreference

# Register view
def user_preferences(request):
    preference, created = UserPreference.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            return redirect('article_list')  # or wherever you want to go after saving
    else:
        form = UserPreferenceForm(instance=preference)

    return render(request, 'users/preferences.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# Preferences view
@login_required
def set_preferences(request):
    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=request.user.userpreference)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to homepage or any view
    else:
        form = UserPreferenceForm(instance=request.user.userpreference)

    return render(request, 'users/preferences_form.html', {'form': form})


@login_required
def preferences(request):
    user_preference, created = UserPreference.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=user_preference)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your preferences have been updated!')
            return redirect('users:preferences')  # <-- FIXED
    else:
        form = UserPreferenceForm(instance=user_preference)

    return render(request, 'users/preferences.html', {'form': form})