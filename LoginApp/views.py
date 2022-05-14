from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = 'likelion'
        user = auth.authenticate(request, username=username, password=password)
        
        if user is None: 
          User.objects.create_user(
                username = username,
                password = password,
            )
          user = auth.authenticate(request, username=username, password=password)
    
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
      
        if 'next' in request.POST: #login이후에 리다이렉트가 된다면 next로 받는다(login.html에 <input type="hidden"> 참고)
          return redirect(request.POST['next'])
        return redirect('home')

    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')
