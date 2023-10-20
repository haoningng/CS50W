from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown
from random import randint, choice

from . import util


def index(request):
    if request.method == "GET":
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def search(request):
    if request.method == "POST":
        title_list = util.list_entries()
        new_list = []
        q = request.POST.get("q")
        # If there is no direct match, search by substring
        if not q in title_list:
            for each_title in title_list:
                if q in each_title:
                    new_list.append(each_title)
            return render(request, "encyclopedia/index.html", {
                "entries": new_list
            })
        # If there is a direct match
        else:
            content = util.get_entry(q)
            return render(request, "encyclopedia/entry.html", {
                "content": Markdown().convert(content),
                "title": q
            })


def entry(request, title):
    title_list = util.list_entries()

    # Render 404 error page if page not found
    if not title in title_list:
        return render(request, "encyclopedia/error.html")

    # Render the content of the page if page is found
    content = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "content": Markdown().convert(content),
        "title": title
    })

def random(request):
    title_list = util.list_entries()
    title = choice(title_list)
    content = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "content": Markdown().convert(content),
        "title": title
    })

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    if request.method == "POST":
        title_list = util.list_entries()
        title = request.POST.get("title")
        content  = request.POST.get("content")
        # If the title doesn't exist
        if not title in title_list:
            util.save_entry(title, content)
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })
        # If the title already exists
        else:
            return render(request, "encyclopedia/error2.html")

def edit(request):
    if request.method == "POST":
        title = request.POST.get("entry_title")
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "content": content,
            "title": title
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content  = request.POST.get("content")
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "content": Markdown().convert(content),
            "title": title
        })

def delete(request):
    if request.method == "POST":
        title = request.POST.get("entry_title")
        util.del_entry(title)
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })