from multiprocessing.sharedctypes import Value
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from matplotlib.pyplot import title
from requests import post
from . import forms
import numpy as np 


import markdown2

from . import util


def index(request):
    search_f=forms.search_form()
   
    if request.method=="POST":
        entry = request.POST['search']
        mdfile=util.get_search(entry)
        value=False
        if isinstance(mdfile,list):
            value=True
        return render(request, "encyclopedia/entry.html",{"entry":entry,"mdfile":mdfile,'value':value,"random":np.random.choice(util.list_entries(), size=1)[0]})

       
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),"form":search_f,"random":np.random.choice(util.list_entries(), size=1)[0]
    })
    

def entry_page(request,entry): 
    mdfile=util.get_entry(entry)
    if mdfile==None:
        return HttpResponse("<h1 >Error: page does not exist</h1>")
    return render(request, "encyclopedia/entry.html",{"entry":entry,"mdfile":mdfile,"random":np.random.choice(util.list_entries(), size=1)[0]})


def create(request):
    # return HttpResponse("Creat New Page") 
    if request.method=="POST":
        title=request.POST['title']
        text=request.POST['text']
        result=util.save_entry(title,text)
        if result == "exists":
            return HttpResponse("<h1> Error : Title already exists </h1> ")
        else:
           mdfile=util.get_entry(title)
           return render(request, "encyclopedia/entry.html",{"entry":title,"mdfile":mdfile,"random":np.random.choice(util.list_entries(), size=1)[0]}) 
        

    create_f=forms.create_form()
    return render(request,"encyclopedia/create.html",{'form':create_f,"random":np.random.choice(util.list_entries(), size=1)[0]})

def edit(request,title):
    if request.method=="POST":
        title=request.POST['title']
        text=request.POST['text']
        util.edit_entry(title,text)
        mdfile=util.get_entry(title)
        return render(request, "encyclopedia/entry.html",{"entry":title,"mdfile":mdfile,"random":np.random.choice(util.list_entries(), size=1)[0]})


    data_dict = {'title': title, 'text': util.get_entry(title)}
    create_f=forms.create_form(data_dict)
    return render(request,"encyclopedia/edit.html",{'form':create_f,'title':title,"random":np.random.choice(util.list_entries(), size=1)[0]})

