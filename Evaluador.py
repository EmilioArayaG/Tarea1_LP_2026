import re

digito = r"[0-9]"
letra_min = r"[a-z]"
letra_may = r"[A-Z]"
letra = rf"(?:{letra_min}|{letra_may})"
palabra = rf"{letra}(?:{letra}|{digito})*"

operacion = r"(?:\+|-|/|\*|==|=|<|>)"
booleano = r"(?:true|false)"
cadena_texto = rf'"{palabra}"'
caracter = rf"'{letra}'"
valor = rf"(?:{digito}+|{booleano}|{cadena_texto}|{caracter})"
tipo_dato = r"(?:int|bool|char|string|void)"

snake_case = rf"{letra_min}+(?:_{letra_min}+)+"
camelCase = rf"{letra_min}+(?:{letra_may}+{letra_min}+)+"
PascalCase = rf"(?:{letra_may}+{letra_min}+)+"
nombre_valido = rf"(?:{snake_case}|{camelCase}|{PascalCase})"

nombre_generico = rf"(?:{letra}|{digito}|_)+"

condicion = rf"(?:\(\s*{nombre_valido}\s*{operacion}\s*{valor}\s*\))"
estructura_control = rf"(?:(?:if|while)\s+{condicion}\s*\{{)"
cierre_bloque = r"\}"
detector_funcion = rf"(?:{tipo_dato})\s+({nombre_valido})\s*\("
detector_funcion_desconocido = rf"(?:{tipo_dato})\s+({nombre_generico})\s*\("
declaracion_variable = rf"(?:{tipo_dato})\s+({nombre_valido})\s*(?:{operacion})\s*(?:{valor})\s*;"
retorno = rf"(?:\s*return\s+{nombre_valido}\s*;)"
comentario_one_line = rf"//\s*{palabra}"
comentario_multi_line = rf"/\*\s*{palabra}\s*\*/"

variable_sin_punto_coma = rf"^(?:{tipo_dato})\s+({nombre_valido})\s*(?:{operacion})\s*(?:{valor})\s*[^;]$"
retorno_sin_punto_coma = rf"^\s*return\s+(?:{nombre_valido})\s*[^;]$"

def determinar_autor(nombre_funcion):
    '''
    ***
    Parametro: nombre_funcion: str que contiene el nombre de la funcion
    ***
    Retorno: str
    ***
    Evalua el nombre de la funcion y retorna al que pertenece
    '''
    if re.fullmatch(snake_case, nombre_funcion):
        return "snake"
    elif re.fullmatch(camelCase, nombre_funcion):
        return "camel"
    elif re.fullmatch(PascalCase, nombre_funcion):
        return "pascal"
    else:
        return "desconocido"

def incializar_archivos():
    '''
    ***
    Parametro: None
    ***
    Retorno: Diccionario de estadisticas
    ***
    Esta funcion crea los archivos de salida (snake.txt, camel.txt, pascal.txt y desconocido.txt)
    y crea un diccionario de estadisticas. 
    '''
    archivos_salida = ['snake.txt', 'camel.txt', 'pascal.txt', 'desconocido.txt']
    for archivo in archivos_salida:
        with open(archivo, 'w', encoding='utf-8') as f:
            pass
    estadisticas = {
        "snake": {"funciones": [], "total_variables": 0, "errores_estilo": [], "errores_sintaxis": []},
        "camel": {"funciones": [], "total_variables": 0, "errores_estilo": [], "errores_sintaxis": []},
        "pascal": {"funciones": [], "total_variables": 0, "errores_estilo": [], "errores_sintaxis": []},
        "desconocido": {"funciones": [], "total_variables": 0, "errores_estilo": [], "errores_sintaxis": []}
    }
    return estadisticas

def escribir_bloque(contexto_actual, bloque_actual):
    '''
    ***
    Parametro 1: contexto_actual: str
    Parametro 2: bloque_actual: list
    ***
    Retorno: none
    ***
    Esta funcion abre el archivo del autor correspondiente y escribe las lineas que se acumularon.
    '''
    with open(f'{contexto_actual}.txt','a',encoding='utf-8') as f:
        f.writelines(bloque_actual)
        f.write('\n')

def evaluar_linea_interna(linea_limpia, contexto_actual, estadisticas):
    '''
    ***
    Parametro 1: str
    Parametro 2: str
    Parametro 3 : dict
    ***
    Retorno: none
    ***
    Esta funcion evalua una linea dentro de un bloque de funcion, busca las variables, errores de 
    estilo y los errores de sintaxis. Tambien actualiza el diccionario de estadisticas con la informacion obtenida.
    '''
    for var_match in re.finditer(declaracion_variable, linea_limpia):
        nombre_variable = var_match.group(1)
        estadisticas[contexto_actual]["total_variables"] += 1
        estilo_variable = determinar_autor(nombre_variable).lower()
        if estilo_variable != contexto_actual:
            if contexto_actual == "snake":
                estilo_impresion = "snake_case"
            elif contexto_actual == "camel":
                estilo_impresion = "camelCase"
            elif contexto_actual == "pascal":
                estilo_impresion = "PascalCase"
            else:
                estilo_impresion = "desconocido"
            mensaje_error = f"La variable '{nombre_variable}' no es {estilo_impresion}"
            estadisticas[contexto_actual]["errores_estilo"].append(mensaje_error)

    funcion_actual = estadisticas[contexto_actual]["funciones"][-1]
    match_var_rota = re.match(variable_sin_punto_coma, linea_limpia)
    
    if match_var_rota:
        estadisticas[contexto_actual]["total_variables"] += 1
        mensaje_error = f"Error en '{funcion_actual}': Falta ';' en la linea '{linea_limpia}'"
        estadisticas[contexto_actual]["errores_sintaxis"].append(mensaje_error)
    elif re.match(retorno_sin_punto_coma, linea_limpia):
        mensaje_error = f"Error en '{funcion_actual}': Falta ';' en la linea '{linea_limpia}'"
        estadisticas[contexto_actual]["errores_sintaxis"].append(mensaje_error)
def procesar_archivo():
    '''
    ***
    Parametro: None
    ***
    Retorno: None
    ***
    Esta funcion lee el archivo programa.txt linea por linea, detecta las funciones, acumula las lineas de cada bloque de funcion y las escribe en el archivo correspondiente.
    '''
    estadisticas = incializar_archivos()

    contexto_actual = None
    bloque_actual = []
    contador_llaves = 0

    with open('programa.txt', 'r', encoding='utf-8') as archivo:
        for linea in archivo: 
            linea_limpia = linea.strip()

            if not linea_limpia:
                continue

            match_funcion = re.search(detector_funcion, linea_limpia)
            if not match_funcion:
                match_funcion = re.search(detector_funcion_desconocido, linea_limpia)
            
            if match_funcion:
                if contexto_actual is not None and contador_llaves > 0:
                    funcion_anterior = estadisticas[contexto_actual]["funciones"][-1]
                    mensaje = f"Error en '{funcion_anterior}': Bloque sin cerrar. Faltan {contador_llaves} llaves '}}' de cierre."
                    estadisticas[contexto_actual]["errores_sintaxis"].append(mensaje)
                    escribir_bloque(contexto_actual, bloque_actual)

                nombre = match_funcion.group(1)
                contexto_actual = determinar_autor(nombre).lower()
                estadisticas[contexto_actual]["funciones"].append(nombre)
                
                bloque_actual = [linea]
                contador_llaves = linea_limpia.count('{') - linea_limpia.count('}')
                
            elif contexto_actual:
                bloque_actual.append(linea)
                evaluar_linea_interna(linea_limpia, contexto_actual, estadisticas)
                contador_llaves += linea_limpia.count('{') - linea_limpia.count('}')
                
                if contador_llaves == 0:
                    escribir_bloque(contexto_actual, bloque_actual)
                    bloque_actual = []
                    contexto_actual = None

    if contexto_actual is not None and contador_llaves > 0:
        funcion_anterior = estadisticas[contexto_actual]["funciones"][-1]
        mensaje = f"Error en '{funcion_anterior}': Bloque sin cerrar. Faltan {contador_llaves} llaves '}}' de cierre."
        estadisticas[contexto_actual]["errores_sintaxis"].append(mensaje)
        escribir_bloque(contexto_actual, bloque_actual)
    imprimir_reporte(estadisticas)

def imprimir_reporte(estadisticas):
    '''
    ***
    Parametro : estadisticas: dict
    ***
    Retorno: None
    ***
    Esta funcion se encarga de imprimir el reporte final con las estadisticas obtenidas del archivo
    '''
    print("\n=== REPORTE DE EVALUACIÓN DE PRACTICANTES ===")
    orden_autores = ["snake", "camel", "pascal", "desconocido"]
    for autor in orden_autores:
        datos = estadisticas[autor]
        if len(datos["funciones"]) > 0:
            print(f"\nPRACTICANTE: {autor.capitalize()}")
            cant_funciones = len(datos["funciones"])
            nombres_funciones = ", ".join(datos["funciones"])
            print(f"- Funciones creadas: {cant_funciones} ({nombres_funciones})")
            print(f"- Variables declaradas: {datos['total_variables']}")

            cant_estilos = len(datos["errores_estilo"])
            if cant_estilos > 0:
                errores_str = ", ".join(datos["errores_estilo"])
                print(f"- Diferencias de estilo: {cant_estilos} ({errores_str})")
            else:
                print(f"- Diferencias de estilo: {cant_estilos}")
            
            cant_sintaxis = len(datos["errores_sintaxis"])
            print(f"- Errores de sintaxis: {cant_sintaxis}")

            for error in datos["errores_sintaxis"]:
                print(f"- {error}")

procesar_archivo()
