from django.shortcuts import render
from .github_parcer import parse


def form_table(request):
    name = 'xddd'
    
    data = parse() 

    context = {
            'name':name,
            'data':data
    }
    return render(request=request, template_name='commit_concatenate/index.html', context=context)
