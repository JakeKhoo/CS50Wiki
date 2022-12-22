from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from markdown import Markdown
from . import util
from django import forms
import random as rand

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
                "searchform" : SearchForm()
    })

def entry(request, title):
    try:
        entry_HTML = Markdown().convert(util.get_entry(title))
        return render(request, "encyclopedia/entry.html",{
            "title" : title,
            "entry" : entry_HTML,
                "searchform" : SearchForm()
         })
    except:
        return render(request, "encyclopedia/error.html",{
            "title" : title,
                "searchform" : SearchForm()

         })


class EditForm(forms.Form):
    entry = forms.CharField(label= '', widget = forms.Textarea(attrs = {
        "placeholder": "Entry",
        "class": "form-control",
        "style" : 'width: 500px; height:400px'
    }))

class SearchForm(forms.Form):
    search = forms.CharField(label= '', widget = forms.TextInput(attrs = {
        "placeholder": "Search",
        "style" : 'max-width: 300px;'
    }))

class CreateForm(forms.Form):
    title = forms.CharField(label= '', widget = forms.TextInput(attrs = {
        "placeholder": "Title of the Page",
        "style" : 'max-width: 300px;'
    }))
    entry = forms.CharField(label= '', widget = forms.Textarea(attrs = {
        "placeholder": "Entry",
        "class": "form-control",
        "style" : 'width: 500px; height:400px'
    }))

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html",{
            "createform" : CreateForm(),
            "searchform" : SearchForm()
        })
    else:
        form = CreateForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            entry = form.cleaned_data['entry']
        else:
            return render(request, "encyclopedia/create.html",{
                "createform" : CreateForm(),
                "searchform" : SearchForm()
        })

        if util.get_entry(title) != None:
            messages.warning(request, 'Title: {} already exists, use a new title or edit the existing page.'.format(title))
            return render(request, "encyclopedia/create.html",{
                "createform" : CreateForm(),
                "searchform" : SearchForm()
        })

        else:
            util.save_entry(title, "#" + title + "\n" + entry)
            return redirect(reverse('entry', args=[title]))

def edit(request, title):
    if request.method == "GET":
        entry = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
                "editform" : EditForm(initial={'entry':entry}),
                "title" : title,
                "searchform" : SearchForm()
        })
    else:
        f = EditForm(request.POST)
        a = f.is_valid()
        util.save_entry(title, f.cleaned_data['entry'])
        return redirect(reverse('entry', args=[title]))

def random(request):
    length = len(util.list_entries())
    randomtitle = util.list_entries()[rand.randrange(length)]
    return redirect(reverse('entry', args=[randomtitle]))

def search(request):
    f = SearchForm(request.POST)
    a = f.is_valid()
    search = f.cleaned_data["search"]
    lst=[]
    e = util.list_entries()
    for ent in e:
        if search.lower() in ent.lower():
            lst.append(ent)
    if util.get_entry(search):
        return redirect(reverse('entry', args = [search]))
    else:
        
        return render(request,"encyclopedia/search.html", {
            "entries": lst,
            "search" : search.lower(),
            "searchform" : SearchForm()
        })