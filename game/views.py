from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from game.models import Conjugator
# Create your views here.

def index(request):
    """View function for home page of site."""
    request.session['correct_answer'] = "テスト"
    context = {}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

@csrf_exempt
def play(request):
    conjugator = Conjugator()

    if request.is_ajax and request.method == 'POST':
        attempt = request.POST.get('attempt')
        print(attempt)
        request.session['submitted_answer'] = attempt

        if request.session['correct_answer'] == attempt:
            print("HORRAY")


    context = {}
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'play.html', context=context)

def about(request):
    context = {}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'about.html', context=context)
