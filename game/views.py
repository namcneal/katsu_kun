from django.shortcuts import render

# Create your views here.

def index(request):
    """View function for home page of site."""

    context = {}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def play(request):
    context = {}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'play.html', context=context)

def about(request):
    context = {}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'about.html', context=context)
