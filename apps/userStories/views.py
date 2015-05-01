from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User, Permission
from django.db.models import Q
from django.forms.models import modelformset_factory
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from datetime import datetime

# Create your views here.
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy
from sigepro import settings
from apps.flujos.models import Flujo
from apps.userStories.models import UserStory
from apps.proyectos.models import Proyecto
from apps.userStories.forms import EstadoUSForm, PrimerFlujoForm
from django import forms




@login_required
def listar_userStories(request):
    """
    vista para listar los userStories pertenecientes a la flujo
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_userStory: clave foranea a la flujo
    @return render_to_response(..) o HttpResponse(...)
    """
    #tuserStory=get_object_or_404(Flujo,id=id_flujo)
    #flujo=Flujo.objects.filter(id=id_flujo)
    #if es_miembro(request.user.id,flujo,''):
    userStories=UserStory.objects.filter()
    #if puede_add_userStories(flujo):
    nivel = 3
    #id_proyecto=Flujo.objects.get().proyecto_id
    #proyecto=Proyecto.objects.get()
    return render_to_response('userStories/listar_userStories.html', {'datos': userStories, 'nivel':nivel},
                                  context_instance=RequestContext(request))
    #else:
        #ESTE HAY QUE CORREGIR SI HAY TIEMPO
        #return HttpResponse("<h1>No se pueden administrar los UserStories de esta flujo. La flujo anterior aun no tiene userStories finalizados<h1>")

    #else:
    #return render_to_response('403.html')





# @login_required
# def detalle_userStory(request, id_userStory):
#     """
#     vista para ver los detalles del userStory <id_userStory>
#     @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
#     @param id_userStory: clave foranea al userStory
#     @return render_to_response(..)
#     """
#     userStory=get_object_or_404(UserStory,id=id_userStory)
#     tipouserStory=get_object_or_404(TipoUserStory,id=userStory.tipo_userStory_id)
#     flujo=tipouserStory.flujo_id
#     fasse=Flujo.objects.get(id=flujo)
#     proyecto=Proyecto.objects.get(id=fasse.proyecto_id)
#     if es_miembro(request.user.id, flujo,''):
#         atributos=AtributoUserStory.objects.filter(id_userStory=id_userStory)
#         archivos=Archivo.objects.filter(id_userStory=id_userStory)
#         dato = get_object_or_404(UserStory, pk=id_userStory)
#
#         return render_to_response('userStories/detalle_userStory.html', {'datos': dato, 'atributos': atributos, 'archivos':archivos,'flujo':fasse,'proyecto':proyecto}, context_instance=RequestContext(request))
#     else:
#         return render_to_response('403.html')

