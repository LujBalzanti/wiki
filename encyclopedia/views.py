from django.shortcuts import render, redirect
import markdown2
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from django.core.files import File
import re

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    try:
        page = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
        "page": page,
        "title": title
    })
    except TypeError:
        return render(request, "encyclopedia/missing.html")

def search(request, query=""):
    if request.method == "GET":
        query = request.GET.get('q')
        try:
            page = markdown2.markdown(util.get_entry(query))
            return render(request, "encyclopedia/entry.html", {
                "page": page
            })    
        except:
            def find_match(entry):
                test = re.compile(f"\w*{query}\w*", re.IGNORECASE)
                match = test.match(entry)
                if match:
                    return match.group()
                else:
                    return None
            return render(request, "encyclopedia/search.html", {
                "results": list(filter(find_match, util.list_entries()))
            })   
        
def newPage(request):
    if request.method == "POST":
        title = request.POST.get("title").replace(" ", "_")
        content = request.POST.get("pageContent")
        try:
            with open(f"entries/{title}.md") as entry:
                return render(request, "encyclopedia/exists.html")
        except:
            with open(f"entries/{title}.md", "w") as f:
                newEntry = File(f)
                newEntry.write(content)
        return HttpResponseRedirect(f"wiki/{title}")

    return render(request, "encyclopedia/newPage.html")

def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("pageContent")
        with open(f"entries/{title}.md", "w") as f:
            entry = File(f)
            entry.write(content)

        return redirect("entry", title=title)

    else:
        try:
            return render(request, "encyclopedia/edit.html", {
            "page": util.get_entry(title),
            "title": title
        })
        except TypeError:
            return render(request, "encyclopedia/missing.html")

