Nombre alumno: Emilio Alfonso Araya Guzman
Rol alumno: 202473561-6

Tenemos el archivo principal para el funcionamiento del programa "Evaluador.py"

Instrucciones de uso para el .py:
-Necesitamos primero los archivos correspondientes en el entorno para que el programa funcione, los cuales son "Evaluador.py" y "programa.txt"
 que el programa.txt contiene el texto del codigo de c++ correspondiente. Es de suma importancia que ambos archivos se encuentren en el mismo entorno
 para el funcionamiento del programa.

-Evaluador.py se desarrollo en python 3.12.3 por lo cual se recomienda esta version para asegurarse que el programa funcionara correctamente

-Para ejecutar el programa hay dos opciones, una es abrir la terminal  con el siguiente comando (importante estar en el entorno correcto): "python Evaluador.py"
 la otra opcion es en Visual Studio Code estando en el entorno correspondinte en la pestaña de Evaluador.py clickear en el icono de "Play" que para el testing se uso este metodo
 cualquiera de los dos metodos servira

-Una consideracion importante es que el programa se probo en todo momento usando la WSL de Ubuntu, es decir un entorno de Linux, se recomienda usar este para
 el programa.

Resultados y terminal:
-El programa al ejecutarse entregara en terminal las estadisticas por funcion, con la cantidad de variables declaradas, errores de sintaxis, diferencias de estilo, todo esto lo hace por cada estilo
 aparte genera archivos distintos segun cada estilo, con sus respectivos nombres en .txt

Consideraciones importantes! : 
El programa se hizo en base a el ebnf entregado siguiendo por completo este, de forma que hay varios casos en los que se hicieron asumsiones segun lo entregado.

1- Estilo de nombres de variables: Segun el ebnf entregado, los distintos casos nombres de funciones snake_case, camelCase y PascalCase se construyen con letra_min y letra_may, por lo que cualquier funcion o variable escrita con
   algun digito [0-9] no sera valida un ejemplo de esto podria ser int hola1 = 1; esto el programa lo ignora

