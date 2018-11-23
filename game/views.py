from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from game.models import Conjugator, Verb, Game
# Create your views here.

@csrf_exempt
def index(request):
    """View function for home page of site."""
    context = {}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

@csrf_exempt
def play(request):
    params = list(request.POST.keys())
    game = Game(params)
    for i in range(100):
        print(game.get_conjugation())
        
    if request.is_ajax and request.method == 'POST':
        attempt = request.POST.get('attempt')

        if request.session['correct_answer'] == attempt:
            print("HORRAY")


    context = {}
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'play.html', context=context)

def about(request):
    context = {}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'about.html', context=context)
