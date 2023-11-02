from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from commit_concatenate.form_table import form_table
from commit_concatenate.models import User
from django.urls import reverse


def show_table(request):
    context = {
        'data': form_table(request.user.github_id),
    }
    return render(request=request, template_name='grid.html', context=context)


def show_home(request):
    context = {
    }
    return render(request=request, template_name='home.html', context=context)










def register(request):
    if request.method == "GET":
        return render(request, "reg.html")
    else:
        data = request.POST
        username = data.get("username")
        password1, password2 = data.get("password1"), data.get("password2")
        github_id = data.get("github_id")
        if github_id is None:
            github_id=None
        if username is None:
            return HttpResponse("<h3><a href=''>Введите имя пользователя</a></h3>")
        elif password1 is None or password2 is None:
            return HttpResponse("<h3><a href=''>Введите пароль</a></h3>")
        elif password1 != password2:
            return HttpResponse("<h3><a href=''>Пароли должны совпадать</a></h3><br>")
        else:
            newuser = User()
            newuser.create_user(username, password1, github_id)
            return HttpResponseRedirect(reverse('index'))


def login_form(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        data = request.POST
        user = authenticate(request, username=data.get('username'), password=data.get('password'))
        if user is None:
            return HttpResponse("<h3><a href=''>Пользователь с таким логином и паролем не найден</a></h3><br>")
        login(request,user)
        return HttpResponseRedirect(reverse('index'))


def logout_form(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
