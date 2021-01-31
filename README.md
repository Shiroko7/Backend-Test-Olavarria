# Cornershop's Backend Test


## Indicaciones Generales:


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



## Estructura

MainProject:

- BackendTest:
  - settings.py
    - AUTH_USER_MODEL = 'mealmngmt.User', modelo de usuario usado para el autentificador.
    - LOGIN_REDIRECT_URL = '/mealmngmt/create-menu', url donde se redirige luego de iniciar sesión.
    - SLACK_TOKEN: Token para la app de SLACK.
    - SCHEDULER_CONFIG: Configuración del scheduler.
    - OPEN_HOUR = 7, hora donde trabaja el schedueler y se pueden recibir pedidos de menus.
    - CLOSE_HOUR = 11, hora donde se deja de invocar al scheduler y se dejan de recibir pedidos de menus.
  - urls.py: ruteo principal, contiene el homeview, login y logout. Se delega el resto de urls dentro de mealmgnt.
- mealmgntmt:
   - apps.py
      - ```python
         def ready(self):
         ```
          Invoca al scheduler al comenzar la aplicación.
  - models.py
    - ```python
         class User(AbstractUser):
             pass
        ```
        Solo hereda la clase abstracta de django, usada para la autentificación.
    - ```python
         class MealManager(models.Model):
        ```
        Usuario que maneja los menus y tiene acceso a los requests.
    - ```python
         class Menu(models.Model):
        ```
        Representación de un menú. Sus campos son message(str): menu del día, date(datetime): fecha del menú y mealmanager(class MealManager foreingkey): Usuario MealManager que lo crea.
    - ```python
         class MenuRequest(models.Model):
        ```
       Representación de la solicitud de un menú del día. Sus campos son: first_name(str): Nombre de la persona, last_name(str): apellido de la persona, option(str): Elección personal, customization(str): Indicaciones personales sobre la solicitud, Menu (class Menu foreingkey) UIID del menú que se requiere el almuerzo.
  - forms.py
    - ```python
         class CreateMenuModelForm(forms.ModelForm):
        ```
      ModelForm que toma los campos de message(str) y date(datetime) del usuario. El campo de MealManager se deduce del estado de la sesión en MenuCreateView.
    - ```python
         class CreateMenuRequestModelForm(forms.ModelForm):
        ```
       ModelForm que toma los campos de first_name(str), last_name(str), option(srt), customization(str). El campo de menu (UUID) se obtiene de la URL del pedido en MenuRequestView.
    - ```python
         class SchedulerForm(forms.Form):
        ```
      Form usado para obtener los datos en caso de querer modificar el recordatorio de SLACK. Sus campos son: initial_time (int) y final_time(int) el intervalo donde la tarea se corre periódicamente, interval (int): cada cuantos minutos se envia el recordatorio.
  - views.py
    - ```python
         class HomeView(generic.TemplateView):
        ```
        Simplemente muestra el navbar de la app. No requiere autentificación.
    - ```python
         class MenuCreateView(generic.CreateView):
        ```
        Crea los menus diarios. Requiere autentificación. Usa el modelform CreateMenuModelForm. Se redifine get_context_data(self, **kwargs) para poblar la vista con la información que crea. Esto es dos enlces para compartir el menú o modificarlo, identificados con su UUID recien creada. detaillink. El método form_valid(self,form) se sobreescribre para añadir datos de sesión en el formulario, actualizar la vista y programar el trabajo de slack para recordar.
    - ```python
         class MenuListView(generic.ListView):
        ```
        Enumera los menus creados a la fecha. Requiere autentificación.
    - ```python
         class MenuDetailView(generic.FormView):
        ```
        Muestra los detalles asociados al menú de un UUID junto con todos los pedidos asociados a el. Requiere autentificación. get_context_data(self, **kwargs) recupera la info del menú con su pk=uuid y todas los pedidos. form_valid(self,form) usa el form SchedulerForm, reemplazando el task existente con los campos nuevos.
    - ```python
         class MenuRequestView(generic.CreateView):
        ```
        Muestra el menú y un formulario para hacer el pedido. No requiere autentificación.get_context_data(self, **kwargs) consigue la información del menú y determina si se esta permitido solicitar el pedido o no (fijandose en los valores de OPEN_HOUR y CLOSE_HOUR en settings.py). form_valid(self,form) se sobreescribe para añadir el valor del menu de la sesión y añadir un mensaje de confirmación de pedido.
  - urls.py: ruteo dentro de mealmngnt, aquí se definen que vistas requieren autentificación y cuales no. create-menu, menu-list y menu-details requieren autentificación, menu no lo requiere.
  - scheduler
    - scheduler.py
      - ```python
          async def post_message(message): 
        ```
        Su función es mandar mensajes asincronicamente a SLACK. 
      - ```python
            def slack_reminder(start=settings.OPEN_HOUR, end=settings.CLOSE_HOUR, url="beep boop", job_id="slack_reminder"):
          ```
          start: Desde que hora se puede correr la tarea.

          end: Hora en la que se termina de correr la tarea.

          url: url del menú el cual se requiere recordar.
          
          job_id: identificador de la tarea, usado para terminarla en ejecución.

          Esta función es la tarea recurrente que se corre dentro del scheduler. Convoca la función post_message() cuando es llamada por el scheduler. Cuando detecta que el intervalo de tiempo no es valido, se libera su trabajo del scheduler.

      - ```python
           def start():
          ```
          Empieza el scheduler, llamado en apps.py.

  - tests
    - test_forms.py: Se prueban que las formas se comporten correctamente en el caso que sean validas y no lo sean.
    - test_models.py: Se prueba que se adhieran correctamente los componentes a la base de datos.
    - test_urls.py: Se prueban que esten correctamente utilizadas las rutas.
    - test_views.py: Para cada modelo se prueba que la función get funcione y que devuelva el template correcto. Se prueba el correcto funcionar de los formularios froms en las vistas que lo usan.
  - templates/mealmngmt: templates html usados por las vistas de la aplicación mealmngmt. 

- templates: templates generales usados de base/navbar y login.
        
    
        