from django.shortcuts import render
from django.http import HttpResponse
import markdown2
from . import util
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from django.core.files import File
from django.http import HttpResponseRedirect


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display_entry(request, entry):
        markdowner = Markdown()
        entryPage = util.get_entry(entry)

        if entryPage is None:
            return render(request, "encyclopedia/entryNil.html",
            {"entry": entry} )

        else:
            markdowner = Markdown()
            return render(request, "encyclopedia/entry.html", 
            { "entry": markdowner.convert(entryPage)
            })

def search(request):
    
    existing_entries = util.list_entries()
    uppercase_existing_entries = [x.upper() for x in existing_entries]
    existing_entries = uppercase_existing_entries
    print(existing_entries)
    entry = request.GET.get('q').upper()
    print(entry)

    markdowner = Markdown()
    entryPage = util.get_entry(entry)

    if entry in existing_entries:
        return render(request, "encyclopedia/entry.html", {         
        "entry": markdowner.convert(entryPage)})
    else:
        return render(request, "encyclopedia/entryNil.html",
            {"entry": entry} )

# def newPage(request):
#     return render(request, "encyclopedia/newPage.html")

class newEntryForm(forms.Form):
    title = forms.CharField(max_length=30)
    content = forms.CharField(
        max_length=2000,
        widget=forms.Textarea()
    )
    edit = forms.BooleanField(initial=False)

def newPage(request):
    if request.method == 'POST':
        form = newEntryForm(request.POST)
        
        if form.is_valid():
            title =form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            title_present=util.get_entry(title)
            if (title_present is None or form.cleaned_data["edit"] is True):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/newPage.html", 
                {"form": form,
                "existing": True,
                "entry": title})
        else:
            form = newEntryForm()
            return render(request, "encyclopedia/newPage.html", {'form': form, "existing": False})
    
    else:
        return render(request, "encyclopedia/newPage.html",
        {
            "form": newEntryForm(),
            "existing": False
        })

