from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def signup(request):
    # need to determine if form is sending GET or POST
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error':'Username has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                login(request, user) # logs in the user
                return render(request, 'posts/home.html')
        else:
            return render(request, 'accounts/signup.html', {'error':'Passwords didn\'t match'})
    else:
        return render(request, 'accounts/signup.html')

def loginview(request):
    # need to determine if form is sending GET or POST
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            # Redirect to a success page.
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'accounts/login.html', {'error':'Username and Passwords didn\'t match'})

    else:
        return render(request, 'accounts/login.html')


def logoutview(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
