from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='user_login')
def account(request):
    return render(request, 'index.html')