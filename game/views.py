from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from game.models import Conjugator, Verb
# Create your views here.

@csrf_exempt
def index(request):
    """View function for home page of site."""
    request.session['correct_answer'] = "テスト"
    context = {}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

@csrf_exempt
def play(request):
    conjugator = Conjugator()
    verb_list = Verb.objects.all()

    for verb in verb_list:
        for x in [1,0]:
            conjugator.set_verb(verb)
            conjugator.ba(x)
            print(str(conjugator))

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
