from django.shortcuts import render

from commit_concatenate import github_parcer
from commit_concatenate import leetcode_parcer
import datetime
import time

DEFAULT_WEEK_RANGE = 6


def empty_data(time_range=DEFAULT_WEEK_RANGE):
    base = datetime.datetime.today()
    date_list = []
    for i in range(time_range * 7):
        fixed_date = base - datetime.timedelta(days=i)
        fixed_date = fixed_date.date().timetuple()
        date_list.append(int(time.mktime(fixed_date)))
    empty_data = {}
    for i in date_list:
        empty_data[i] = [0]
    return empty_data


def merge_data(data : dict, main_set :dict):
    if main_set == None:
        main_set = empty_data()
    for i in main_set.keys():
        if i in data.keys():
            main_set[i].append(data[i])
        else:
            main_set[i].append(0)
    for i in main_set.keys():
        if i in data.keys():
            value = 0
            for j in range(1, len(main_set[i])):
                value += main_set[i][j] 
            main_set[i][0] = value
    return main_set


def concat_to_weekdays(data_input):
    tuple = sorted(data_input.items(), key=lambda x: x[0])
    for a, b in tuple:
        data_input.setdefault(a, b)
    data = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
    }
    if datetime.datetime.fromtimestamp(tuple[-1][0]).weekday() != 6:
        for i in range(datetime.datetime.fromtimestamp(tuple[-1][0]).weekday() + 1):
            data[datetime.datetime.fromtimestamp(tuple[-i - 1][0]).weekday()].append([0,[0]*len(tuple[1])])
    for i in range(len(tuple)):
        weekday = datetime.datetime.fromtimestamp(tuple[i][0]).weekday()
        date_string = datetime.datetime.fromtimestamp(tuple[i][0]).date()
        data[weekday].append([str(date_string), tuple[i][1]]) #str(date_string)  #tuple[i][0]
    return data


def form_table(request):
    name = 'xddd'
    data_github = github_parcer.parse()
    data = merge_data(data_github, empty_data())
    data_leetcode = leetcode_parcer.parse()
    data = merge_data(data_leetcode, data)
    data = concat_to_weekdays(data)
    context = {
        'name': name,
        'data': data,
    }
    return render(request=request, template_name='commit_concatenate/index.html', context=context)
