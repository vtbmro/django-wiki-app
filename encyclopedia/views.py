from django.shortcuts import render, redirect
from .util import get_entry 
from . import util
import markdown
from django.http import HttpResponse
from django import forms
import os
import os.path
import random

class NewTaskForm(forms.Form):
    search = forms.CharField(label='search', 
    widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia', 
    'class':'search', 'name':'search', 'autocomplete' : 'off'}))

class NewPageForm(forms.Form):
    Title = forms.CharField(required=True)
    Markdown = forms.CharField(required=True,widget=forms.Textarea(
    attrs={"placeholder": "Enter the markdown here..."}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewTaskForm()
    })


def wiki(request, search):
    if get_entry(search) == None:
        return render(request, "encyclopedia/error.html",{
                        "error": "No entry found for this search"
                    })

    with open(f"./entries/{search}.md", "r") as file:
        text = file.read()
        html = markdown.markdown(text)
    
    return render(request, "encyclopedia/wiki.html",{
        "html": html,
        "form": NewTaskForm(),
        "search": search
    })


def search(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)

        if form.is_valid():
            search = form.cleaned_data["search"] 

            if os.path.isfile(f"./entries/{search}.md") == False:
                list_of_files = []

                for filename in os.listdir("./entries"):
                    if filename[:-3].__contains__(f"{search}"):
                        list_of_files.append(filename[:-3])

                if list_of_files == []:
                    return render(request, "encyclopedia/error.html",{
                        "error": "No entry found for this search"
                    })
            
                else:
                    return render(request, "encyclopedia/search.html",{
                        "entries": list_of_files,
                        "form": form,
                    })

            elif os.path.isfile(f"./entries/{search}.md"):
                return redirect(f"/wiki/{search}")

        else:
            return render(request, "encyclopedia/error.html",{
                        "error": "Not valid search parameter"
                    })
        
# TODO: new page function, will probably need to make a new 
# form with a textarea and an title input, we need to save the 
# title.md file with the markdown we inputted and after that 
# redirect the user into the page that he created

def newpage(request):
        if request.method == "POST":

            form = NewPageForm(request.POST)
            if form.is_valid():

                title = form.cleaned_data["Title"]
                markdown = form.cleaned_data["Markdown"]

                try:
                    file = open(f"./entries/{title}.md", "x")
                except FileExistsError:
                    return render(request, "encyclopedia/error.html",{
                        "error": "This page already exists"
                    })
                
                file = open(f"./entries/{title}.md", "w")
                file.write(markdown)

                return redirect(f"/wiki/{title}")
        else:
            return render(request, "encyclopedia/new_page.html",{
                "markdown": NewPageForm(),
                "form": NewTaskForm()
            })

class EditPageForm(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea, label="")

def editpage(request, markdown):
    if request.method == "GET":
        entry = util.get_entry(markdown)
        context = {
            "title": markdown,
            "edit": EditPageForm(initial={"textarea":entry})
        }
        return render(request, "encyclopedia/editpage.html", context)
    
    else:
        form = EditPageForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["textarea"]
            file = open(f"./entries/{markdown}.md", "w")
            file.write(new_content)
            file.close()
            return redirect(f"/wiki/{markdown}")

def randompage(request):
    files = []
    file_list = os.listdir("./entries")
    for file_name in file_list:
        files.append(file_name) 
    search = random.choice(files)
    return redirect(f"/wiki/{search[:-3]}")

# all the implementatiosn completed 