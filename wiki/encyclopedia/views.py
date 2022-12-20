from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django import forms
import markdown
import random

from . import util

class NewForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

class EditForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)


    def clean_title(self):
        cleaned_data = self.cleaned_data
        title = cleaned_data.get("title")
        return title


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    mdStr = util.get_entry(title)
    if mdStr:
        html = markdown.markdown(mdStr)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html
        })
    else:
        return render(request, "encyclopedia/notfound.html", {
            "message": f"Error: Wiki page titled '{title.capitalize()}' not found"
        })


def search(request):
    sub_list = []
    entries = util.list_entries()
    search = request.POST.get("q")

    for ent in entries:
        if search.lower() == ent.lower():
            return redirect("entry", title=search)
        elif search.lower() in ent.lower():
            sub_list.append(ent)
            return render(request, "encyclopedia/search.html",{
                "title":search,
                "sub_list":sub_list
    })  
    return render(request, "encyclopedia/notfound.html", {
            "message": f"Error: Wiki page titled '{search.capitalize()}' not found"
        })


def create(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = "# " + title + "\n" + form.cleaned_data["content"]
            if title not in util.list_entries():
                util.save_entry(title, content)
                return HttpResponseRedirect("/wiki/" + title)
            else:
                return render(request, "encyclopedia/notfound.html", {
                    "message": f"Error: Wiki page titled '{search.capitalize()}' Already Exists"
        })
    return render(request,"encyclopedia/create.html", {
            "title": "Create Page",
            "createpage": NewForm()
        })


def edit(request):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = "# " + title + "\n" + form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect("/wiki/" + title)

    return render(request,"encyclopedia/edit.html", {
            "title": "Edit Page",
            "editpage": EditForm()
        })  


def random_page(request):
    entries = util.list_entries()
    randomiser = random.choice(entries)
    mdStr = util.get_entry(randomiser)
    if mdStr:
        html = markdown.markdown(mdStr)
        return render(request, "encyclopedia/entry.html", {
            "title": randomiser,
            "content": html
        })
    else:
        return render(request, "encyclopedia/notfound.html", {
            "message": f"Error: Wiki page titled '{randomiser.capitalize()}' not found"
        })