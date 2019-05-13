from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from game.models import Conjugator, Verb, Game
import urllib, time

# Create your views here.

@csrf_exempt
def index(request):
    """View function for home page of site."""
    context = {}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

# Converts a verb string into html with furigana
def verb_string_to_html(string):
    split_verb = string.split(";")
    html = ""

    for n in range(len(split_verb)):
        # Handling the kanji, so we'll only grab one character
        if n < len(split_verb) -1:
            html += "<rb>" + split_verb[n].replace(",", "</rb><rt>") + "</rt>"
    # The last entry in the split verb is the okurigana
    else:
            html += split_verb[n]
    return html

def params_to_html(param_list):
    forms = {'short':'', 'polite':'~ます', 'te':'~て', 'tai':'〜たい','tara':'~たら', 'ba':'~ば'}
    tense = {'non-past':'present ', 'past':'past '}
    polarity = {'non-negative':'positive ', 'negative':'negative '}

    if param_list[0] == 'regular':
        param_list[0] = ""
    else:
        param_list[0] += "'s"
    if param_list[3] in ['standard']:
        return [param_list[0], polarity[param_list[1]], tense[param_list[2]],
                forms[param_list[3]], "%s" %formality[param_list[4]]]

    return [param_list[0],  polarity[param_list[1]], "",
            forms[param_list[3]], ""]

@csrf_exempt
def play(request):
    params = request.GET.keys()
    game = Game(params)

    # Process the initial submission from the homepage
    if request.method == 'GET':
        # Get a random conjugation for the user, in the form of the list given
        # by this function.
        request.session['current_verb'] = game.get_conjugation()

        # Extract the parameter list from the outputted conjugation
        request.session['html_params']  = params_to_html(request.session['current_verb'][2])

        character = "../static/resources/ganbaru.png"
    # Process the user's conjugation attempts
    if request.is_ajax and request.method == 'POST':
        attempt = request.POST.get('attempt')

        if attempt in request.session['current_verb'][3]:
            request.session['current_verb'] = game.get_conjugation()
            request.session['html_params']  = params_to_html(request.session['current_verb'][2])
            character = "../static/resources/ganbaru.png"

        else:
            # print(request.session['current_verb'])
            character = "../static/resources/incorrect.png"


    # Send the proper parameters for the current conjugation to the template
    context = {'verb'        :verb_string_to_html(request.session['current_verb'][0]),
               'translation' :request.session['current_verb'][1],
               'construction':request.session['html_params'][0],
               'polarity'    :request.session['html_params'][1],
               'tense'       :request.session['html_params'][2],
               'form'        :request.session['html_params'][3],
               'character'   :character
              }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'play.html', context=context)

def about(request):
    context = {}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'about.html', context=context)
