from django.shortcuts import render
import urllib.request
import json
from http import HTTPStatus
from urllib.error import HTTPError
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import Players

# Create your views here.
def index(request):
    return render(request, 'app_poke_api/index.html')

def pokemon(request):
    if request.method == 'POST':
        pokemon = request.POST['pokemon'].lower()
        url_pokeapi = urllib.request.Request(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')
        url_pokeapi.add_header('User-Agent', "pikachu")
        source = urllib.request.urlopen(url_pokeapi).read()
        list_of_data = json.loads(source)
        data = {
                    "number": str(list_of_data['id']),
                    "name": str(list_of_data['name']).capitalize(),
                    "sprite": str(list_of_data['sprites']['front_default']),
                    "ability": str(list_of_data['abilities'][0]['ability']['name']).capitalize(),
                    "type": str(list_of_data['types'][0]['type']['name']),
                }
    else:
            data = {}
    return render(request, 'app_poke_api/pokemon.html',data)

class ApiView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request,id=0):
        if(id>0):
            players = list(Players.objects.filter(id=id).values())
            if len(players)>0:
                player=players[0]
                data={'message':"Succes",'players':player}
            else:
                data={'message':"No players found."}
            return JsonResponse(data)
        else:    
            players = list(Players.objects.values())
            if len(players)>0:
                data={'message':"Succes",'players':players}
            else:
                data={'message':"No players to Show."}
            return JsonResponse(data)

    def post(self, request):
        jasonData = json.loads(request.body)
        Players.objects.create(name=jasonData['name'],country=jasonData['country'],age=jasonData['age'])
        data={'message':"Player saved correctly."}
        return JsonResponse(data)

    def put(self, request,id):
        jasonData = json.loads(request.body)
        players = list(Players.objects.filter(id=id).values())
        if len(players)>0:
            player=Players.objects.get(id=id)
            player.name=jasonData['name']
            player.country=jasonData['country']
            player.age=jasonData['age']
            player.save()
            data={'message':"Updated."}
        else:
            data={'message':"No players found."}
        return JsonResponse(data)

    def delete(self, request,id):
        players = list(Players.objects.filter(id=id).values())
        if len(players)>0:
            Players.objects.filter(id=id).delete()
            data={'message':"Deleted"}
        else:
            data={'message':"No players found."}
        return JsonResponse(data)