from django.shortcuts import render


def exchange(request):
    name = 'xddd'
    
    data = [[0,0],[0,1],[1,0],[1,1]]

    context = {
            'name':name,
            'data':data
    }
    return render(request=request, template_name='commit_concatenate/index.html', context=context)
