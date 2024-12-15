# Grup05_projecte
# ProjecteDT


DAW:
Para el apartado de crear un wireframe d'aplicació web en FIGMA lo dividiremos en difentes secciones para que los usuarios que quieran hacer su registro de fichaje puedan llevar un control de fichaje de ellos mismos.
El objetivo és la creación de un sistema de fichaje para una institución donde quede registrado quien entra y sale una persona de una empresa como en el trabajo, lo que haremos es una pagina web donde cuando entren a la pagina puedan registrarse y luego iniciar sesión para asi saber quien esta entrando y que sus datos queden registrados en la base de datos del registro.

1. Para ello empezaremos en la primera pagina que es una bienvenida que da a los usuarios que entren de cual es la función principal de esta pagina que es la de hacer un control de fichaje en tiempo real, y un apartado de contacto por si llegan a tener algun problema a la hora de hacer el registro.

![image](https://github.com/user-attachments/assets/82459c3b-4af1-422a-87b4-9ff95b324db3)



2. En la primera pagina hemos visto que en el apartado del 'HEADER', hay diferentes botones al lado del logo y el nombre de la pagina, tenemos el botón para registrarse o iniciar sesión, para los usuarios que lleguen a la empresa por un ejemplo tendran la opción de 'iniciar sesión' y cuando le dan les aparecera la pagina para iniciar sesión y darle a la opción 'Continuar con Google' y seleccionar su correo de empresa o personal y ya con eso se les hara un registro automaticamente de ese usuario. Y cuando otro dia quieran iniciar sesión otra vez como se le ha cerrado la sesión directamente pone el correo suyo y ya podra acceder.

![image](https://github.com/user-attachments/assets/66c7a1f0-4067-4251-a766-2d8937a4d39d)



3. Si no tenemos una cuenta creada, podemos registrarla con tus datos personales para que queden guardados en la base de datos de la web con sus secciones para poner el nombre, apellidos y mas informaticón tuya, luego aceptar las condiciones de la pagina y un boton que
  dice 'CREA TU CUENTA' que al darle al boton ya tendras hecho el registro con tu correo y ya poder iniciar sesión para poder hacer tu fichaje y se quede guardado en la base de datos en este caso en el historial de registro.
![image](https://github.com/user-attachments/assets/a7f56ddc-49b3-4d1a-802d-73e6612bc906)




4. Una vez que ya hemos el registro y ya podemos acceder al apartado para hacer el registro y mirar el historial de registro, procederemos a ver la funcionalidad de esta pagina y como funciona, vemos que una vez dentro hay un apartado que pone 'Instruccions', que nos explicara como hacer el registro y tendremos dos botones, uno que es para ir a la pagina del registro y el otro es para ver el historial para comprobar que se ha hecho el registro correctamente.
![image](https://github.com/user-attachments/assets/fd72c4b1-b750-4d7e-a091-4b26c578b44e)



5.En este apartado una vez que clicamos en la opción registrar nos aparecera nuestro usuario para que se vea que somos nosotros quien hacemos el fichaje, la fecha y hora a la que se hace el fichaje y ponemos si queremos hacer fichaje de entrada o salida.
![image](https://github.com/user-attachments/assets/ec8a1cc5-98e6-4e99-8b0e-82186a6de3cf)



6.Y por último tenemos el 'Historia de fichaje que es para confirmar que se ha hecho el fichaje correctamente y llevar un control de nuestros ultimos fichajes.
![image](https://github.com/user-attachments/assets/8928d588-7cb0-4caa-8b3a-7b07b77dbefd)




DAM:

Esta aplicación está diseñada para tres tipos de usuarios: **Alumno**, **Profesor** y **Administrador**. Cada tipo de cuenta tiene diferentes permisos y funciones específicas. 

- **Objetivo para el alumno**: Consultar sus registros de asistencia, retrasos, y datos personales.
- **Objetivo para el profesor**: Consultar su información personal, gestionar sus grupos, pasar lista, y administrar su horario.
- **Objetivo para el administrador**: Supervisar los registros de asistencia y gestionar alertas de asistencia para los alumnos.

---

## 1. Funcionalidad del Alumno

Al iniciar sesión, el alumno verá un **calendario** con un resumen de su asistencia, donde se destacan en rojo los días de retrasos o ausencias. También verá su información personal registrada en la base de datos. En el menú superior, dispone de dos opciones principales:

![Imagen del calendario de alumno](https://github.com/user-attachments/assets/28a1886b-1515-4eab-b97d-50e86c9f3875)

### 1.1. Marcajes
En esta sección, el alumno puede consultar sus registros de asistencia. Cada registro muestra la **fecha**, **hora** y el **ID de marcaje**, correspondiente a su tarjeta o chip RFID (cada uno con un ID único).

![Imagen de marcajes](https://github.com/user-attachments/assets/c6b99d87-2b4b-47ba-ad7d-040d00d71612)

---

## 2. Funcionalidad del Profesor

Al iniciar sesión, el profesor verá una **tabla con sus grupos asignados**, donde puede consultar la asistencia de cada grupo, incluyendo el ID del grupo, nombre, y aula asignada. También verá su información personal. En el menú superior, dispone de opciones para **pasar lista** y **consultar horarios**.

![Imagen de grupos del profesor](https://github.com/user-attachments/assets/4b714e26-9509-4a8a-a61a-61eea5a81c6e)

### 2.1. Pasar Lista
En esta sección, el profesor puede pasar lista de asistencia para el grupo seleccionado desde el menú desplegable. La lista es **desplazable**, adaptándose al número de alumnos. En la parte inferior, dispone de dos botones: uno para **modificar la lista** y otro para **guardar** la asistencia.

![Imagen de pasar lista](https://github.com/user-attachments/assets/323ae17e-3b4c-4692-b300-f4088520df1d)

### 2.2. Horarios
En la sección de horarios, el profesor puede ver su horario en forma de tabla, que incluye **hora**, **nombre del curso** y **ID del curso**. Además de visualizar su horario, puede subir uno nuevo mediante un archivo Excel, el cual se almacenará en el servidor al presionar el botón de guardar.

![Imagen de horarios](https://github.com/user-attachments/assets/4ff6d7c3-4762-463e-b155-53cfd36c5df0)

---

## 3. Funcionalidad del Administrador

Al iniciar sesión, el administrador verá una **tabla con los marcajes recientes** que muestra el ID y fecha de cada registro de asistencia. En el menú superior, dispone de tres opciones principales:

![Imagen de la vista del administrador](https://github.com/user-attachments/assets/335c63d3-7557-4a94-a27b-5063feeac273)

### 3.1. Editar Marcaje
En esta sección, el administrador puede modificar el estado de los marcajes (presencia, ausencia, retraso). También puede **notificar al alumno** en caso de excesivas ausencias o retrasos. Los cambios solo se guardarán al presionar el botón de guardar.

![Imagen de editar marcaje](https://github.com/user-attachments/assets/84615e49-46ff-41ea-90e0-437be3f863f3)

### Otras Funcionalidades
Además de las funcionalidad de ediatr marcaje, el administrador tiene acceso a las mismas opciones que los usuarios **Alumno** y **Profesor** (pasar lista y horarios).

---
## Enlace Figma
https://www.figma.com/design/Pzd7ATRbGheYRKQswwkhY5/Wireframe-projecte?node-id=1-2&t=qHNvOIDonUpMxWAL-1
