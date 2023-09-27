
# hay que agregar la CA al cacert.pem en el directorio de certifi del venv creado
import certifi
import sys
import argparse

from functions import *
from notif import *

parser = argparse.ArgumentParser(prog='docker_registry_cleaner')
parser.add_argument('--reg', type=str, dest='registry_host', required=True, help='registry para el borrado desde %(prog)s')
#parser.add_argument('--env', type=str, dest='env', choices=["dev", "test", "prod"], required=True, help='ambiente para ser ejecutado por %(prog)s')
parser.add_argument('--n', type=int, dest='number', required=True, default=10, help='cantidad de imagenes para ser retenida por %(prog)s ')
args = parser.parse_args()

## props
#registry_host  = "https://xxxx.xxx.xxx:5001"
#repo_name = "repo_name"
#N = 0  
output_file = "./eliminados.txt"  # Nombre del archivo de resultados
#env = "dev" # ambiente a impactar

## Obtener la URL base del repositorio en el registro Docker
#repo_url = f"{registry_host}"
mensaje = f"Comenzo el script de borrado en {args.registry_host}"
#teams_notifi({"title": "Borrado de imagenes docker", "themeColor": "FFF300", "text": mensaje})

## Obtener la lista de imagenes del repositorio
try:
    imgs_data = catalogo(args.registry_host)
    #print (imgs_data)
except Exception as e:
    mensaje = f"Ha fallado el script al traer el catalogo con: {e}"
    #teams_notifi({"title": "Borrado de imagenes docker", "themeColor": "FF0000", "text": mensaje})
    sys.exit(1)

## Llamada para generar la lista de imagenes ordenada por fecha
try:
    t_ordenadas , manifiestos_borrados = getSortedList(imgs_data, args.number, args.registry_host, args.env)
    #print(t_ordenadas)
except Exception as e:
    mensaje = f"Ha fallado el script al traer la lista de imagenes con: {e}"
    #teams_notifi({"title": "Borrado de imagenes docker", "themeColor": "FF0000", "text": mensaje})
    sys.exit(1)

## Llamada al borrado de la lista de las z imagenes viejas de cada tipo
try:
    m_borrados = toDelete(t_ordenadas, manifiestos_borrados, output_file, args.registry_host)
except Exception as e:
    mensaje = f"Ha fallado al borrar las imagenes con: {e}"
    #teams_notifi({"title": "Borrado de imagenes docker", "themeColor": "FF0000", "text": mensaje})
    sys.exit(1)


## Notifico que termino el script 
mensaje = f"Finalizo el script de borrado en {args.registry_host}"
#teams_notifi({"title": "Borrado de imagenes docker", "themeColor": "00FF00", "text": mensaje})



