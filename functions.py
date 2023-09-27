import datetime
import bisect

from dockerV2 import *

def getSortedList(imgs_data, n, repo_url, env):
    tags_by_name = {}
    manifiestos_borrados = []
    for img in imgs_data:
        all_tags = traerTags(repo_url, img)
        # Longitud para calcular el resto de n para el borrado
        m = len(all_tags['tags'])
        tags_fechas = [] 
        for tag in all_tags['tags']:
            #Control de codigo de estado del tag
            head = traerManifiesto(repo_url, img, tag)
            if head.status_code == 200:
                print ("El asset" , img, tag, " devolvio status code: 200")
                head = head.headers
                print ("Head---->", head)
                date = datetime.datetime.strptime(head["Last-Modified"].split(",")[1], " %d %b %Y %H:%M:%S GMT")
                sha =  head["Docker-Content-Digest"]
                bisect.insort(tags_fechas, (date, tag, sha))
                tags_by_name[img] = tags_fechas
            else:
                print ('Hay error en el asset ',img ,tag, " con status code: ", head.status_code )
                #hacer que quede primero en la lista del borrado
                m =- 1
                manifiestos_borrados.append((img, tag, "ERROR-MANIFIESTO", head.status_code))
        # Evaluar la cantidad de tags para ver si hay que borrar tags y quitarlas de la lista
        z = m - n
        if z > 0:
            #Nos quedamos con las primeras z imagenes mas viejas           
            imagenes_removidas = tags_by_name[img][:z]
            tags_by_name[img] = imagenes_removidas          
        elif z <= 0:
            tags_by_name[img] = []
        else:
            pass                   
    return tags_by_name, manifiestos_borrados


# Función para eliminar desde la lista generada
def toDelete(images, manifiestos_borrados, output_file, repo_url):
    with open(output_file, 'w', encoding='utf-8') as f:
        for image in images:
            for tag in images[image]:
                response = borrarManifiesto(repo_url, image, tag[2])
                if response.status_code == 202:
                    success_msg = f"{tag[0]} / Imagen {image}, {tag[1]}, eliminada exitosamente: {response.status_code}\n"
                    print(success_msg)
                    f.write(success_msg)
                    manifiestos_borrados.append((image, tag[1], tag[2], response))
                else:
                    error_msg = f"{tag[0]} / Error al eliminar la imagen {image}, {tag[1]} Código de estado: {response.status_code}\n"
                    print(error_msg)
                    f.write(error_msg)
                    manifiestos_borrados.append((image, tag[1], tag[2], response))
    return manifiestos_borrados