from django.db import models
from apps.proyectos.models import Proyecto

# Create your models here.

class Sprint(models.Model):
    """
    Manejo de los sprints del proyecto
    """
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(verbose_name='Descripcion')
    inicio = models.DateField(verbose_name='Fecha de Inicio, formato  DD/MM/AAAA')
    fin = models.DateField(verbose_name='Fecha de Inicio, formato  DD/MM/AAAA')
    orden = models.SmallIntegerField(verbose_name='Orden')
    proyecto = models.ForeignKey(Proyecto, null=False)

    class Meta:
        default_permissions = ()
        verbose_name = 'sprint'
        verbose_name_plural = 'sprints'

    def __unicode__(self):
        return self.nombre