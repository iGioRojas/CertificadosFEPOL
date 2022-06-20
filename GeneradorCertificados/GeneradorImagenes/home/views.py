from django.shortcuts import render
from django.http import HttpResponse
from pandas.io.parsers import TextParser
from home.models import Certificado, ArchivosGenerados
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from datetime import datetime
from zipfile import *
import requests
from home.util import *
from io import BytesIO
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
        plantilla.urlSpotify = request.POST.get("cancion")
        plantilla.save()  # ORM
        generarCertificado(id)
        #sgteTexto(id)
        Archivo = Certificado.objects.get(documentoDatos=id)
        return render(request, "descarga.html", {"objeto": Archivo})


def generarCertificado(id):
    objeto = Certificado.objects.get(documentoDatos=id)
    archivo = pd.read_csv(objeto.documentoDatos, sep=";",
                        encoding='utf-8')
    nombres = archivo["Nombres"].to_list()
    # correos = archivo["Correo"].to_list()
    tipo_letra = ImageFont.truetype(objeto.tipoLetra, objeto.tamanioTexto)
    nombreCertificado = []
    for i in range(len(nombres)):
        name = nombres[i]
        name = name.strip()
        nombreCertificado.append(name.title())
    
    for i in range(len(nombreCertificado)):
        certificado = Image.open(objeto.imagen)
        #if (objeto.urlSpotify):
        # nom = guardaImg(musica[i])
        # qr = Image.open("media/plantillas/"+nom+".png")
        # certificadoW = certificado.size[0]
        # certificadoH = certificado.size[1]
        # qrsize = (int(qr.size[0]/3.5), int(qr.size[1]/3.5))
        # qr = qr.resize(qrsize, Image.ANTIALIAS)
        # ubicacion = (int(certificadoW/2)-int(qrsize[0]/2), certificadoH-70)
        # certificado.paste(qr, ubicacion)
        nuevo = ImageDraw.Draw(certificado)
        ubiRelativa = tipo_letra.getlength(nombreCertificado[i])/2
        coordenadas = (objeto.coordenadaX-ubiRelativa, objeto.coordenadaY -
                       objeto.tamanioTexto+10)
        color_texto = hexToRGB(objeto.colorTexto)
        nuevo.text(coordenadas, nombreCertificado[i], fill=color_texto, font=tipo_letra, align='center')
        certificado.save("media/generadosAutomaticos/"+nombreCertificado[i]+".pdf")
        nombreRAR = "Certificados"+str(objeto.id)+".rar"
        with ZipFile("media/"+nombreRAR, "a") as myZip:
            myZip.write("media/generadosAutomaticos/"+nombreCertificado[i]+".pdf")
        archivoGenerado = ArchivosGenerados()
        archivoGenerado.nombreID = id
        archivoGenerado.docGenerado = "generadosAutomaticos/"+nombreCertificado[i]+".pdf"
        archivoGenerado.save()
    objeto.archivoRAR = nombreRAR
    objeto.save()
        

# def sgteTexto(id):
#     objeto = Certificado.objects.get(documentoDatos=id)
#     archivo = pd.read_csv(objeto.documentoDatos, sep=";",
#                         encoding='utf-8')
#     datos = archivo["Nombres"].to_list()
#     cualidades = archivo ["Cualidades"].to_list()
#     tipo_letra = ImageFont.truetype(objeto.tipoLetra,35)
#     for i in range(len(datos)):
#         certificado = Image.open("media/generadosAutomaticos/"+datos[i]+".jpg")
#         nuevo = ImageDraw.Draw(certificado)
#         coordenadas = (756,842)
#         color_texto = hexToRGB(objeto.colorTexto)
#         nuevo.text(coordenadas, cualidades[i], fill=color_texto, font=tipo_letra,align="left")
#         certificado.save("media/generadosAutomaticos/"+datos[i]+".pdf")
#         nombreRAR = "Certificados"+str(objeto.id)+".rar"
#         with ZipFile("media/"+nombreRAR, "a") as myZip:
#             myZip.write("media/generadosAutomaticos/"+datos[i]+".pdf")
#         archivoGenerado = ArchivosGenerados()
#         archivoGenerado.nombreID = id
#         archivoGenerado.docGenerado = "generadosAutomaticos/"+datos[i]+".pdf"
#         archivoGenerado.save()
#     objeto.archivoRAR = nombreRAR
#     objeto.save()
