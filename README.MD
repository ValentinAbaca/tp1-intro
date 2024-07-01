# Guerreros Z

  

Un pequeño juego con una wiki integrada de algunos personajes de Dragon Ball Z

  

___

## Creacion base datos

  

Deberas tener postgreSQL instalado, puedes obtener informacion de instalacion en la [web de postgres](https://www.postgresql.org/)

  
  

## Clonar el repositorio

  

Para clonar el repositorio escribe en una terminal:

  

```

git clone https://github.com/ValentinAbaca/tp1-intro

```

  

Después metete a la carpeta que se te crea

  

```

cd ./tp1-intro

```

  

Ahora desde esta ubicación estas listo para continuar a la instalación.

  
  

## Instalación web

  

Asegurate de crear un archivo de variables de ambiente con las credenciales de tu base de datos.

  

Puedes ver un archivo de ejemplo, copia el contenido de este archivo.

  

```

cp backend/.env.example backend/.env
```

Y asegurate de cambiar los valores con los datos de tu base de datos en el archivo .env .

  

Dependiendo tu version de python deberas utilizar python o python3

  

Para la Instalación del proyecto primero crearemos un venv de python de la siguiente forma

  
  

```

python3 -m venv venv

```

  

Luego lo activamos de la siguiente forma

  

```

source venv/bin/activate

```

  

Una vez dentro instalaremos los requerimientos necesarios.

  

```

pip install requeriments.txt

```

  

Ya estaria listo para ser utilizado!!

___

## Correr

  

Para correr el proyecto debemos tener dos terminales y activamos dentro de ellas el venv con el siguiente comando

  

```

source venv/bin/activate

```

  

Para levantar el servidor backend en una de las terminales debejos ejecutar:

```

cd backend/

python3 app.py

```

El servidor ya esta corriendo en el puerto 5000 puedes acceder a el mediante el siguiente [link](http://localhost:5000)

  

Para levantar el servidor frontend en una de las terminales debejos ejecutar:

  

```

cd frontend/

python3 -m http.server

```

El servidor ya esta corriendo en el puerto 8000 puedes acceder a el mediante el siguiente [link](http://localhost:8000)  
