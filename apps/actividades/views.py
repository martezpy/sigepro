# -*- encoding: utf-8 -*-

__text__ = 'Este modulo contiene funciones que permiten el control de las actividades'

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.actividades.models import Actividad
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q
from django.contrib import messages
from sigepro import settings
from django.contrib import messages
from django.shortcuts import render
from apps.proyectos.models import Proyecto
from apps.flujos.models import Flujo
from apps.actividades.forms import ActividadForm, ModificarActividadForm, CrearActividadForm
from apps.roles.forms import GroupForm
from datetime import datetime
from apps.userStories.models import UserStory
from apps.actividades.models import Actividad


@login_required
@permission_required('actividad')
def registrar_actividad(request, id_proyecto):
    """
    Vista para registrar un nuevo actividad dentro de proyecto
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return HttpResponseRedirect('/actividades/register/success') si el rol fue correctamente asignado o
    render_to_response('proyectos/registrar_proyecto.html',{'formulario':formulario}, context_instance=RequestContext(request)) al formulario
    """
    mensaje=100
    proyecto = Proyecto.objects.get(id=id_proyecto)
    if request.method=='POST':
        proyecto = Proyecto.objects.get(id=id_proyecto)
        formulario = CrearActividadForm(request.POST)
        if formulario.is_valid():
            newActividad = Actividad(nombre = request.POST["nombre"],descripcion = request.POST["descripcion"],
                               estado = "PRO", proyecto_id = id_proyecto)
            orden=Actividad.objects.filter(proyecto_id=id_proyecto)
            proyecto=Proyecto.objects.get(id=id_proyecto)
            cantidad = orden.count()
            if cantidad>0:
                newActividad.orden=orden.count()+1 # Calculo del orden del actividad a crear
                newActividad.save()
                return render_to_response('actividades/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
            else:
                newActividad.orden=1
                newActividad.save()
                return render_to_response('actividades/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
    else:
        formulario = CrearActividadForm() #formulario inicial
    return render_to_response('actividades/registrar_actividades.html',{'formulario':formulario,'id':id_proyecto, 'proyecto':proyecto, 'mensaje':mensaje},
                              context_instance=RequestContext(request))



@login_required
@permission_required('flujos, actividades')
def listar_actividades(request,id_flujo):
    """
    vista para listar los actividades del flujo
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return render_to_response('actividades/listar_actividades.html', {'datos': actividades}, context_instance=RequestContext(request))
    """
    actividades = Actividad.objects.filter(flujo_id=id_flujo).order_by('orden')
    proyecto = Proyecto.objects.get(id=id_flujo)

    return render_to_response('actividades/listar_actividades.html', {'datos': actividades}, context_instance=RequestContext(request))


@login_required
@permission_required('flujos, actividades')
def editar_actividad(request,id_actividad):
    """
    Vista para editar un proyecto,y actividad
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: HttpResponseRedirect('/proyectos/register/success/') cuando el formulario es validado correctamente o render_to_response('proyectos/editar_proyecto.html', { 'proyectos': proyecto_form, 'nombre':nombre}, context_instance=RequestContext(request))
    """
    actividad= Actividad.objects.get(id=id_actividad)
    flujo=Flujo.objects.get(id=actividad.flujo_id)
    if request.method == 'POST':
        # formulario enviado
        mensaje =100
        actividad_form = ModificarActividadForm(request.POST, instance=actividad)
        if actividad_form.is_valid():
            orden=Actividad.objects.filter(flujo_id=actividad.flujo_id)
            cantidad = orden.count()
            if cantidad>1 and actividad.orden != cantidad and actividad.orden >1: #comprobaciones de fechas
                actividad_form.save()
                return render_to_response('actividades/creacion_correcta.html',{'id_actividad':id_actividad}, context_instance=RequestContext(request))
            elif cantidad>1 and actividad.orden != cantidad and actividad.orden==1:
                actividad_form.save()
                return render_to_response('actividades/creacion_correcta.html',{'id_actividad':id_actividad}, context_instance=RequestContext(request))
            elif cantidad>1 and actividad.orden == cantidad:
                actividad_form.save()
                return render_to_response('actividades/creacion_correcta.html',{'id_actividad':id_actividad}, context_instance=RequestContext(request))
            else:
                actividad_form.save()
                return render_to_response('actividades/creacion_correcta.html',{'id_actividad':id_actividad}, context_instance=RequestContext(request))
    else:
        # formulario inicial
        actividad_form = ModificarActividadForm(instance=actividad)
    return render_to_response('actividades/editar_actividad.html', { 'form': actividad_form, 'actividad': actividad, 'flujo': flujo}, context_instance=RequestContext(request))

@login_required
@permission_required('actividad')
def actividades_todas(request,id_proyecto):
    """
    vista para listar las actividades del sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: render_to_response('actividades/actividades_todas.html', {'datos': actividades, 'proyecto' : proyecto}, context_instance=RequestContext(request))
    """
    actividades = Actividad.objects.all()
    proyecto = Proyecto.objects.get(id=id_proyecto)
    return render_to_response('actividades/actividades_todas.html', {'datos': actividades, 'proyecto' : proyecto}, context_instance=RequestContext(request))


@login_required
@permission_required('actividad')
def detalle_actividad(request, id_actividad):

    """
    Vista para ver los detalles del usuario <id_user> del sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_actividad: referencia a la actividad dentro de la base de datos
    @return: render_to_response
    """

    dato = get_object_or_404(Actividad, pk=id_actividad)
    proyecto = Proyecto.objects.get(id=dato.proyecto_id)
    if proyecto.estado!='PRO':
        proyectos = Proyecto.objects.all().exclude(estado='ELI')
        return render_to_response('proyectos/listar_proyectos.html', {'datos': proyectos,'mensaje':1},
                              context_instance=RequestContext(request))
    return render_to_response('actividades/detalle_actividad.html', {'datos': dato,'proyecto':proyecto}, context_instance=RequestContext(request))


@login_required
@permission_required('actividad')
def eliminar_actividad(request,id_actividad):
    """
    Vista para eliminar un actividad de un proyecto. Busca la actividad por su id_actividad y lo destruye.
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_actividad: referencia a la actividad dentro de la base de datos
    @return: render_to_response('actividades/listar_actividades.html', {'datos': actividades, 'proyecto' : proyecto}, context_instance=RequestContext(request))
    """
    actividad = get_object_or_404(Actividad, pk=id_actividad)
    proyecto = Proyecto.objects.get(id=actividad.proyecto_id)
    if proyecto.estado =='PRO':
        actividad.delete()
    actividades = Actividad.objects.filter(proyecto_id=proyecto.id).order_by('orden')
    return render_to_response('actividades/listar_actividades.html', {'datos': actividades, 'proyecto' : proyecto}, context_instance=RequestContext(request))

@login_required
@permission_required('actividad')
def buscar_actividades(request,id_proyecto):
    """
    vista para buscar los actividades del proyecto
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: render_to_response('proyectos/listar_proyectos.html', {'datos': results}, context_instance=RequestContext(request))
    """
    query = request.GET.get('q', '')
    proyecto = Proyecto.objects.get(id=id_proyecto)
    if query:
        qset = (
            Q(nombre__contains=query)
        )
        results = Actividad.objects.filter(qset, proyecto_id=id_proyecto).distinct()
    else:
        results = []


    return render_to_response('actividades/listar_actividades.html', {'datos': results, 'proyecto' : proyecto}, context_instance=RequestContext(request))


@login_required
@permission_required('actividad')
def asignar_usuario(request,id_actividad):
    """
    Vista auxiliar para obtener un listado de usuarios para asociar a el actividad
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_actividad: referencia a la actividad dentro de la base de datos
    @return: render_to_response
    """
    usuarios=User.objects.filter(is_active=True)
    actividad=Actividad.objects.get(id=id_actividad)
    roles=Group.objects.filter(actividad__id=id_actividad)
    for rol in roles:       #Un usuario tiene un rol por actividad
        usuarios=usuarios.exclude(groups__id=rol.id)
    proyecto = Proyecto.objects.get(id=actividad.proyecto_id)
    if proyecto.estado!='PRO':
        proyectos = Proyecto.objects.all().exclude(estado='ELI')
        return render_to_response('proyectos/listar_proyectos.html', {'datos': proyectos,'mensaje':1},
                              context_instance=RequestContext(request))
    return render_to_response('actividades/asignar_usuarios.html', {'datos': usuarios, 'actividad' : actividad,'proyecto':proyecto}, context_instance=RequestContext(request))


@login_required
@permission_required('actividad')
def desasignar_usuario(request,id_actividad):
    """
    vista para listar a los usuario de un actividad, para poder desasociarlos
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_actividad: referencia a la actividad dentro de la base de datos
    @return: render_to_response('actividades/desasignar_usuarios.html', {'datos': usuarios,'actividad':id_actividad,'proyecto':proyecto}, context_instance=RequestContext(request))
    """
    actividad=Actividad.objects.get(id=id_actividad)
    proyecto = Proyecto.objects.get(id=actividad.proyecto_id)
    if proyecto.estado!='PRO':
        proyectos = Proyecto.objects.all().exclude(estado='ELI')
        return render_to_response('proyectos/listar_proyectos.html', {'datos': proyectos,'mensaje':1},
                              context_instance=RequestContext(request))
    roles=Group.objects.filter(actividad__id=id_actividad)
    usuarios=[]
    for rol in roles:
        p=User.objects.filter(groups__id=rol.id)
        for pp in p:
            usuarios.append(pp) #lista todos los usuarios con rol en el actividad
    return render_to_response('actividades/desasignar_usuarios.html', {'datos': usuarios,'actividad':actividad,'proyecto':proyecto,'roles':roles}, context_instance=RequestContext(request))

@login_required
@permission_required('proyectos')
def estadoKanban(request, id_actividad):
    """

    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: render_to_response('proyectos/cambiar_estado_proyecto.html', { 'proyectos': proyecto_form, 'nombre':nombre}, context_instance=RequestContext(request))
    """
    # formulario inicial
    # actividad=Actividad.objects.get(id=id_actividad)
    userStories = UserStory.objects.filter(actividad=id_actividad)
    actividades = Actividad.objects.filter(actividad_id=id_actividad)
    cantActividades = actividades.count()
    print "cantactividades"
    print cantActividades
    return render_to_response('actividades/kanban.html', {'userStories': userStories, 'actividades': actividades, 'cantActividades': cantActividades}, context_instance=RequestContext(request))