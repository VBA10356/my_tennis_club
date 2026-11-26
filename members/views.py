from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member
# Create your views here.

def main(request):
    template = loader.get_template("main.html")
    return HttpResponse(template.render())

def members (request):
    mymembers = Member.objects.all().values()
    template = loader.get_template("all_members.html")
    context = {
        'mymembers':mymembers
    }
    return HttpResponse(template.render(context, request))

def firstHTML (request):
    template = loader.get_template('myFirst.html')
    return HttpResponse(template.render())

def details(request,id):
    mymember = Member.objects.get(id=id)
    template = loader.get_template("details.html")
    
    context = {
        'mymember' : mymember,
        
    }

    return HttpResponse(template.render(context,request))

def testing(request):
    alldata = Member.objects.order_by("-firstName").filter(firstName="Hal", lastName="Jordan").values() | Member.objects.filter(firstName__contains="uce").values()
    mymembers = Member.objects.all()
    template = loader.get_template('template.html')
    context = {
        'fruits' : ['apple', 'banana', 'cherry'],
        'mymembers': mymembers,
        'allData' : alldata
    }

    return HttpResponse(template.render(context, request))