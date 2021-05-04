from django.shortcuts import render
from django.http import HttpResponse
from home.models import Certificado,ArchivosGenerados
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from datetime import datetime
from zipfile import *
import requests
from home.util import *
# Create your views here.



def home(request):
    return render(request, "home.html")


def certificado(request):
    id = ""    
    if request.POST: 
        plantilla = Certificado() 
        plantilla.imagen = request.FILES.get("imgPC")
        plantilla.documentoDatos = request.FILES.get("infoCertificado")
        id = plantilla.documentoDatos
        plantilla.coordenadaX = request.POST.get("coordenadaX")
        plantilla.coordenadaY = request.POST.get("coordenadaY")
        plantilla.tipoLetra = request.FILES.get("typeTXT")
        plantilla.colorTexto = request.POST.get("colorTXT")
        plantilla.tamanioTexto = request.POST.get("tamanioTXT")
        plantilla.urlSpotify=request.POST.get("cancion")
        plantilla.save() #ORM
        generarCertificado(id)
        Archivo = Certificado.objects.get(documentoDatos = id)
        return render(request,"descarga.html",{"objeto":Archivo})



def generarCertificado(id):
    objeto = Certificado.objects.get(documentoDatos = id)
    datos = pd.read_csv(objeto.documentoDatos, sep=",")["Nombres"].to_list()
    tipo_letra = ImageFont.truetype(objeto.tipoLetra, objeto.tamanioTexto)
    for nombre in datos:            
        certificado = Image.open(objeto.imagen)
        if (objeto.urlSpotify):
            nom = guardaImg(objeto.urlSpotify)
            qr = Image.open("media/plantillas/"+nom+".png")
            certificadoW = certificado.size[0]
            certificadoH = certificado.size[1]
            qrsize = (int(qr.size[0]/3.5),int(qr.size[1]/3.5))
            qr = qr.resize(qrsize,Image.ANTIALIAS)
            ubicacion = (int(certificadoW/2)-int(qrsize[0]/2),certificadoH-70)
            certificado.paste(qr,ubicacion)

        nuevo = ImageDraw.Draw(certificado)
        coordenadas = (objeto.coordenadaX, objeto.coordenadaY-objeto.tamanioTexto+10)
        color_texto = hexToRGB(objeto.colorTexto)
        nuevo.text(coordenadas, nombre, fill=color_texto, font=tipo_letra)
        certificado.save("media/generadosAutomaticos/"+nombre+".pdf")
        nombreRAR ="Certificados"+str(objeto.id)+".rar"
        with ZipFile("media/"+nombreRAR,"a") as myZip:
            myZip.write("media/generadosAutomaticos/"+nombre+".pdf")
        archivoGenerado = ArchivosGenerados()
        archivoGenerado.nombreID = id
        archivoGenerado.docGenerado =  "generadosAutomaticos/"+nombre+".pdf"
        archivoGenerado.save()
    objeto.archivoRAR = nombreRAR
    objeto.save() 


          