from django.shortcuts import render
from commit_concatenate.form_table import form_table


def show_tabel(request):

    context = {
        'data': form_table(),
    }
    return render(request=request, template_name='grid.html', context=context)

def show_home(request):

    context = {
    }
    return render(request=request, template_name='base.html', context=context)
