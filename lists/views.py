from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.html_parser import HTMLParseError
from django.core.exceptions import ValidationError

# Create your views here.
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm


def home_page(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})
   

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(data=request.POST, for_list=list_)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(
        request, 'lists/list.html',
        { 
            'list': list_,
            'form': form
        }
    )


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        return render(request, 'lists/home.html', {'form': ItemForm()})
