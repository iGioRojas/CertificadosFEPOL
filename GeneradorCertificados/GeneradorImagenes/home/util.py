import requests


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
    link=link[ini:end]
    link=link.replace(".com","")
    link=link.replace("/",":")
    return link

def qrSpotify(link):
    uri=urispotify(link)
    url="https://scannables.scdn.co/uri/plain/png/ffffff/black/640/"+uri
    return url