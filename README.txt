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
El programa se hizo en base a el ebnf entregado siguiendo por completo este, de forma que hay varios casos en los que se hicieron supuestos segun lo entregado.

1- Estilo de nombres de variables: Segun el ebnf entregado, los distintos casos nombres de funciones snake_case, camelCase y PascalCase se construyen con letra_min y letra_may, por lo que cualquier funcion o variable escrita con numeros o caracteres especiales rompen con la regla del ebnf, 
   he hecho algunos patrones para que el programa las detecte, aunque no este especificado en el ebnf entregado. Se detectan como "desconocido"

2- Salida por terminal practicante desconocido: No sale explicito en el pdf entregado como instruccion pero asumi que el practicante en el reporte "desconocido" tambien se entrega por el reporte de terminal, aparte de
   hacerle el desconocido.txt

3- Errores de sintaxis estructuras de control: Segun el ebnf entregado se hace la declaracion de estructuras de control pero no se especifica bien en el pdf si se debe considerar como error de sintaxis el mal uso de la estructura de control
   pero asumi que hay que tenerlos en cuenta, para mostrarlos en terminal el formato que se debe usar tampoco se especifico por lo que utilice uno que se me hiciera comodo.

4- Declaraciones de variables vacias: Segun el ebnf entregado la declaracion de una variable tiene que tener asignado un valor por lo que variables declaradas como por ejemplo: "int numero;", el programa las ignorara y no las contara como
   variables declaradas, aunque en c++ si lo sean por el ebnf entregado no se contaran.

5- Cadenas de texto strings y caracteres char: Revisando el ebnf, una cadena_texto exige que adentro vaya una palabra. Como la regla de palabra no incluye espacios y obliga a empezar siempre con una letra, el programa ignora cualquier string que tenga espacios como por ejemplo: "hola mundo" o que empiece con numeros como por ejemplo: "123hola"
   ya que son invalidos gramaticalmente. Para los char ocurre lo mismo la regla dice que solo aceptan una letra asi que si se declara algo como char x = '1'; o un espacio en blanco, la linea se descartara por completo. 

6- Retornos de funciones: Segun el ebnf entregado, el retorno exige que lo que se devuelva sea un nombre_valido. Si se intentara retornar un valor directo como 5 o false, el programa lo ignorara y simplemente evaluara si contiene ; a retornos de variables

7- Numeros negativos: Segun el ebnf entregado, un numero es una sucesion de digitos, el signo "-" es categorizado como una operacion, por lo tanto tratar de declarar algo con algun numero negativo causara que el programa ignore esta variable.

8- Operaciones permitidas: La regla de operacion entregada en el ebnf agrupa todos los simbolos. por esto el programa procesara como una declaracion valida algo como "int hola > 5" o algo "bool verdad == true", ya que en teoria segun el ebnf entregado cumple con la gramaticalmente correctamente.

