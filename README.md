[![wakatime](https://wakatime.com/badge/user/54d759a2-12d9-48b4-9e4e-88518abe7706/project/95af36b6-344b-4adb-8df2-96a3b6d8533b.svg)](https://wakatime.com/badge/user/54d759a2-12d9-48b4-9e4e-88518abe7706/project/95af36b6-344b-4adb-8df2-96a3b6d8533b)

# Acceder a la documentación de la API

La documentación de la API está desplegada en la siguiente dirección IP:
[Deco-Hogar](http://206.81.9.7/docs)

En la documentación de la API, podrás encontrar toda la información necesaria para consumir los endpoints de la aplicación. También podrás realizar pruebas de las diferentes funcionalidades de la API directamente desde la página de documentación.

# Cómo ejecutar el proyecto de manera local

## Requisitos previos
- Tener Python 3.6 o superior instalado en tu computadora
- Tener pip instalado en tu computadora

## Instalación

1. Clona el repositorio en tu computadora.
2. Abre una terminal y navega a la carpeta donde clonaste el repositorio.
3. Instala las dependencias del proyecto con el siguiente comando:
    - `pip install -r requirements.txt`
    
## Ejecución

4. En la misma terminal, navega a la carpeta donde se encuentra el archivo main.py.
5. Ejecuta el siguiente comando para iniciar el servidor:
      - `uvicorn main:app --reload`
6. Abre un navegador web y accede a la siguiente URL:
      - `http://localhost:8000/docs`

Esto abrirá la documentación de la API de FastAPI, donde puedes probar los endpoints de la aplicación.

