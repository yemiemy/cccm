from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def events(request):
    return render(request, "event.html")


def blog(request):
    return render(request, "blog.html")


def serviceDetail(request):
    return render(request, "serviceDetail.html")
    