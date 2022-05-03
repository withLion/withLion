from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = 'likelion'
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            user = User.objects.create_user(
                username = username,
                password = password,
            )
            user.save()
            user = auth.authenticate(request, username=username, password=password)
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
            #함수 빼내서 좀더 예쁘게 바꿀것
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')
