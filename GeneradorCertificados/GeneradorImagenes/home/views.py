from django.shortcuts import render
from django.http import HttpResponse
from home.models import Certificado,ArchivosGenerados
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from datetime import datetime
from zipfile import *
# Create your views here.



def home(request):
    return render(request, "home.html")


def certificado(request):
    certificado = False
    id = ""    
    if request.POST: 
        plantilla = Certificado() 
        plantilla.imagen = request.FILES.get("imgPC")
        plantilla.documentoDatos = request.FILES.get("infoCertificado")
        id = plantilla.documentoDatos
        plantilla.coordenadaX = request.POST.get("coordenadaX")
        plantilla.coordenadaY = request.POST.get("coordenadaY")
        if (request.POST.get("exampleRadios") == "postON"):
            plantilla.isPost = True
        else:
            certificado = True
            plantilla.isCertificado = True

        plantilla.tipoLetra = request.FILES.get("typeTXT")
        plantilla.colorTexto = request.POST.get("colorTXT")
        plantilla.tamanioTexto = request.POST.get("tamanioTXT")
        plantilla.save()
    if certificado:
        generarCertificado(certificado,id)
        Archivo = Certificado.objects.get(documentoDatos = id)
        return render(request,"descarga.html",{"objeto":Archivo})
    else:
        return HttpResponse("Generando los post...")


def generarCertificado(isPdf,id):
    objeto = Certificado.objects.get(documentoDatos = id)
    datos = pd.read_csv(objeto.documentoDatos, sep=",")["Nombres"].to_list()
    tipo_letra = ImageFont.truetype(objeto.tipoLetra, objeto.tamanioTexto)
    for nombre in datos:
        certificado = Image.open(objeto.imagen)
        nuevo = ImageDraw.Draw(certificado)
        coordenadas = (objeto.coordenadaX, objeto.coordenadaY)
        color_texto = hexToRGB(objeto.colorTexto)
        nuevo.text(coordenadas, nombre, fill=color_texto, font=tipo_letra)
        if isPdf:
            certificado.save("media/generadosAutomaticos/"+nombre+".pdf")
            nombreRAR ="Certificados"+str(objeto.id)+".rar"
            with ZipFile("media/"+nombreRAR,"a") as myZip:
                myZip.write("media/generadosAutomaticos/"+nombre+".pdf")
            archivoGenerado = ArchivosGenerados()
            archivoGenerado.nombreID = id
            archivoGenerado.docGenerado =  "generadosAutomaticos/"+nombre+".pdf"
            archivoGenerado.save()
        else:
            certificado.save("media/jpg/"+nombre+".jpg")
    objeto.archivoRAR =nombreRAR
    objeto.save() 

def hexToRGB(hexa):
    red = hexa[1:3]
    green = hexa[3:5]
    blue = hexa[5:]

    return (hexToDec(red), hexToDec(green), hexToDec(blue))

def hexToDec(hexNumber):
    dic = {"a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15}
    decimalValue = 0
    count = len(hexNumber)-1
    for i in hexNumber:
        if i.isdigit():
            decimalValue += (int(i)*(16**count))
        else:
            num = dic[i]
            decimalValue += (int(num)*(16**count))
        count-= 1

    return decimalValue

