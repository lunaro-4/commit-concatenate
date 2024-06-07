from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from commit_concatenate.form_table import (empty_data, merge_data,
                                           DEFAULT_WEEK_RANGE,
                                           concat_to_weekdays)
from commit_concatenate.models import User
from commit_concatenate import github_parcer
from commit_concatenate import leetcode_parcer
from django.urls import reverse

# from sql_app.sql_models import UserSQL
# from sql_app.database_access import get_db


def show_home(request: HttpRequest) -> HttpResponse:
    context: dict = {}
    # print(request.session)

    return render(request=request, template_name="home.html", context=context)


# async def handle_registration(username : str | None = None,
#                         password1 : str | None = None,
#                         password2 : str | None = None):
#     if not (username and password1 and password2):
#         return
#     if password1 != password2:
#         return
#     new_user = UserSQL(username=username, unhashed_pass= password2)
#     async with settings.DB_SESSION_MANAGER.session() as session:
#         session.add(new_user)
#         await session.commit()
#     return HttpResponseRedirect(reverse('index'))


# async def register(request):
#     if request.method == "GET":
#         return render(request, "reg.html")
#     else:
#         data = request.POST
#         await handle_registration(username=data.get('username'),
#                             password1=data.get("password1"),
#                             password2=data.get("password2"))
#
#


def get_github(request: HttpRequest) -> HttpResponse:
    response = github_parcer.parse()
    dates = list(response.keys())
    for date in dates:
        if type(date) != datetime.date:
            print(type(date), "  ", date)
            raise Exception
        response[date.strftime("%Y-%m-%d")] = response[date]
        response.pop(date)
    return JsonResponse(response)


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "reg.html")
    else:
        data = request.POST
        username = data.get("username")
        password1, password2 = data.get("password1"), data.get("password2")
        github_id = data.get("github_id")
        if github_id is None:
            github_id = None
        if username is None:
            return HttpResponse(
                "<h3><a href=''>Введите имя пользователя</a></h3>"
            )
        elif password1 is None or password2 is None:
            return HttpResponse("<h3><a href=''>Введите пароль</a></h3>")
        elif password1 != password2:
            return HttpResponse(
                "<h3><a href=''>Пароли должны совпадать</a></h3><br>"
            )
        else:
            newuser = User()
            newuser.create_user(username, password1, github_id)
            return HttpResponseRedirect(reverse("index"))


def login_form(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "login.html")
    else:
        data = request.POST
        user = authenticate(
            request,
            username=data.get("username"),
            password=data.get("password"),
        )
        if user is None:
            return HttpResponse(
                "<h3><a href=''>Пользователь с таким логином и паролем не найден</a></h3><br>"
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))


def logout_form(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def form_table(github_id: str | None, time_range: int) -> dict:
    if time_range == 0:
        time_range = DEFAULT_WEEK_RANGE
    # print(github_id)
    data_github = github_parcer.parse(str(github_id))
    data = merge_data(
        data_github,
        time_range,
        empty_data(time_range),
    )
    data_leetcode = leetcode_parcer.parse()
    data = merge_data(data_leetcode, time_range, data)
    data = concat_to_weekdays(data)
    return data


def show_table(request: HttpRequest) -> HttpResponse:
    context: dict = {}
    try:
        if request.user.is_authenticated:
            context = {
                    "data": form_table(
                        request.user.github_id, 0), # type ignore:[union-attr]
            }
        return render(
            request=request, template_name="grid.html", context=context
        )
    except AttributeError:
        response = redirect("/login")
        return response
