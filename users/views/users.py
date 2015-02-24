 # -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

@sensitive_post_parameters('password')
def register(request):

    context = {}
    if request.user and request.user.is_authenticated():
        return redirect('/')

    if request.method == 'GET':
        return render(request, 'register.html')

    email = request.POST.get('email')
    nickname = request.POST.get('nickname')
    password = request.POST.get('password')

    user = User()

    if not email:
        context['error'] = 'email missing'
        
    if User.objects.filter(email=email).count() < 1:
        user.username = email
        user.email = email
        user.last_name = nickname
        user.set_password(password)
        user.save()

    else:
        context['error'] = 'exist'


    if 'error' in context:
        return render(request, 'register.html', context)

    else:
        # TODO: send check email
        context['message'] = '註冊確認信已寄至您的信箱'
        return render(request, 'msg.html', context)

@login_required
def profile(request):

    if request.method == 'GET':
        return render(request, 'profile.html')

    user = request.user
    nickname = request.POST['nickname']
    password = request.POST['password']
    user.nickname = nickname

    if password != '':
        user.set_password(password)

    user.save()

    # TODO: add error message
    return render(request, 'profile.html')
