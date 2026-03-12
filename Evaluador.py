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
declaracion_variable = rf"(?:{tipo_dato}\s+{nombre_valido}\s*{operacion}\s*{valor}\s*;)"
retorno = rf"(?:\s*return\s+{nombre_valido}\s*;)"
comentario_one_line = rf"//\s*{palabra}"
comentario_multi_line = rf"/\*\s*{palabra}\s*\*/"

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
        return "Pascal"
    else:
        return "desconocido"
    
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
    contexto_actual = None

    with open('programa.txt','r',encoding='utf-8') as archivo:
        for linea in archivo:
            linea_limpia = linea.strip()

            if not linea_limpia:
                continue

            match_funcion = re.search(detector_funcion, linea_limpia)
            if match_funcion:
                nombre = match_funcion.group(1)
                contexto_actual=determinar_autor(nombre)

                print((f"linea: {linea_limpia}"))
                print(f"Funcion detectada Nombre: {nombre}| autor: {contexto_actual}")

procesar_archivo()