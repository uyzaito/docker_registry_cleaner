Proyecto desarrollado en Python 3.9.16 (main, May 29 2023, 00:00:00) 

Script para el borrado de imagenes en cualquier docker registry 

Elimina las mas antiguas por cada nombre de imagen conservando las n ultimas, para la autenticacion contra el registry hay que editar auth del dockerV2.py

Hay que tener en cuenta que despues de correr el script hay que correr una garbage collector para liberar el espacio