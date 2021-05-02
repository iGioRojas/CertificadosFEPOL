from django.db import models

# Create your models here.
class Certificado(models.Model):
    imagen = models.ImageField(upload_to = "plantillas",null="True")
    documentoDatos = models.FileField(upload_to="archivos", null=True, blank=True)
    coordenadaX = models.IntegerField(null = True)
    coordenadaY = models.IntegerField(null = True)
    isCertificado = models.BooleanField(default = False)
    isPost = models.BooleanField(default = False)
    tipoLetra = models.FileField(upload_to="archivos", null=True, blank=True)
    tamanioTexto = models.IntegerField(null = False,default = 11)
    colorTexto = models.CharField(null = True,max_length=8)
    urlSpotify= models.CharField(null=True,max_length=120)
    archivoRAR = models.FileField(upload_to="archivos", null=True, blank=True)


class ArchivosGenerados(models.Model):
    nombreID = models.TextField(null = False)
    docGenerado = models.FileField(upload_to="generadosAutomaticos",null = True, blank = True)