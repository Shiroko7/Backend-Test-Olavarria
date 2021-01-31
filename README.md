# Cornershop's Backend Test


## Descripción e Instrucciones


Sobre Requerimientos:

Nora quiere:
- Crear un menú para una fecha específica: 
  
Requiere iniciar sesión https://localhost:8000/login, (credenciales de prueba en create_nora.py user:Nora,pw:1234 ). Luego dirigirse a https://localhost:8000/mealmngmt/create-menu para crear un menu. 

Hay un sencillo navbar para navegar, se incluye una lista de menus creados y drento de los detalles se ven las solicitudes recibidas y se edita el recordatorio/menu.

- Mandar un recordatorio de Slack con el menu del día a todos los empleados en chile.

Se crea automaticamente al crear un menú. Modificable en el enlace del menú: https://localhost:8000/mealmngmt/menu-details/xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx. Implementado con apscheduler, asyncio y slack_sdk. Se detiene cuando no esta en un intervalo de tiempo definido en settings.py

  
El empleado quiere:  
- Elegir su menú preferido (until 11 AM CLT):
  
Los empleados en slack recibiran un mensaje del bot con una dirección url donde pueden realizar un pedido. La url de prueba es: https://localhost:8000/mealmngmt/menu/xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx, no requiere autentificación. El menu se bloquea dependiendo de la hora. Dentro de settings.py se configura el intervalo.

- Requerir especificaciones adicionales (ej: ensalada sin tomates): 
  
Se incluye dentro del formulario del pedido.

## Instalación

Installar dependencias:
```python
pip install -r requirements.txt 
``` 

Migrar esquema y crear usuario para Nora:
```
python manage.py makemigrations
python manage.py migrate
python manage.py shell < create_nora.py
```

Probar la implementación:
```python
python manage.py runserver --noreload
``` 

Felipe Olavarría Riquelme
