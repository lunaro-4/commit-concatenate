from django.shortcuts import render
from .github_parcer import parse
import datetime

def concat_to_weekdays(data_input):
    sorted(data_input.items(), key=lambda x: x[1])
    data  = {
        0:[],
        1:[],
        2:[],
        3:[],
        4:[],
        5:[],
        6:[],
    }
    for i in data_input.keys():
        weekday = datetime.datetime.fromtimestamp(i).weekday()
        data[weekday].append([i,data_input[i]])
    return data

def form_table(request):
    name = 'xddd'
    data = parse()
    data = concat_to_weekdays(data)
    context = {
            'name':name,
            'data':data,
    }
    return render(request=request, template_name='commit_concatenate/index.html', context=context)
