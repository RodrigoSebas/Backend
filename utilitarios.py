from math import ceil
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from os import environ
from cryptography.fernet import Fernet

def serializadorPaginacion(total:int,pagina:int,porPagina:int):
    itemsPorPagina = porPagina if total >= porPagina else total

    totalPaginas = ceil(total/itemsPorPagina) if itemsPorPagina > 0 else None
    paginaPrevia = pagina-1 if pagina>1 and pagina<=totalPaginas else None
    paginaSiguiente = pagina+1 if totalPaginas > 1 and pagina<totalPaginas else None

    return {
        "itemsPorPagina":itemsPorPagina,
        "totalPaginas":totalPaginas,
        "total":total,
        "paginaPrevia":paginaPrevia,
        "paginaSiguiente":paginaSiguiente,
        "porPagina": porPagina,
        "pagina":pagina
    }

def enviarCorreo(destinatario, titulo, texto, html):
    if not destinatario:
        print("Es necesario el correo")
        return
    
    emailEmisor = environ.get("CORREO_EMISOR")
    passwordEmisor = environ.get("PASSWORD_CORREO_EMISOR")

    cuerpo = MIMEText(texto, 'plain')

    cuerpoHtml = MIMEText(html, 'html')

    correo = MIMEMultipart('alternative')

    correo['Subject'] = titulo

    correo['To'] = destinatario

    correo.attach(cuerpo)
    correo.attach(cuerpoHtml)

    emisor = SMTP(environ.get("CORREO_HOST"), 587)

    emisor.starttls()
   
    emisor.login(emailEmisor, passwordEmisor)

    emisor.sendmail(from_addr=emailEmisor, to_addrs=destinatario, msg=correo.as_string())

    emisor.quit()

    print("Correo enviado exitosamente")


def encriptarTexto(texto):
    fernet = Fernet(environ.get("FERNET_KEY"))

    textoEncriptado = fernet.encrypt(bytes(texto, 'utf-8'))

    return textoEncriptado.decode('utf-8')    

def desencriptarTexto(textoEncriptado):
    print(textoEncriptado)
    fernet = Fernet(environ.get("FERNET_KEY"))
    texto = fernet.decrypt(textoEncriptado)

    return texto
