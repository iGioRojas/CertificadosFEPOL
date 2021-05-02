from django.shortcuts import render
from django.http import HttpResponse
from home.models import Certificado,ArchivosGenerados
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from datetime import datetime
from zipfile import *
import requests
# Create your views here.



def home(request):
    return render(request, "home.html")


def certificado(request):
    certificado = False
    id = ""    
    if request.POST: 
        plantilla = Certificado() 
        plantilla.imagen = request.FILES.get("imgPC")
        print(plantilla.imagen)
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
        plantilla.urlSpotify=request.POST.get("cancion")
        plantilla.save() #ORM
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
        nom=guardaImg(objeto.urlSpotify)
        qr=Image.open("media/plantillas/"+nom+".png")
        certificado = Image.open(objeto.imagen)
        certificadoW=certificado.size[0]
        certificadoH=certificado.size[1]
        qrsize=(int(qr.size[0]/3.5),int(qr.size[1]/3.5))
        qr=qr.resize(qrsize,Image.ANTIALIAS)
        ubicacion= (int(certificadoW/2)-int(qrsize[0]/2),certificadoH-70)
        print(ubicacion,qrsize)
        certificado.paste(qr,ubicacion)
        nuevo = ImageDraw.Draw(certificado)
        coordenadas = (objeto.coordenadaX, objeto.coordenadaY-objeto.tamanioTexto+10)
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
    objeto.archivoRAR = nombreRAR
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

def guardaImg(url):
    url=qrSpotify(url)
    url_imagen = url # El link de la imagen
    nombre=url[url.find("/"):].replace("/","").replace(".","").replace(":","")
    nombre_local_imagen = "media/plantillas/"+nombre+".png" # El nombre con el que queremos guardarla
    imagen = requests.get(url_imagen).content
    with open(nombre_local_imagen, 'wb') as handler:
        handler.write(imagen)
        return nombre
    
def urispotify(link):
    ini = link.find("spotify")
    end = link.find("?")
    print(ini,end)
    link=link[ini:end]
    link=link.replace(".com","")
    link=link.replace("/",":")
    return link

def qrSpotify(link):
    uri=urispotify(link)
    url="https://scannables.scdn.co/uri/plain/png/ffffff/black/640/"+uri
    return url
          