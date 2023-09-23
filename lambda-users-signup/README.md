# Función Lambda para registro de usuarios

* Se debe instalar los paquetes de psycopg2 con: `pip install aws-psycopg2 -t .`  
Esto crea los paquetes de instalación de psycopg2 en la raiz del proyecto.

* se debe subir un archivo comprimido en 'AWS Lambda' en donde este la función junto a los paquetes que se instalaron en el paso anterior.

* Se debe tener en cuenta que la función se debe configurar para que reciba automaticamente los mensajes de la cola de mensajería, para ello se configura que el "Trigger" de la función Lambda sea una cola SQS.

* Para su correcto funcionamiento, se debe crear en la función las siguientes variables de entorno:
    * USER_NAME = Nombre de usuario de la base de datos
    * PASSWORD = Constraseña de la base de datos
    * RDS_PROXY_HOST = URL o proxy de la base de datos
    * DB_NAME = Nombre de la base de datos