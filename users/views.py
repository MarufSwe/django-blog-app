from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST) #default fields, without email
        form = UserRegisterForm(request.POST) #custome class with email field
        if form.is_valid():
            # form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can login now!!')
            return redirect('login')
    else:
        # form  = UserCreationForm()
        form  = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



@login_required() #Decorator for access profile url
def profile(request):
    if request.method == 'POST': #check POST method
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid(): #check validate
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)