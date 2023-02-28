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

