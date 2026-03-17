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

snake_case = rf"{letra_min}+(?:_{letra_min}+)*"
camelCase = rf"{letra_min}+(?:{letra_may}+{letra_min}+)+"
PascalCase = rf"(?:{letra_may}+{letra_min}*)+"
nombre_valido = rf"(?:{snake_case}|{camelCase}|{PascalCase})"

condicion = rf"(?:\(\s*{nombre_valido}\s*{operacion}\s*{valor}\s*\))"
estructura_control = rf"(?:(?:if|while)\s+{condicion}\s*\{{)"
cierre_bloque = r"\}"
detector_funcion = rf"(?:{tipo_dato})\s+({palabra})\s*\("
declaracion_variable = rf"(?:{tipo_dato})\s+({nombre_valido})\s*(?:{operacion})\s*(?:{valor})\s*;"
retorno = rf"(?:\s*return\s+{nombre_valido}\s*;)"
comentario_one_line = rf"//\s*{palabra}"
comentario_multi_line = rf"/\*\s*{palabra}\s*\*/"

variable_sin_punto_coma = rf"^(?:{tipo_dato})\s+(?:{nombre_valido})\s*(?:{operacion})\s*(?:{valor})\s*[^;]$"
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

def escribir_bloque():
def verificar_llaves():
def procesar_archivo():
    '''
    ***
    Parametro: None
    ***
    Retorno: None
    ***
    Esta funcion lee el archivo programa.txt, va leyendo cada linea y evalua el contexto
    correspondiente
    '''
    
    archivos_salida = ['snake.txt', 'camel.txt', 'pascal.txt', 'desconocido.txt']
    for archivo in archivos_salida:
        with open(archivo, 'w',encoding='uft-8') as f:
            pass
    
    estadisticas = {
        "snake": {"funciones": [], "total_variables": 0, "errores_estilo": [], "errores_sintaxis": []},
        "camel": {"funciones": [], "total_variables": 0, "errores_estilo": [], "errores_sintaxis": []},
        "pascal": {"funciones": [], "total_variables": 0, "errores_estilo": [], "errores_sintaxis": []},
        "desconocido": {"funciones": [], "total_variables": 0, "errores_estilo": [], "errores_sintaxis": []}
    }

    contexto_actual = None
    bloque_actual = []

    with open('programa.txt', 'r', encoding='utf-8') as archivo:
        for linea in archivo: 
            linea_limpia = linea.strip()

            if not linea_limpia:
                continue

            match_funcion = re.search(detector_funcion, linea_limpia)
            if match_funcion:
                nombre = match_funcion.group(1)
                contexto_actual = determinar_autor(nombre).lower()

                estadisticas[contexto_actual]["funciones"].append(nombre)

                bloque_actual.append(linea)
            elif re.search(cierre_bloque, linea_limpia) and contexto_actual:
                bloque_actual.append(linea)
                with open(f'{contexto_actual}.txt', 'a', encoding='utf-8') as f:
                    f.writelines(bloque_actual)
                    f.write('\n')
                bloque_actual = []
                contexto_actual = None
            elif contexto_actual:
                bloque_actual.append(linea)
                for var_match in re.finditer(declaracion_variable,linea_limpia):
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
                        mensaje_error = f"La variable '{nombre_variable}' no es '{estilo_impresion}"
                        estadisticas[contexto_actual]["errores_estilo"].append(mensaje_error)

                funcion_actual = estadisticas[contexto_actual]["funciones"][-1]
                if re.match(variable_sin_punto_coma, linea_limpia):
                    mensaje_error = f"Error en {funcion_actual}: Falta ';' en la linea {linea_limpia}"
                    estadisticas[contexto_actual]["errores_sintaxis"].append(mensaje_error)
                elif re.match(retorno_sin_punto_coma, linea_limpia):
                    mensaje_error = f"Error en {funcion_actual}: Falta ';' en la linea {linea_limpia}"
                    estadisticas[contexto_actual]["errores_sintaxis"].append(mensaje_error)

                
procesar_archivo()
