from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserProfileForm


def home(request):
    count = User.objects.count()
    return render(request, 'home.html', {
        'count': count
    })


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save() # return the object of the usercreation form

            profile = profile_form.save(commit=False) # not save this monment just instantiate it
            profile.user = user
            profile.save()

            return redirect('home')
    else:
        form = UserCreationForm()
        profile_form = UserProfileForm
    return render(request, 'registration/signup.html', {
        'form': form,
        'profile_form':profile_form
    })


@login_required
def secret_page(request):
    return render(request, 'secret_page.html')


# class based secret page view
class SecretPage(LoginRequiredMixin, TemplateView):
    template_name = 'secret_page.html'
